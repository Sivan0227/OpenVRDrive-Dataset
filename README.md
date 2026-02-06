# OpenVRDrive-Dataset

**OpenVRDrive-Dataset** is a comprehensive VR driving simulation dataset capturing Human-Driven Vehicle (HDV) behavior in mixed traffic flows with Connected and Automated Vehicles (CAVs). The dataset features **immersive VR driving experiments** with eye-tracking and **full-stack automated driving framework** supporting communication and cooperation within the platoon, enabling realistic HDV-CAV interaction studies in controlled yet naturalistic scenarios.

<img src="images/Demo.gif" width="70%">

*Platform Overview: From immersive VR driving experience to real-world simulator setup*

---

## Overview

The **OpenVRDrive-Dataset** is dedicated to facilitating community exploration of emerging HDV behaviors in mixed traffic flows via our VR-enabled, platoon-supported, human-in-the-loop simulation platform. By combining immersive virtual reality with realistic CAV platoon simulation, this platform enables controlled experiments that capture naturalistic driver responses to automated vehicles in safety-critical scenarios.

### What is OpenVRDrive?

OpenVRDrive is an integrated simulation platform that brings together:

- **Immersive VR Environment**: First-person driving experience with realistic vehicle controls and visual feedback
- **Eye-Tracking Integration**: Real-time gaze tracking to understand driver attention allocation
- **CAV Platoon Simulation**: Realistic automated vehicle behaviors with configurable control strategies
- **Mixed Traffic Scenarios**: Controllable interaction between human drivers and automated platoons
- **Multi-Modal Data Collection**: Synchronized capture of trajectories, control inputs, gaze data, and subjective assessments

### Purpose and Research Goals

This dataset aims to:

1. **Understand HDV-CAV Interaction Dynamics**: Capture how human drivers perceive, respond to, and interact with CAV platoons in various traffic scenarios
2. **Support Behavior Modeling**: Provide high-quality data for developing and validating driver behavior models in mixed traffic
3. **Enable Safety Analysis**: Facilitate risk assessment and safety evaluation of mixed-traffic scenarios
4. **Advance Control Strategies**: Help optimize CAV platoon control algorithms considering human driver behaviors
5. **Foster Open Research**: Establish a standardized, reproducible benchmark for the research community

## Platform Architecture

OpenVRDrive integrates multiple state-of-the-art open-source tools into a unified simulation platform:

![Platform Architecture](images/co-simulation.png)
*Figure: Technical integration architecture of simulation components*

### Core Components and Integration

```
┌─────────────────────────────────────────────────────────────────┐
│                    OpenVRDrive Platform                         │
└─────────────────────────────────────────────────────────────────┘
                               │
        ┌──────────────────────┼─────────────────────┐
        │                      │                     │
┌───────▼────────┐    ┌────────▼────────┐    ┌───────▼────────┐
│  CARLA 0.9.13  │    │  VR Interface   │    │  OpenCDA       │
│                │    │  + Eye Tracker  │    │                │
│ • 3D Rendering │◄───┤                 ├───►│ • CAV Control  │
│ • Physics Sim  │    │ • HTC Vive Pro  │    │ • Platoon Mgmt │
│ • Recorder     │    │ • Tobii Tracker │    │ • V2V Comm     │
└────────┬───────┘    └─────────────────┘    └────────┬───────┘
         │                                            │
         │            ┌─────────────────┐             │
         └───────────►│  SUMO Traffic   │◄────────────┘
                      │  • Flow Control │
                      │  • Routing      │
                      └─────────────────┘
```

#### 1. CARLA (Open Urban Driving Simulator)
- **Version**: 0.9.13
- **Role**: Core simulation engine providing 3D environment, physics, and rendering
- **Customizations**: 
  - 6-lane highway map with realistic textures
  - Vehicle models with accurate dynamics
  - Recorder module for precise playback

