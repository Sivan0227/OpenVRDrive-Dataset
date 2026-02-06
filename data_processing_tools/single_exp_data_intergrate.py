"""
single_exp_data_intergrate.py - Integrate data from a single experiment trial

This module handles the integration of VR eye-tracking data with vehicle
trajectory data from CARLA for a single experimental trial. It performs:
1. Time alignment between VR data and trajectory data
2. Data filtering and synchronization
3. Experiment metadata extraction from file names

The output is a unified JSON structure containing all data streams aligned
by timestamp.

Usage:
    from single_exp_data_intergrate import SingleExpDataIntergrate
    
    integrator = SingleExpDataIntergrate(traj_path, vr_path)
    result = integrator.run()
"""

import json
import os
from pathlib import Path
from config_loader import load_scenario_config, Constants

# Load default scenario configuration (can be overridden per-instance)
constants = Constants(load_scenario_config())

class SingleExpDataIntergrate:
    """
    Integrates VR eye-tracking data with vehicle trajectory data for a single trial.
    
    This class handles the complex task of aligning two different data sources:
    - VR data: Eye tracking, user inputs, ego vehicle state (from DreyeVR)
    - Trajectory data: Position, rotation, velocity of all vehicles (from CARLA recorder)
    
    The main challenge is that these data streams have different sampling rates
    and time references, requiring careful timestamp alignment.
    
    Attributes:
        traj_data_path: Path to trajectory JSON file
        vr_data_path: Path to VR data JSON file
        have_vr_data: Whether raw VR data is provided directly
        raw_vr_data: Pre-loaded VR data (optional)
    """

    def __init__(self, traj_data_path: str, vr_data_path: str, raw_vr_data: dict = None):
        """
        Initialize the data integrator.
        
        Args:
            traj_data_path: Path to the trajectory data JSON file
            vr_data_path: Path to the VR data JSON file
            raw_vr_data: Optional pre-loaded VR data dictionary
        """
        self.traj_data_path = traj_data_path
        self.vr_data_path = vr_data_path
        self.have_vr_data = False
        if raw_vr_data is not None:
            self.have_vr_data = True
            self.raw_vr_data = raw_vr_data

    def read_json(self, file_path: str) -> dict:
        """Load JSON data from file."""
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data

    def find_vr_veh(self, traj_data: dict) -> str:
        """
        Find the vehicle ID that corresponds to the VR-controlled ego vehicle.
        
        The trajectory data contains multiple vehicles. This method identifies
        which one is the human-driven VR vehicle by checking the 'if_vr' flag.
        
        Args:
            traj_data: Dictionary containing trajectory data for all vehicles
            
        Returns:
            Vehicle ID string for the VR vehicle, or None if not found
        """
        for key in traj_data.keys():
            if True in traj_data[key]['if_vr']:
                return key
        return None

    def filter_ts(self, vr_v_traj: dict, vr_data: dict) -> dict:
        """
        Filter VR data to only include timestamps present in trajectory data.
        
        Since VR data may have a higher sampling rate than trajectory data,
        this method selects the VR samples closest to each trajectory timestamp.
        
        Args:
            vr_v_traj: Trajectory data for the VR vehicle
            vr_data: Full VR data dictionary
            
        Returns:
            Updated trajectory dict with synchronized VR data added
        """
        vaild_idx = []
        for ts in vr_v_traj['carla_ts']:
            ts = int(ts * 1000)  # Convert to milliseconds
            min_diff_idx = self.find_closest_ts(ts, vr_data, vaild_idx)
            vaild_idx.append(min_diff_idx)
        vr_v_traj = self.delete_vr_data(vr_v_traj, vr_data, vaild_idx)
        return vr_v_traj

    def delete_vr_data(self, vr_v_traj: dict, vr_data: dict, vaild_idx: list) -> dict:
        """
        Extract VR data at specified indices and merge into trajectory data.
        
        This method flattens the nested VR data structure and extracts only
        the samples at the specified indices (those matching trajectory timestamps).
        
        Args:
            vr_v_traj: Trajectory data for the VR vehicle
            vr_data: Full VR data dictionary
            vaild_idx: List of indices to extract from VR data
            
        Returns:
            Updated trajectory dict with VR data fields added
        """
        # Top-level keys that contain single arrays
        first_level_keys = ['TimeElapsed', 'TimestampCarla']
        # Keys containing nested dictionaries
        second_level_keys = ['EyeTracker', 'FocusInfo', 'EgoVariables', 'UserInputs']
        
        for key in vr_data.keys():
            if key == 'Actors':
                continue  # Skip actor data
            if key in first_level_keys:
                vr_v_traj[key] = [vr_data[key][i] for i in vaild_idx]
            elif key in second_level_keys:
                # Flatten nested structure into trajectory dict
                for sub_key in vr_data[key].keys():
                    vr_v_traj[sub_key] = [vr_data[key][sub_key][i] for i in vaild_idx]
        return vr_v_traj

    def find_closest_ts(self, ts: int, vr_data: dict, vaild_idx: list) -> int:
        """
        Find the VR data index closest to a given trajectory timestamp.
        
        Ensures each VR sample is only used once (no duplicate matches).
        
        Args:
            ts: Target timestamp in milliseconds
            vr_data: VR data dictionary containing 'TimestampCarla'
            vaild_idx: List of already-used indices to exclude
            
        Returns:
            Index of the closest matching VR timestamp
        """
        ts_diff = [abs(ts - vr_ts) for vr_ts in vr_data['TimestampCarla']]
        min_diff = min(ts_diff)
        min_diff_idx = ts_diff.index(min_diff)
        
        # Ensure we don't reuse the same index
        while min_diff_idx in vaild_idx:
            ts_diff[min_diff_idx] = 100000  # Mark as used
            min_diff = min(ts_diff)
            min_diff_idx = ts_diff.index(min_diff)
        return min_diff_idx

    def cut_traj_data(self, traj_data: dict, interval: list) -> dict:
        """
        Trim trajectory data to a specified time interval.
        
        Args:
            traj_data: Dictionary of vehicle trajectories
            interval: [start_time, end_time] in milliseconds
            
        Returns:
            Trimmed trajectory data
        """
        for veh_id in traj_data.keys():
            # Filter each data field to only include samples within the interval
            for key in traj_data[veh_id].keys():
                if key != 'carla_ts':
                    traj_data[veh_id][key] = [
                        value for i, value in enumerate(traj_data[veh_id][key])
                        if interval[0] <= int(traj_data[veh_id]['carla_ts'][i] * 1000) <= interval[1]
                    ]
            # Filter timestamps separately
            traj_data[veh_id]['carla_ts'] = [
                value for i, value in enumerate(traj_data[veh_id]['carla_ts'])
                if interval[0] <= int(traj_data[veh_id]['carla_ts'][i] * 1000) <= interval[1]
            ]
        return traj_data

    def determine_interval(self, traj_data: dict, vr_data: dict, vr_veh_id: str) -> list:
        """
        Determine the overlapping time interval between VR and trajectory data.
        
        Both data sources may have different start/end times. This method finds
        the intersection where both sources have valid data.
        
        Args:
            traj_data: Trajectory data dictionary
            vr_data: VR data dictionary
            vr_veh_id: Vehicle ID of the VR-controlled vehicle
            
        Returns:
            [start_time, end_time] interval in milliseconds
        """
        # VR data time range
        min_vr_ts = vr_data['TimestampCarla'][0]
        max_vr_ts = vr_data['TimestampCarla'][-1]
        
        # Trajectory data time range (convert to milliseconds)
        min_traj_ts = int(traj_data[vr_veh_id]['carla_ts'][0] * 1000)
        max_traj_ts = int(traj_data[vr_veh_id]['carla_ts'][-1] * 1000)
        
        # Find intersection
        interval = [max(min_vr_ts, min_traj_ts), min(max_vr_ts, max_traj_ts)]
        return interval

    def time_alignment(self, traj_data_path: str, vr_data_path: str) -> dict:
        """
        Perform time alignment between trajectory and VR data.
        
        This is the core data integration step that:
        1. Identifies the VR-controlled vehicle
        2. Finds the common time interval
        3. Trims trajectory data to this interval
        4. Synchronizes VR data to trajectory timestamps
        
        Args:
            traj_data_path: Path to trajectory JSON file
            vr_data_path: Path to VR data JSON file
            
        Returns:
            Dictionary with 'vr_id' and 'all_veh_info' containing aligned data
        """
        traj_data = self.read_json(traj_data_path)
        
        if not self.have_vr_data:
            vr_data = self.read_json(vr_data_path)
        else:
            vr_data = self.raw_vr_data
        
        vr_veh_id = self.find_vr_veh(traj_data)
        print(f"VR vehicle ID: {vr_veh_id}")
        
        # Determine overlapping time interval
        interval = self.determine_interval(traj_data, vr_data, vr_veh_id)
        
        # Trim trajectory data to the common interval
        traj_data = self.cut_traj_data(traj_data, interval)
        
        # Synchronize VR data to trajectory timestamps
        traj_data[vr_veh_id] = self.filter_ts(traj_data[vr_veh_id], vr_data)
        
        return {'vr_id': vr_veh_id, 'all_veh_info': traj_data}

    def divide_file_name(self, file_name: str) -> dict:
        """
        Parse experiment parameters from the file name.
        
        File names follow the pattern: {exp_type}_[param1, param2, ...].json
        Example: discretionary_[72, 0.6, 64.8, 7].json
        
        Args:
            file_name: Name of the trajectory file
            
        Returns:
            Dictionary with 'type', 'param_name', and 'param' keys
        """
        file_name = os.path.basename(file_name)
        file_name_parts = file_name.split('_')
        exp_type = file_name_parts[0]  # 'discretionary' or 'mandatory'
        
        # Extract parameter string (remove .json suffix)
        exp_param_name = file_name_parts[-1][:-5]  # e.g., "[72, 0.6, 64.8, 7]"
        
        # Parse parameter values
        exp_param = exp_param_name[1:-1].split(',')  # Remove brackets and split
        exp_param = [eval(i.strip()) for i in exp_param]  # Convert to numbers
        
        # Map parameter values to named parameters
        param_name_list = constants.param_dict[exp_type]
        exp_param_dict = {
            param_name_list[i]: exp_param[i] 
            for i in range(len(param_name_list))
        }

        return {
            'type': exp_type,
            'param_name': exp_param_name,
            'param': exp_param_dict
        }

    def add_exp_info(self, traj_data: dict, traj_data_path: str) -> dict:
        """
        Add experiment metadata to the integrated data.
        
        Args:
            traj_data: Integrated trajectory and VR data
            traj_data_path: Path to the original trajectory file
            
        Returns:
            Data dictionary with 'exp_info' field added
        """
        traj_data_name = traj_data_path.split('/')[-1]
        exp_info = self.divide_file_name(traj_data_name)
        
        # Create new dictionary with exp_info at the top
        data = {'exp_info': exp_info}
        for key in traj_data.keys():
            data[key] = traj_data[key]
        return data

    def run(self) -> dict:
        """
        Execute the full data integration pipeline.
        
        Returns:
            Integrated data dictionary containing:
            - exp_info: Experiment metadata (type, parameters)
            - vr_id: Vehicle ID of the VR-controlled vehicle
            - all_veh_info: Trajectory data for all vehicles with VR data merged
        """
        # Step 1: Align timestamps between trajectory and VR data
        new_data = self.time_alignment(self.traj_data_path, self.vr_data_path)
        
        # Step 2: Add experiment metadata from file name
        new_data = self.add_exp_info(new_data, self.traj_data_path)
        
        # TODO: Add questionnaire data integration
        return new_data


if __name__ == '__main__':
    traj_data_path = './1/discretionary_[500, 500, 500, 2, 20, 5]/discretionary_[500, 500, 500, 2, 20, 5].json'
    vr_data_path = './1/discretionary_[500, 500, 500, 2, 20, 5]/data.json'
    intergrater = SingleExpDataIntergrate(traj_data_path, vr_data_path)
    new_data = intergrater.run()
    # print(new_data['all_veh_info']['97']['carla_ts'])
    print(new_data.keys())
    print(new_data['exp_info'].keys())
    print(new_data['exp_info']['type'])
    print(new_data['exp_info']['param_name'])
    print(new_data['exp_info']['param'])
    print(new_data['all_veh_info']['97'].keys())
