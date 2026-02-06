"""
log2txt.py - Convert CARLA recorder log files to human-readable text format

This script converts binary CARLA recorder (.log) files to text format (.txt)
using the CARLA show_recorder_file_info.py utility. This is a necessary
preprocessing step before parsing the VR driving data.

Usage:
    python log2txt.py [--scenario SCENARIO_NAME] [--data-dir DATA_DIR]

Requirements:
    - CARLA Python API must be installed and accessible
    - Path to show_recorder_file_info.py must be configured
"""

import subprocess
import os
import json
import argparse
from pathlib import Path
from config_loader import load_scenario_config, Constants


# ============================================================================
# CONFIGURATION
# ============================================================================

# Path to CARLA's recorder info utility (modify according to your installation)
CARLA_RECORDER_SCRIPT = 'show_recorder_file_info.py'


# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def run_convert(log_file: str, carla_script_path: str = CARLA_RECORDER_SCRIPT) -> None:
    """
    Convert a single CARLA recorder log file to text format.
    
    Args:
        log_file: Path to the .log file to convert
        carla_script_path: Path to CARLA's show_recorder_file_info.py script
    
    The output .txt file will be saved in the same directory as the input .log file.
    """
    save_file = log_file.replace('.log', '.txt')
    
    # Run CARLA recorder conversion utility
    # -a: Show all actor information
    # -f: Input file path
    # -s: Save output to file
    subprocess.run([
        'python', carla_script_path,
        '-a', '-f', log_file,
        '-s', save_file
    ])
    print(f"Converted: {log_file} -> {save_file}")


def find_all_exp_data(person_dir: str) -> None:
    """
    Find and convert all experiment log files for a single participant.
    
    Args:
        person_dir: Path to the participant's data directory
        
    Each participant's directory contains multiple experiment folders,
    and each experiment folder contains one .log file to be converted.
    """
    print(f'Processing participant directory: {os.path.basename(person_dir)}')
    
    # Get all experiment directories for this participant
    all_exp = os.listdir(person_dir)
    
    # Ignore system files
    if '.DS_Store' in all_exp:
        all_exp.remove('.DS_Store')
    
    exp_data_dirs = [os.path.join(person_dir, exp_data_dir) for exp_data_dir in all_exp]

    for exp_data_dir in exp_data_dirs:
        # Process each experiment directory
        all_files = os.listdir(exp_data_dir)
        
        # Filter out system files
        if '.DS_Store' in all_files:
            all_files.remove('.DS_Store')
        
        # Find the .log file in this experiment directory
        log_files = [os.path.join(exp_data_dir, f) for f in all_files if f.endswith('.log')]
        
        if log_files:
            log_file = log_files[0].replace('\\', '/')
            print(f"Found log file: {log_file}")
            run_convert(log_file)


def find_all_person_data(data_dir: str) -> list:
    """
    Find all participant directories in the data folder.
    
    Args:
        data_dir: Root directory containing participant folders
        
    Returns:
        List of paths to participant directories (folders named with numeric IDs)
    """
    person_dirs = [
        os.path.join(data_dir, person_dir) 
        for person_dir in os.listdir(data_dir) 
        if person_dir.isdigit()
    ]
    return sorted(person_dirs, key=lambda x: int(os.path.basename(x)))


def read_json(json_file: str) -> dict:
    """Load JSON data from file."""
    with open(json_file, 'r') as f:
        return json.load(f)


def save_json(data: dict, json_file: str) -> None:
    """Save data to JSON file with proper formatting."""
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def run(data_dir: str = None) -> None:
    """
    Main function to convert all log files in the dataset.
    
    Args:
        data_dir: Optional custom data directory path
    """
    if data_dir is None:
        # Default: look for data in parent directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        data_dir = os.path.join(parent_dir, 'lc_exp_data')
    
    print(f"Searching for participant data in: {data_dir}")
    person_dirs = find_all_person_data(data_dir)
    print(f"Found {len(person_dirs)} participant directories")

    for person_dir in person_dirs:
        find_all_exp_data(person_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert CARLA recorder log files to text format'
    )
    parser.add_argument(
        '--data-dir', '-d',
        type=str,
        default=None,
        help='Path to the raw experiment data directory'
    )
    args = parser.parse_args()
    
    run(data_dir=args.data_dir)
            


