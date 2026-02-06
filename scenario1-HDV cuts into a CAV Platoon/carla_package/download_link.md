# CARLA Package - VR Highway Scenario

## Download

**Download Links:**
- **Google Drive**: [Download from Google Drive](https://drive.google.com/file/d/1Se2j7YQu1jHio4xfEHJAiQx7-7JDtUMP/view?usp=drive_link)
- **Baidu Netdisk** (百度网盘): [下载链接](#) | 提取码: [XXXX]

**Version**: CARLA 0.9.13 with `vr_wider` map

---

This directory contains a pre-configured CARLA package specifically designed for the HDV cut-in experiments. The package includes a custom highway map and is ready to use for visualizing and replaying experimental trials.

## Package Contents

- **Custom Map**: `vr_wider.map` - A 6-lane highway environment designed for VR driving experiments
- **Default Configuration**: Map is pre-set as default - opens automatically when launching CARLA
- **Vehicle Blueprints**: Pre-configured vehicle models used in experiments
- **Weather Presets**: Daytime clear weather conditions matching experimental setup

## Map Features: vr_wider.map

The `vr_wider.map` is a custom CARLA map built for mixed traffic experiments:

**Highway Specifications:**
- **Lanes**: 6 lanes (3 lanes per direction)
- **Lane Width**: 3.5 meters (standard highway width)
- **Length**: Extended straight section for sustained lane-change scenarios
- **Environment**: Realistic highway textures and markings
- **Lighting**: Optimized for VR rendering at 90Hz

**Design Optimizations:**
- Wide lanes accommodate platoon formations and lane changes
- Minimal curves for consistent speed maintenance
- Clear lane markings for visual guidance
- Reduced decorative elements to maintain VR performance

## Installation

### Prerequisites

- **Operating System**: Windows 10/11
- **Python**: Version 3.7
- **Hardware**: GPU recommended for smooth visualization

### Setup Instructions

This package includes a **pre-configured CARLA 0.9.13 installation** with the custom `vr_wider.map` already set as default. Simply extract the package and run `CarlaUE4.exe` to launch. The map will load automatically.

For detailed usage instructions, refer to the [CARLA Quick Start Guide](https://carla.readthedocs.io/en/latest/start_quickstart/).

## Replaying Experimental Trials

You can replay any experimental trial using the log files from the `run_artifacts/` directory. CARLA's replay system reconstructs the exact simulation state, allowing visualization from any viewpoint.

### Basic Replay

**Step 1: Start CARLA Server**
```bash
# In the extracted carla_package directory
CarlaUE4.exe -quality-level=Epic
```

**Step 2: Replay a Log File**
```bash
# In a new terminal, navigate to PythonAPI examples
cd carla_package/PythonAPI/examples/

# Replay a specific trial
python start_replaying.py -f /path/to/run_artifacts/00/discretionary_[72, 0.6, 64.8, 7].log
```

**Alternative: Using Python API**
```python
import carla

# Connect to CARLA
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# Replay the recording
log_file = '/path/to/run_artifacts/00/discretionary_[72, 0.6, 64.8, 7].log'
client.replay_file(log_file, 0, 0, 0)  # (filename, start_time, duration, follow_id)
```

### Advanced Replay Options

#### 1. Follow Specific Vehicle (Ego Vehicle)

```bash
# Replay and follow the VR-controlled vehicle (ID varies by trial)
python start_replaying.py -f trial.log --follow 123
```

To find the ego vehicle ID:
```bash
# Show all actors in the recording
python show_recorder_file_info.py -f trial.log -a
# Look for the vehicle with role_name "ego_vehicle" or if_vr: true
```

#### 2. Camera Control During Replay

**Free Camera Mode** (default):
- WASD: Move camera
- Mouse: Rotate view
- Mouse Wheel: Zoom in/out
- Q/E: Move up/down

**Attached Camera Mode**:
```python
import carla

client = carla.Client('localhost', 2000)
world = client.get_world()

# Start replay
client.replay_file('trial.log', 0, 0, 0)

# Attach camera to ego vehicle after replay starts
ego_vehicle = world.get_actor(123)  # Replace with actual ego ID
spectator = world.get_spectator()

# Follow from behind
transform = carla.Transform(
    ego_vehicle.get_location() + carla.Location(x=-5, z=2),
    ego_vehicle.get_transform().rotation
)
spectator.set_transform(transform)
```

#### 3. Time Control

```python
# Start replay at 10 seconds into the recording
client.replay_file('trial.log', 10.0, 0, 0)

# Replay only 30 seconds of duration
client.replay_file('trial.log', 0, 30.0, 0)

# Start at 10s and play for 30s
client.replay_file('trial.log', 10.0, 30.0, 0)
```

## Viewing Recording Information

### Summary Information

```bash
cd $CARLA_ROOT/PythonAPI/examples/

# Show basic recording info
python show_recorder_file_info.py -f /path/to/trial.log -s
```

**Output Example**:
```
Version: 1
Map: vr_wider
Date: 2024-04-03 15:26:00
Duration: 45.5 seconds
Frames: 2365
Total Size: 474 KB
```

### Detailed Actor Information

```bash
# Show all actors (vehicles) in the recording
python show_recorder_file_info.py -f /path/to/trial.log -a > actors.txt
```

**Output includes**:
- Actor ID and type
- Role name (ego_vehicle, autopilot, etc.)
- Spawn and destroy times
- Complete trajectory data

### Frame-by-Frame Data

```bash
# Export complete frame-by-frame data
python show_recorder_file_info.py -f /path/to/trial.log -a > full_recording.txt
```

This generates a human-readable text file containing:
- Frame timestamps
- All actor positions and rotations
- Physics states (velocity, acceleration)
- Control inputs (for ego vehicle)

## Recording New Experiments

If you want to run new experiments using this map:

### Basic Recording

```bash
cd $CARLA_ROOT/PythonAPI/examples/

# Start CARLA with no extra agents, begin recording
python start_recording.py -n 0 -f my_experiment.log

# Your experiment code runs here...

# Stop recording with Ctrl+C
```

### Recording with Custom Agents

```python
import carla

client = carla.Client('localhost', 2000)
world = client.get_world()

# Start recording
client.start_recorder("my_experiment.log")

# Spawn vehicles, run experiment...
# Your experiment code here

# Stop recording
client.stop_recorder()
```

## Integration with ScenarioRunner

For automated scenario execution:

```bash
cd $SCENARIO_RUNNER_ROOT

# Run a scenario and record
./run_experiment.py \
    --title hdv_cutin_experiment \
    --route srunner/data/routes_debug.xml \
           srunner/data/all_towns_traffic_scenarios1_3_4.json 0 \
    --output \
    --reloadWorld
```

**Note**: ScenarioRunner integration requires additional configuration. See CARLA ScenarioRunner documentation for details.

## Extracting Data from Recordings

### Convert to Human-Readable Format

The `log2txt.py` tool in `data_processing_tools/` converts binary logs to text:

```bash
cd data_processing_tools

# Convert a single log file
python log2txt.py --data-dir ../scenario1-HDV\ cuts\ into\ a\ CAV\ Platoon/run_artifacts/00
```

This generates `.txt` files that can be parsed for analysis.

### Extract Trajectories

```bash
cd $CARLA_ROOT/PythonAPI/examples/

# Show only trajectory data
python show_recorder_file_info.py -f trial.log -a | grep "Location:" > trajectories.txt
```

## Troubleshooting

### Issue: Map Doesn't Load

**Solution**: Ensure the package was extracted to the correct CARLA root directory:
```bash
ls $CARLA_ROOT/CarlaUE4/Content/Carla/Maps/vr_wider.umap
```

### Issue: Replay File Not Found

**Error**: `RuntimeError: unable to open file for reading`

**Solution**: Use absolute paths for log files:
```bash
# Get absolute path
realpath run_artifacts/00/trial.log

# Use in replay command
python start_replaying.py -f /full/path/to/trial.log
```

### Issue: Low Frame Rate During Replay

**Solution**: Reduce graphics quality:
```bash
CarlaUE4.exe -quality-level=Low
```

Or disable rendering in headless mode:
```bash
CarlaUE4.exe -RenderOffScreen
```

### Issue: Wrong Vehicles Appear

**Problem**: Replay shows different vehicle models than experiments

**Solution**: Ensure you're using CARLA 0.9.13. Vehicle blueprints changed between versions.

## Performance Tips

- **Replay Speed**: Normal replay is 1x speed. Cannot be adjusted directly.
- **Recording Size**: Typical 60-second trial = 400-600 KB
- **Memory Usage**: ~2 GB RAM for replay
- **GPU Usage**: Rendering quality affects GPU load

## Related Documentation

- [CARLA Official Documentation](https://carla.readthedocs.io/)
- [CARLA Recorder Documentation](https://carla.readthedocs.io/en/0.9.13/adv_recorder/)
- [Run Artifacts README](../run_artifacts/download_link.md) - Log file descriptions
- [Data Processing Tools](../../../data_processing_tools/README.md) - How to process recordings

## Version Compatibility

| Component | Required Version |
|-----------|------------------|
| CARLA | 0.9.13 |
| Python | 3.7 |
| pygame | 2.0.1+ |
| numpy | 1.19+ |
| OS | Windows 10/11 |

**Warning**: Using different CARLA versions may result in incompatible replay files or missing map assets.

## Contact

For issues with the CARLA package or map files:
- Check the main [dataset README](../../../README.md)
- Verify CARLA installation: [CARLA Quick Start](https://carla.readthedocs.io/en/0.9.13/start_quickstart/)
- Open an issue with your CARLA version and error logs
