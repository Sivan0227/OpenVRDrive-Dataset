"""
intergrate_all.py - Aggregate all experimental data into a unified dataset

This script combines trajectory and VR data from all participants and scenarios
into a single structured JSON file for analysis. The output organizes data by:
1. Experiment type (discretionary/mandatory lane change)
2. Scenario parameter combination
3. Participant ID

Usage:
    python intergrate_all.py [--scenario SCENARIO_NAME] [--output OUTPUT_FILE]

Output Structure:
    {
        "discretionary": {
            "0": {"participant_00": {...}, "participant_01": {...}, ...},
            "1": {...},
            ...
        },
        "mandatory": {
            "0": {...},
            ...
        }
    }
"""

import os
import json
import argparse
from pathlib import Path
from config_loader import load_scenario_config, Constants

# Load default scenario configuration
constants = Constants(load_scenario_config())


# ============================================================================
# DATA STRUCTURE FUNCTIONS
# ============================================================================

def create_data_format(constants: Constants = constants) -> dict:
    """
    Create the hierarchical data structure for storing all experiment data.
    
    The structure organizes data by:
    - Experiment type (discretionary/mandatory)
    - Scenario index (0, 1, 2, ... based on parameter combinations)
    - Participant ID
    
    Args:
        constants: Constants object with scenario parameters
        
    Returns:
        Empty nested dictionary structure ready to be populated
    """
    data_final = {
        'discretionary': {},
        'mandatory': {}
    }
    # Create empty dict for each scenario index
    data_final['discretionary'] = {
        i: {} for i in range(len(constants.discretionary_params))
    }
    data_final['mandatory'] = {
        i: {} for i in range(len(constants.mandatory_params))
    }
    return data_final


# ============================================================================
# FILE DISCOVERY FUNCTIONS
# ============================================================================

def find_all_person_data(data_dir: str) -> list:
    """
    Find all participant trajectory data directories.
    
    Looks for directories named with numeric IDs (participant IDs) and
    returns paths to their 'traj_data' subdirectories.
    
    Args:
        data_dir: Root directory containing processed participant data
        
    Returns:
        List of paths to trajectory data directories, sorted by participant ID
    """
    person_dirs = [
        os.path.join(data_dir, person_dir, 'traj_data')
        for person_dir in os.listdir(data_dir)
        if person_dir.isdigit()
    ]
    return sorted(person_dirs, key=lambda x: int(os.path.basename(os.path.dirname(x))))


# ============================================================================
# FILE I/O FUNCTIONS
# ============================================================================

def read_json(json_file: str) -> dict:
    """Load JSON data from file."""
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data


def save_json(data: dict, json_file: str) -> None:
    """Save data to JSON file with proper formatting."""
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to: {json_file}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def run(
    data_dir: str = None,
    output_file: str = None,
    max_participants: int = None
) -> None:
    """
    Aggregate all experimental data into a unified dataset.
    
    This function reads all processed trajectory data files and organizes
    them into a hierarchical structure for easy analysis.
    
    Args:
        data_dir: Path to directory containing processed data (default: ../lc_data_all)
        output_file: Path for output JSON file (default: ../data_all.json)
        max_participants: Limit number of participants to process (for testing)
    """
    # Initialize the output data structure
    data_final = create_data_format()
    
    # Set up directories
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    
    if data_dir is None:
        data_dir = os.path.join(parent_dir, 'lc_data_all')
    
    if output_file is None:
        output_file = os.path.join(parent_dir, 'data_all.json')
    
    # Find all participant directories
    person_dirs = find_all_person_data(data_dir)
    print(f"Found {len(person_dirs)} participant directories in: {data_dir}")
    
    # Process each participant
    processed_count = 0
    for person_dir in person_dirs:
        # Check if we've reached the limit
        if max_participants is not None and processed_count >= max_participants:
            print(f"Reached maximum participant limit: {max_participants}")
            break
        
        participant_id = os.path.basename(os.path.dirname(person_dir))
        print(f"Processing participant: {participant_id}")
        
        # Get all JSON files in the trajectory data directory
        all_files = os.listdir(person_dir)
        if '.DS_Store' in all_files:
            all_files.remove('.DS_Store')
        
        json_files = [
            os.path.join(person_dir, f)
            for f in all_files
            if f.endswith('.json')
        ]
        
        # Process each trial for this participant
        for json_file in json_files:
            data = read_json(json_file)
            
            # Extract experiment type and scenario index
            exp_type = data['exp_info']['type']  # 'discretionary' or 'mandatory'
            param_dict = getattr(constants, f'{exp_type}_param_dict')
            scenario_idx = param_dict[str(data['exp_info']['param_name'])]
            
            # Store data in the hierarchical structure
            data_final[exp_type][scenario_idx][participant_id] = data
        
        processed_count += 1
    
    # Save the aggregated data
    save_json(data_final, output_file)
    print(f"Successfully aggregated data from {processed_count} participants")


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Aggregate all experimental data into a unified dataset'
    )
    parser.add_argument(
        '--data-dir', '-d',
        type=str,
        default=None,
        help='Path to directory containing processed data'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='Path for output JSON file'
    )
    parser.add_argument(
        '--max-participants', '-m',
        type=int,
        default=None,
        help='Maximum number of participants to process (for testing)'
    )
    args = parser.parse_args()
    
    run(
        data_dir=args.data_dir,
        output_file=args.output,
        max_participants=args.max_participants
    )
            


