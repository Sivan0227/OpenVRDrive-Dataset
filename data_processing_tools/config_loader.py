"""
config_loader.py - Unified configuration loader for multi-scenario support

This module provides a centralized way to load scenario-specific configuration
files for the OpenVRDrive dataset processing tools. It supports loading
configuration from any scenario folder, making the tools extensible to new
experimental scenarios.

Supported Configuration Sources:
    - JSON configuration files in scenario trials_info folders
    - Default fallback to Scenario 1 if no scenario specified

Usage:
    from config_loader import load_scenario_config, Constants
    
    # Load default scenario (scenario 1)
    config = load_scenario_config()
    constants = Constants(config)
    
    # Load specific scenario by name
    config = load_scenario_config(scenario_name="scenario2-Highway Merge")
    
    # Load from custom path
    config = load_scenario_config(config_path="/path/to/config.json")
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any, List


# ============================================================================
# DEFAULT CONFIGURATION
# ============================================================================

# Base directory of the dataset (parent of data_processing_tools)
BASE_DIR = Path(__file__).parent.parent

# Default scenario configuration path
DEFAULT_SCENARIO = "scenario1-HDV cuts into a CAV Platoon"
DEFAULT_CONFIG_PATH = BASE_DIR / DEFAULT_SCENARIO / "trials_info" / "scenario1_trial_params.json"


# ============================================================================
# CONFIGURATION LOADER FUNCTIONS
# ============================================================================

def find_scenario_config(scenario_name: str) -> Optional[Path]:
    """
    Find the configuration file for a given scenario.
    
    Args:
        scenario_name: Name of the scenario folder (e.g., "scenario1-HDV cuts into a CAV Platoon")
        
    Returns:
        Path to the scenario's configuration JSON file, or None if not found
    """
    scenario_dir = BASE_DIR / scenario_name / "trials_info"
    
    if not scenario_dir.exists():
        return None
    
    # Look for any JSON config file in the trials_info folder
    json_files = list(scenario_dir.glob("*_trial_params.json"))
    
    if json_files:
        return json_files[0]
    
    return None


def list_available_scenarios() -> List[str]:
    """
    List all available scenarios in the dataset.
    
    Returns:
        List of scenario folder names that have valid configuration files
    """
    scenarios = []
    
    for item in BASE_DIR.iterdir():
        if item.is_dir() and item.name.startswith("scenario"):
            config_path = find_scenario_config(item.name)
            if config_path is not None:
                scenarios.append(item.name)
    
    return sorted(scenarios)


def load_scenario_config(
    scenario_name: Optional[str] = None,
    config_path: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Load trial parameters from a scenario configuration file.
    
    Args:
        scenario_name: Name of the scenario folder (optional)
        config_path: Direct path to config file (optional, takes precedence)
        
    Returns:
        Dictionary containing the scenario configuration
        
    Raises:
        FileNotFoundError: If no configuration file can be found
        json.JSONDecodeError: If the configuration file is invalid
    """
    # Determine which config path to use
    if config_path is not None:
        target_path = Path(config_path)
    elif scenario_name is not None:
        target_path = find_scenario_config(scenario_name)
        if target_path is None:
            raise FileNotFoundError(
                f"No configuration file found for scenario: {scenario_name}"
            )
    else:
        # Use default scenario
        target_path = DEFAULT_CONFIG_PATH
    
    # Verify file exists
    if not target_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {target_path}")
    
    # Load and return configuration
    with open(target_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Add metadata about the source
    config['_config_path'] = str(target_path)
    
    return config


# ============================================================================
# CONSTANTS CLASS
# ============================================================================

class Constants:
    """
    Container class for scenario-specific experimental parameters.
    
    This class provides easy access to parameter names, values, and lookup
    dictionaries for mapping between parameter combinations and scenario IDs.
    
    Attributes:
        scenario_name: Human-readable name of the scenario
        scenario_id: Numeric identifier for the scenario
        discretionary: List of parameter names for DLC (discretionary lane change)
        mandatory: List of parameter names for MLC (mandatory lane change)
        param_dict: Dictionary mapping experiment type to parameter names
        discretionary_params: List of parameter value combinations for DLC
        mandatory_params: List of parameter value combinations for MLC
        discretionary_param_dict: Mapping from param string to scenario index
        mandatory_param_dict: Mapping from param string to scenario index
    
    Example:
        >>> constants = Constants(load_scenario_config())
        >>> print(constants.discretionary)
        ['cav_max_speed', 'cav_time_gap', 'front_hdv_speed', 'platoon_size']
        >>> print(constants.discretionary_params[0])
        [72, 0.6, 64.8, 7]
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Constants from a configuration dictionary.
        
        Args:
            config: Configuration dictionary loaded from JSON file
        """
        # Scenario metadata
        self.scenario_name = config.get('scenario_name', 'Unknown')
        self.scenario_id = config.get('scenario_id', 0)
        
        # Parameter names
        self.discretionary = config['parameter_names']['discretionary']
        self.mandatory = config['parameter_names']['mandatory']
        self.param_dict = config['parameter_names']
        
        # Parameter value combinations
        self.discretionary_params = config['discretionary_params']
        self.mandatory_params = config['mandatory_params']
        
        # Create lookup dictionaries for fast parameter-to-index mapping
        # Key: string representation of parameter list
        # Value: scenario index
        self.discretionary_param_dict = {
            str(p): i for i, p in enumerate(self.discretionary_params)
        }
        self.mandatory_param_dict = {
            str(p): i for i, p in enumerate(self.mandatory_params)
        }
        
        # Store config path for reference
        self._config_path = config.get('_config_path', None)
    
    def get_param_dict(self, exp_type: str) -> Dict[str, int]:
        """
        Get the parameter-to-index mapping for a given experiment type.
        
        Args:
            exp_type: Either 'discretionary' or 'mandatory'
            
        Returns:
            Dictionary mapping parameter string to scenario index
        """
        return getattr(self, f'{exp_type}_param_dict')
    
    def get_params(self, exp_type: str) -> List[List]:
        """
        Get all parameter combinations for a given experiment type.
        
        Args:
            exp_type: Either 'discretionary' or 'mandatory'
            
        Returns:
            List of parameter value combinations
        """
        return getattr(self, f'{exp_type}_params')
    
    def get_param_names(self, exp_type: str) -> List[str]:
        """
        Get parameter names for a given experiment type.
        
        Args:
            exp_type: Either 'discretionary' or 'mandatory'
            
        Returns:
            List of parameter names
        """
        return self.param_dict[exp_type]
    
    def __repr__(self) -> str:
        return (
            f"Constants(scenario='{self.scenario_name}', "
            f"dlc_scenarios={len(self.discretionary_params)}, "
            f"mlc_scenarios={len(self.mandatory_params)})"
        )


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def get_default_constants() -> Constants:
    """
    Get Constants object for the default scenario.
    
    Returns:
        Constants object initialized with default scenario configuration
    """
    return Constants(load_scenario_config())


def get_constants_for_scenario(scenario_name: str) -> Constants:
    """
    Get Constants object for a specific scenario.
    
    Args:
        scenario_name: Name of the scenario folder
        
    Returns:
        Constants object initialized with the specified scenario configuration
    """
    return Constants(load_scenario_config(scenario_name=scenario_name))


# ============================================================================
# MODULE-LEVEL TESTING
# ============================================================================

if __name__ == '__main__':
    # Test the configuration loader
    print("Testing config_loader module...")
    print()
    
    # List available scenarios
    scenarios = list_available_scenarios()
    print(f"Available scenarios: {scenarios}")
    print()
    
    # Load default configuration
    config = load_scenario_config()
    print(f"Loaded config from: {config['_config_path']}")
    print(f"Scenario name: {config['scenario_name']}")
    print(f"Scenario ID: {config['scenario_id']}")
    print()
    
    # Create Constants object
    constants = Constants(config)
    print(f"Constants: {constants}")
    print(f"DLC parameter names: {constants.discretionary}")
    print(f"MLC parameter names: {constants.mandatory}")
    print(f"Number of DLC scenarios: {len(constants.discretionary_params)}")
    print(f"Number of MLC scenarios: {len(constants.mandatory_params)}")