#### 2. VR Interface with Eye-Tracking
- **Base Framework**: [DReyeVR](https://github.com/HARPLab/DReyeVR) - VR driving simulation plugin for CARLA
- **Hardware**: HTC Vive Pro Eye headset with integrated Tobii eye tracker
- **Controls**: Logitech G29 steering wheel, pedals, and shifter
- **Capabilities**:
  - Stereoscopic 90Hz rendering for immersion
  - Real-time gaze tracking at 120Hz
  - Haptic feedback through force-feedback wheel
  - Natural head movements tracked
  - Seamless integration with CARLA for synchronized data recording

![DReyeVR VR Interface](images/DReyeVR_demo.gif)
*Figure: Immersive VR driving experience with real-time eye-tracking visualization*

#### 3. [OpenCDA](https://github.com/ucla-mobility/OpenCDA) (Cooperative Driving Automation)
- **Role**: Full-stack cooperative driving automation framework for CAV simulation
- **Key Features**:
  - Complete CDA pipeline: perception, localization, planning, control modules
  - CACC (Cooperative Adaptive Cruise Control) for platoon management
  - V2X communication protocols and cooperative perception
  - Modular design enabling customization of control strategies
  - Support for various cooperation levels between CAVs
  - Configurable platoon parameters (time gaps, speeds, platoon size)

![OpenCDA CAV Platoon](images/OpenCDA_demo.gif)
*Figure: CAV platoon with cooperative driving automation and V2X communication*

#### 4. SUMO (Simulation of Urban MObility)
- **Role**: Background traffic flow management
- **Integration**: Co-simulation with CARLA for realistic traffic density
- **Function**: Manages non-platoon vehicles following car-following models


### Current Release: Scenario 1 - HDV Cut-in Behavior

#### 📹 Experiment Demonstration Video

*Full Experimental Session Walkthrough** (Scenario 1): [Watch on YouTube](#)

The OpenVRDrive-Dataset is designed as an **expandable multi-scenario dataset series**. Each scenario focuses on a specific HDV-CAV interaction pattern, providing comprehensive multi-modal data following standardized formats.

**This release (v1.0) includes the first scenario:** HDV cut-in behavior, where human drivers merge into or cut in front of CAV platoons under different motivations and traffic conditions.

**Scenario 1 Contents:**
- **60 participants** (aged 21-58, mixed driving experience)
- **22 sub-scenarios** (14 discretionary + 8 mandatory lane changes)
- **960 experimental trials** (16 trials per participant)
- **Multi-modal synchronized data** (trajectories, eye-tracking, control inputs, questionnaires)

**Future Scenarios**: Additional HDV-CAV interaction scenarios are planned for future releases. Each new scenario will follow the same standardized data structure, ensuring consistency and compatibility across the entire dataset series.

![HDV Cut-in Scenario](images/DLC.gif)
*Figure: Example of HDV cutting into a CAV platoon in mixed traffic*

## Standardized Data Package

Each scenario in OpenVRDrive-Dataset follows a standardized structure, ensuring consistency and reproducibility across different experimental conditions.

### Data Components (Per Scenario)

Every scenario folder contains the following standardized data types:

#### 1. **CARLA Scenario Packages** (`carla_package/`)
Pre-compiled CARLA packages enabling researchers to:
- Rapidly visualize experimental scenarios
- Replay simulation runs with original physics
- Verify data accuracy through visual inspection

**Contents**: Map files, vehicle blueprints, weather configurations

#### 2. **Participant Demographics** (`questionnaires/`)
Fully anonymized demographic information including:
- Age range grouping
- Driving experience levels
- Annual mileage categories
- Prior AV exposure

**Privacy**: All personally identifiable information removed

**Format**: Excel files with anonymized participant information

#### 3. **Experimental Parameters** (`trials_info/`)
Randomized parameter sequences for each participant:
- Trial assignment matrices
- Scenario parameter combinations (speed, time gap, platoon size)
- Randomization orders

**Format**: JSON configuration files with complete parameter dictionaries

#### 4. **Subjective Questionnaires** (`questionnaires/`)
Participant responses to validated assessment instruments:
- **SSQ** (Simulation Sickness Questionnaire): Motion sickness levels
- **PEQ** (Perception Evaluation Questionnaire): Subjective risk and comfort
- **SRQ** (Simulation Realism Questionnaire): Scenario fidelity assessment

**Format**: Excel files with Likert-scale responses and derived scores

#### 5. **Behavioral Data** (`run_artifacts/`)
High-resolution multi-modal behavioral data for each trial:

**Vehicle Trajectories** (10Hz sampling):
- Position (x, y, z) for all vehicles
- Velocity and acceleration vectors
- Heading angles and lane positions

**Ego Vehicle Control Inputs** (10Hz):
- Steering angle (-1 to +1)
- Throttle position (0 to 1)
- Brake pressure (0 to 1)
- Gear state and turn signals

**Eye-Tracking Data** (10Hz):
- Gaze direction (yaw, pitch)
- Pupil diameter (left/right eyes)
- Eye openness validity flags
- Fixation and saccade events

**Format**: JSON files with synchronized timestamps

#### 6. **Simulation Logs** (`run_artifacts/`)
Raw CARLA recorder logs for precise reproduction:
- Complete simulation state at each frame
- Actor spawning and destruction events
- Physics parameters and collision data
- Weather and lighting conditions

**Usage**: Can be replayed in CARLA for exact scenario reconstruction

#### 7. **Video Recordings** (`videos/`)
First-person perspective videos from driver's viewpoint:
- 1920×1080 resolution at 30fps
- H.264 encoded MP4 format
- Audio included (most trials)
- Synchronized with behavioral data via timestamps

### Data Standardization Benefits

✓ **Reproducibility**: Complete parameter documentation enables exact replication  
✓ **Interoperability**: Standard formats (JSON, CSV, MP4) work with common tools  
✓ **Extensibility**: New scenarios follow the same structure for easy integration  
✓ **Traceability**: Raw logs allow verification of processed data  
✓ **Multi-Modal Fusion**: Synchronized timestamps enable cross-modal analysis

## Data Processing Tools

To facilitate dataset usage, we provide a comprehensive suite of Python-based processing tools in the `data_processing_tools/` directory.

### Key Features

**Automated Pipeline**:
```
Raw Logs (.log) → Parsed Data (.txt, .json) → Integrated Dataset → Analysis-Ready Format
```

**Core Tools**:
- **`log2txt.py`**: Convert CARLA binary logs to human-readable text format
- **`config_loader.py`**: Centralized configuration management for multi-scenario support
- **`single_exp_data_intergrate.py`**: Merge trajectory and eye-tracking data for single trials
- **`intergrate_all.py`**: Aggregate all participants into unified JSON dataset
- **`src/parser.py`**: Parse VR recording files with eye-tracking data
- **`src/visualizer.py`**: Generate publication-quality plots and visualizations

### Quick Start

```python
# Load and process a single trial
from single_exp_data_intergrate import SingleExpDataIntergrate

integrator = SingleExpDataIntergrate(
    traj_data_path='run_artifacts/00/discretionary_[72, 0.6, 64.8, 7].json',
    vr_data_path='run_artifacts/00/discretionary_[72, 0.6, 64.8, 7].txt'
)
result = integrator.run()

# Access integrated data
print(f"VR vehicle ID: {result['vr_id']}")
print(f"Eye tracking samples: {len(result['all_veh_info'][result['vr_id']]['LEFTPupilDiameter'])}")
```

### Capabilities

- **Multi-scenario support**: Automatically detects and loads configuration for different scenarios
- **Time synchronization**: Aligns high-frequency eye-tracking with lower-frequency trajectory data
- **Data validation**: Built-in checks for completeness and consistency
- **Visualization suite**: Pre-configured plots for common analysis tasks
- **Batch processing**: Tools for processing entire participant datasets

📖 **See [data_processing_tools/README.md](data_processing_tools/README.md) for detailed documentation and examples**

## Dataset Structure

The dataset is organized by scenarios, with each scenario folder containing:

```
OpenVRDrive-Dataset/
├── README.md
├── LICENSE
├── data_processing_tools/              # Python tools for data processing and analysis
│   ├── README.md                       # Tool documentation and examples
│   ├── config_loader.py                # Multi-scenario configuration system
│   ├── log2txt.py                      # CARLA log converter
│   ├── single_exp_data_intergrate.py   # Single trial integrator
│   ├── single_person_data_intergrate.py # Participant-level processor
│   ├── all_person_data_intergrate.py   # Batch processor
│   ├── intergrate_all.py               # Dataset aggregator
│   ├── convert.py                      # Conversion pipeline
│   ├── example.py                      # Visualization examples
│   └── src/                            # Core modules
│       ├── parser.py                   # VR data parser
│       ├── visualizer.py               # Plotting utilities
│       └── utils.py                    # Helper functions
├── scenario1-HDV cuts into a CAV Platoon/
│   ├── brief_introduction.md           # Scenario-specific documentation
│   ├── carla_package/                  # Pre-compiled CARLA package
│   │   └── download_link.md            # Package download link
│   ├── questionnaires/                 # Questionnaire data and templates
│   │   ├── README.md                   # Questionnaire documentation
│   │   ├── demographics_data.xlsx      # Participant demographics
│   │   ├── PEQ_SSQ_data.xlsx          # Perception & sickness data
│   │   ├── SRQ_data.xlsx              # Realism evaluation
│   │   ├── *.pdf                       # Questionnaire templates (English)
│   │   └── questionnaire_in_chinese/   # Chinese versions
│   ├── run_artifacts/                  # Experimental data files
│   │   └── download_link.md            # Data download instructions
│   ├── trials_info/                    # Trial design and assignments
│   │   ├── README.md                   # Assignment matrix documentation
│   │   ├── scenario1_trial_params.json # Parameter configurations
│   │   ├── experiment_guide.pdf        # Pre-experiment instructions (EN)
│   │   └── experiment_guide_chinese.pdf # Pre-experiment instructions (CN)
│   └── videos/                         # First-person video recordings
│       └── download_link.md            # Video download link
└── [Additional scenarios...]
```

## Data Format

All data files use standard formats for easy processing:

- **CSV files**: Time-series vehicle trajectory data, synchronized at 10Hz
- **JSON files**: Structured metadata, event logs, and configuration files
- **MP4/AVI files**: Video recordings from multiple camera angles
- **Excel/CSV files**: Questionnaire responses and participant demographics

### Common Data Fields

**Vehicle Trajectory Data:**
- Timestamp
- Vehicle ID
- Position (x, y, z coordinates)
- Velocity (vx, vy, vz)
- Acceleration (ax, ay, az)
- Heading angle
- Lane ID

**Gaze Tracking Data:**
- Timestamp
- Gaze direction (pitch, yaw)
- Pupil diameter
- Fixation points
- Saccade events

**Control Inputs:**
- Timestamp
- Steering angle
- Throttle position (0-1)
- Brake pressure (0-1)
- Turn signal status

## Data Processing Tools

The `data_processing_tools/` directory contains Python scripts to help users work with the dataset:

- **`parser.py`**: Parse and load raw simulation log files
- **`visualizer.py`**: Generate visualizations of trajectories and behavior metrics
- **`utils.py`**: Utility functions for data cleaning and transformation
- **Example notebooks**: Jupyter notebooks demonstrating common analysis tasks

See the [data_processing_tools/README.md](data_processing_tools/README.md) for detailed usage instructions.


## Potential Applications

This dataset can support various research directions:

- **Driver Behavior Modeling**: Develop and validate microscopic traffic models
- **Machine Learning**: Train models for intention prediction and trajectory forecasting
- **Human-Automation Interaction**: Analyze driver adaptation to automated vehicles
- **Traffic Safety**: Evaluate collision risks in mixed traffic scenarios
- **Control Strategy Design**: Test and optimize CAV platoon control algorithms
- **Cognitive Analysis**: Study driver attention allocation and decision-making


**Note**: The associated research paper is currently under review. Please check back for updates on the publication status and complete citation information.

## Download

**Total Dataset Size**: Approximately [X] GB (uncompressed)

### Current Release: Scenario 1 Data

All data files for **Scenario 1 (HDV Cuts into a CAV Platoon)** are available through the links below. Each data component is hosted on both Google Drive and Baidu Netdisk (百度网盘) for accessibility.

### Quick Access Links (Scenario 1)

- **📊 [Run Artifacts (Experimental Data)](scenario1-HDV%20cuts%20into%20a%20CAV%20Platoon/run_artifacts/download_link.md)** - Trajectory, eye-tracking, and control data
- **🚗 [CARLA Package](scenario1-HDV%20cuts%20into%20a%20CAV%20Platoon/carla_package/download_link.md)** - Pre-configured simulation environment
- **🎥 [Video Recordings](scenario1-HDV%20cuts%20into%20a%20CAV%20Platoon/videos/download_link.md)** - First-person perspective videos
- **📋 [Questionnaires & Demographics](scenario1-HDV%20cuts%20into%20a%20CAV%20Platoon/questionnaires/README.md)** - Subjective assessments and participant data

**Note**: Each download page provides both Google Drive and Baidu Netdisk links for your convenience.

## Related Publications

## Contact

For questions, issues, or collaboration inquiries:

- **Email**: sivanliu@seu.edu.cn
- **Primary Institution**: School of Transportation, Southeast University, China
- **Collaborating Institution**: School of Civil and Environmental Engineering, Nanyang Technological University, Singapore

## License

This dataset is released under [specify license type]. Please see the [LICENSE](LICENSE) file for complete terms and conditions.

**Key Terms:**
- Free for academic and research purposes
- Commercial use requires separate permission
- Proper attribution required
- No redistribution of raw data without permission


## Contributors

OpenVRDrive-Dataset is mainly supported by the School of Transportation at Southeast University.

### Lab Principal Investigator:

- Prof. Zhibin Li ([Southeast University])

### Project Lead:

- Bowen Liu

### Team Members:

- Shenlingrui Yang
- Hao Li
- Di Han
- Yutong Wang

### External Contributor Acknowledgements

We would like to acknowledge the great contributions from Nanyang Technological University (NTU), particularly:
- **Prof. Feng Zhu**: Co-supervision and technical guidance throughout the research
- **Dr. Meng Li**: Data analysis methodology

We gratefully acknowledge:
- All 60 participants who volunteered their time
- Technical support from the CARLA, OpenCDA, and SUMO communities
---

For more questions, please refer to individual scenario documentation or contact us directly.
