# Run Artifacts - Experimental Data Files

## Download

**Download Links:**
- **Google Drive**: [Download from Google Drive](https://drive.google.com/drive/folders/1ixFzhkEnIM2vLZJF8hQ7Bcm9Ad15Xf51?usp=drive_link)
- **Baidu Netdisk** (百度网盘): [下载链接](#) | 提取码: [XXXX]

**Package Contents**:
- Complete run artifacts for all 60 participants
- Organized by participant ID (00-59)
- Includes `.log`, `.txt`, and `.json` files for each trial
- **Size**: ~2.7 GB (compressed), ~5.5 GB (uncompressed)

**After Downloading**:
1. Extract the archive to the `run_artifacts/` directory
2. Verify directory structure matches expected format
3. Run validation script to check for missing files
4. Proceed with data processing using tools in `data_processing_tools/`

---

This folder contains the raw experimental data files generated during VR driving simulation experiments. These artifacts include CARLA simulation logs, converted text files, and trajectory data for each experimental trial.

## Overview

Run artifacts are the direct outputs from the CARLA simulator and data collection system. Each trial produces three types of files that capture different aspects of the experimental session:

- **`.log` files**: Binary CARLA recorder files (raw simulation data)
- **`.txt` files**: Human-readable converted logs (VR data, eye tracking, vehicle states)
- **`.json` files**: Structured trajectory data (vehicle positions, rotations, velocities)

## File Naming Convention

All files follow a consistent naming pattern that encodes the experimental parameters:

```
{exp_type}_[{param1}, {param2}, {param3}, ...].{extension}
```

### Discretionary Lane Change (DLC) Files

Format: `discretionary_[cav_speed, time_gap, front_hdv_speed, platoon_size].{ext}`

**Example**: `discretionary_[72, 0.6, 57.6, 0].json`
- **Experiment Type**: Discretionary lane change
- **CAV Platoon Speed**: 72 km/h
- **Time Gap**: 0.6 seconds
- **Front HDV Speed**: 57.6 km/h (20% reduction from platoon)
- **Platoon Size**: 0 (traditional traffic baseline)

**Parameter Breakdown**:
| Position | Parameter | Description | Example Values |
|----------|-----------|-------------|----------------|
| 1 | `cav_speed` | CAV platoon cruising speed (km/h) | 72, 108 |
| 2 | `time_gap` | Time gap between CAVs (seconds) | 0.6, 0.9, 1.2 |
| 3 | `front_hdv_speed` | Leading HDV speed (km/h) | 64.8, 57.6 (10%, 20% reduction) |
| 4 | `platoon_size` | Number of CAVs in platoon | 7, 0 (0 = traditional traffic) |

### Mandatory Lane Change (MLC) Files

Format: `mandatory_[cav_speed, time_gap, platoon_size].{ext}`

**Example**: `mandatory_[108, 1.2, 7].txt`
- **Experiment Type**: Mandatory lane change
- **CAV Platoon Speed**: 108 km/h
- **Time Gap**: 1.2 seconds
- **Platoon Size**: 7 CAVs

**Parameter Breakdown**:
| Position | Parameter | Description | Example Values |
|----------|-----------|-------------|----------------|
| 1 | `cav_speed` | CAV platoon cruising speed (km/h) | 72, 108 |
| 2 | `time_gap` | Time gap between CAVs (seconds) | 0.6, 0.9, 1.2 |
| 3 | `platoon_size` | Number of CAVs in platoon | 7, 0 (0 = traditional traffic) |

**Note**: MLC scenarios don't have a `front_hdv_speed` parameter because they are triggered by a work zone closure, not by a slow leading vehicle.

## File Types

### 1. `.log` Files (CARLA Binary Logs)

**Purpose**: Raw binary recording from CARLA simulator

**Content**:
- Complete simulation state at each frame
- All actor positions, rotations, and velocities
- Physics simulation data
- Traffic light states
- Sensor data references

**Size**: Typically 300-600 KB per trial

**Usage**: 
- Input for CARLA's `show_recorder_file_info.py` script
- First step in data processing pipeline (convert to `.txt`)

**Processing**:
```bash
python log2txt.py --data-dir /path/to/run_artifacts
```

### 2. `.txt` Files (Converted VR Logs)

**Purpose**: Human-readable VR session data with eye tracking and user inputs

**Content**:
- **Frame timestamps**: Wall-clock time for each frame
- **VR data** (`[DReyeVR]` tag): 
  - Eye tracking: Pupil diameter, gaze direction, eye openness
  - Head tracking: HMD position and rotation
  - User inputs: Steering, throttle, brake, gear
  - Ego vehicle state: Position, velocity, acceleration
- **Custom actor data** (`[DReyeVR_CA]` tag):
  - Additional tracked objects in the scene
- **Actor data** (`Id:` tag):
  - Positions and rotations of all vehicles in the simulation

**Size**: Typically 1-1.5 MB per trial

**Format Example**:
```
Frame 0 at 0.000 seconds
[DReyeVR]TimestampCarla:0.000 EgoVariables:{Location:X=100.0 Y=200.0 Z=50.0} ...
[DReyeVR]EyeTracker:{COMBINEDGazeDir:X=0.99 Y=0.01 Z=0.01} LEFTPupilDiameter:3.2 ...
Id: 123 Location:(100.0, 200.0, 50.0) Rotation:(0.0, 90.0, 0.0)
Frame 1 at 0.033 seconds
...
```

**Usage**:
- Input for VR data parsing (`src/parser.py`)
- Can be opened in text editor for manual inspection
- Used by `single_exp_data_intergrate.py` for integration

### 3. `.json` Files (Trajectory Data)

**Purpose**: Structured vehicle trajectory data for all actors

**Content**:
- Complete trajectories for all vehicles in the scene
- Vehicle metadata (type, role, VR flag)
- Synchronized timestamps with CARLA simulation time

**Size**: Typically 800-1200 KB per trial

**Format Structure**:
```json
{
  "123": {
    "carla_ts": [0.0, 0.033, 0.067, ...],
    "location": [[100.0, 200.0, 50.0], [100.5, 200.1, 50.0], ...],
    "rotation": [[0.0, 90.0, 0.0], [0.0, 90.5, 0.0], ...],
    "velocity": [[10.0, 0.0, 0.0], [10.1, 0.0, 0.0], ...],
    "angular_velocity": [[0.0, 0.0, 0.0], [0.0, 0.1, 0.0], ...],
    "acceleration": [[0.0, 0.0, 0.0], [0.1, 0.0, 0.0], ...],
    "type_id": "vehicle.tesla.model3",
    "role_name": "ego_vehicle",
    "if_vr": true
  },
  "124": {
    "carla_ts": [0.0, 0.033, ...],
    "location": [[150.0, 200.0, 50.0], ...],
    ...
    "type_id": "vehicle.audi.a2",
    "role_name": "autopilot",
    "if_vr": false
  },
  ...
}
```

**Key Fields**:
- `carla_ts`: Simulation timestamps (seconds)
- `location`: Position [X, Y, Z] in meters (Unreal Engine coordinates)
- `rotation`: Euler angles [Pitch, Yaw, Roll] in degrees
- `velocity`: Velocity [X, Y, Z] in m/s
- `angular_velocity`: Angular velocity [X, Y, Z] in rad/s
- `acceleration`: Acceleration [X, Y, Z] in m/s²
- `type_id`: CARLA blueprint ID
- `role_name`: Actor role in simulation
- `if_vr`: Boolean flag indicating human-controlled VR vehicle

**Usage**:
- Direct input for trajectory analysis
- Merged with VR data in `single_exp_data_intergrate.py`
- Used for visualization and statistical analysis

## Directory Structure

The run artifacts are organized by participant ID and scenario:

```
run_artifacts/
├── 00/                                          # Participant ID
│   ├── discretionary_[72, 0.6, 64.8, 7].log
│   ├── discretionary_[72, 0.6, 64.8, 7].txt
│   ├── discretionary_[72, 0.6, 64.8, 7].json
│   ├── discretionary_[72, 0.6, 57.6, 7].log
│   ├── discretionary_[72, 0.6, 57.6, 7].txt
│   ├── discretionary_[72, 0.6, 57.6, 7].json
│   ├── mandatory_[72, 0.6, 7].log
│   ├── mandatory_[72, 0.6, 7].txt
│   ├── mandatory_[72, 0.6, 7].json
│   └── ...                                      # 16 trials total per participant
├── 01/
│   └── ...
...
└── 59/
    └── ...
```

## File Size Summary

Typical file sizes per trial:

| File Type | Size Range | Average |
|-----------|------------|---------|
| `.log` | 300-600 KB | ~470 KB |
| `.txt` | 1-1.5 MB | ~1.3 MB |
| `.json` | 800-1200 KB | ~1 MB |
| **Total per trial** | 2.1-3.3 MB | ~2.8 MB |

**Total Dataset Size Estimate**:
- 60 participants × 16 trials × 2.8 MB ≈ **2.7 GB** (compressed)
- Actual size may vary based on trial duration and number of actors

## Data Processing Workflow

### Step 1: Convert `.log` to `.txt`

```bash
cd data_processing_tools
python log2txt.py --data-dir ../scenario1-HDV\ cuts\ into\ a\ CAV\ Platoon/run_artifacts
```

This generates `.txt` files from `.log` files using CARLA's recorder API.

### Step 2: Parse and Integrate Data

```python
from single_exp_data_intergrate import SingleExpDataIntergrate

# Process a single trial
integrator = SingleExpDataIntergrate(
    traj_data_path='run_artifacts/00/discretionary_[72, 0.6, 64.8, 7].json',
    vr_data_path='run_artifacts/00/discretionary_[72, 0.6, 64.8, 7].txt'
)
result = integrator.run()
```

### Step 3: Batch Process

```python
from single_person_data_intergrate import SinglePersonDataIntegrate

# Process all trials for participant 00
processor = SinglePersonDataIntegrate(
    person_dir='run_artifacts/00',
    folder_dir='processed_data'
)
processor.find_all_exp_data()
```

See [data_processing_tools/README.md](../../../data_processing_tools/README.md) for detailed processing instructions.

## Data Quality Notes

### Missing Files

Some participants may have missing trials due to:
- Technical issues during recording
- Simulator crashes
- Data corruption
- Participant withdrawal from specific trials

**Expected Coverage**: Each participant should have 16 out of 22 possible scenarios (see trial assignment matrix).

### File Validation

To verify data integrity:

```python
import json
from pathlib import Path

def validate_trial_files(participant_dir):
    """Check if a participant has complete trial sets"""
    participant_dir = Path(participant_dir)
    
    # Find all base names (without extensions)
    base_names = set()
    for file in participant_dir.glob('*.*'):
        base_name = file.stem  # Filename without extension
        base_names.add(base_name)
    
    # Check each trial has all three file types
    incomplete_trials = []
    for base_name in base_names:
        has_log = (participant_dir / f"{base_name}.log").exists()
        has_txt = (participant_dir / f"{base_name}.txt").exists()
        has_json = (participant_dir / f"{base_name}.json").exists()
        
        if not (has_log and has_txt and has_json):
            incomplete_trials.append(base_name)
            print(f"⚠ Incomplete trial: {base_name}")
            print(f"  .log: {has_log}, .txt: {has_txt}, .json: {has_json}")
    
    if not incomplete_trials:
        print(f"✓ All trials complete ({len(base_names)} trials)")
    
    return incomplete_trials

# Check participant 00
validate_trial_files('run_artifacts/00')
```

### Common Issues

| Issue | Description | Solution |
|-------|-------------|----------|
| Missing `.txt` file | Log conversion not run | Run `log2txt.py` |
| Large file size | Very long trial duration | Normal variation, no action needed |
| Empty `.json` file | Trajectory export failure | Re-export from simulation |
| Corrupted `.log` | Simulation crash during recording | Cannot recover, trial should be excluded |

## Citation

If you use the run artifacts in your research, please cite:

```bibtex
[Citation information to be added]
```

## Related Documentation

- [Brief Introduction](../brief_introduction.md) - Experimental design and scenarios
- [Trial Assignment Matrix](../trials_info/README.md) - Which scenarios each participant completed
- [Data Processing Tools](../../../data_processing_tools/README.md) - How to process these files
- [Videos](../videos/download_link.md) - Synchronized video recordings

## Contact

For issues with run artifacts or data quality questions:
1. Check the [main dataset documentation](../../../README.md)
2. Review the processing pipeline in [data_processing_tools/](../../../data_processing_tools/)
3. Open an issue on the repository with:
   - Participant ID
   - Trial name
   - Specific file(s) affected
   - Error messages or unexpected behavior
