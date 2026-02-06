# Video Recordings

## Download

**Download Links:**
- **Google Drive**: [Download from Google Drive](#)
- **Baidu Netdisk** (百度网盘): [下载链接](#) | 提取码: [XXXX]

---

## Overview

This folder contains first-person perspective video recordings from the VR driving experiments. All videos were captured from the driver's viewpoint inside the vehicle, showing the highway environment, surrounding traffic (CAV platoon and other HDVs), and the driver's lane-change maneuvers.

## Video Examples

### Discretionary Lane Change (DLC)

The following animation shows a typical discretionary lane-change scenario where the human driver voluntarily cuts into the CAV platoon from the adjacent lane.

![DLC Example](../images/DLC.gif)

**Key Features:**
- Driver initiates lane change from right lane into CAV platoon
- CAVs automatically adjust spacing and speed to accommodate
- No external forcing factors (e.g., work zone)
- Driver has freedom to choose timing and gap selection

### Mandatory Lane Change (MLC)

The following animation shows a mandatory lane-change scenario where the driver must merge into the CAV platoon due to a work zone blocking the current lane.

![MLC Example](../images/MLC.gif)

**Key Features:**
- Work zone forces driver to change lanes
- Limited time window for gap selection
- Higher urgency compared to DLC scenarios
- Driver must adapt to available gaps in platoon

## Video Specifications

- **Recording Device**: HTC Vive Pro VR headset with DreyeVR integration
- **Video Format**: MP4 (H.264 encoding)
- **Resolution**: 1920×1080 pixels
- **Frame Rate**: 30 fps
- **Field of View**: First-person driver perspective
- **Duration**: Variable (typically 30-120 seconds per trial)
- **Audio**: Included in most videos (some audio tracks removed due to background noise)

## Video Content

Each video recording includes:

1. **Highway Environment**
   - 6-lane highway with realistic textures
   - Lane markings and road signs
   - Environmental lighting (daytime conditions)

2. **Traffic Composition**
   - 7-vehicle CAV platoon in middle lane (or traditional HDV traffic)
   - Ego HDV (driver's vehicle)
   - One additional trailing HDV
   - Other background traffic vehicles

3. **Driver Actions**
   - Steering inputs
   - Acceleration/braking behaviors
   - Lane-change maneuvers
   - Gap acceptance decisions

4. **CAV Platoon Behavior** (for mixed traffic scenarios)
   - Automatic speed adjustments
   - Time gap maintenance
   - Cooperative responses to HDV intrusion

## File Organization

Videos are organized by participant folders with systematic file naming:

```
videos/
├── 00/
│   ├── 00_dlc_00.mp4
│   ├── 00_dlc_01.mp4
│   ├── 00_dlc_02.mp4
│   ├── ...
│   ├── 00_dlc_12.mp4
│   ├── 00_dlc_13.mp4
│   ├── 00_mlc_01.mp4
│   ├── 00_mlc_02.mp4
│   ├── ...
│   ├── 00_mlc_06.mp4
│   └── 00_mlc_07.mp4
├── 01/
│   ├── 01_dlc_01.mp4
│   ├── ...
│   └── 01_mlc_07.mp4
├── 02/
│   └── ...
├── ...
└── 59/
    ├── 59_dlc_...mp4
    └── 59_mlc_...mp4
```

**Directory Structure:**
- Each participant has a separate folder named by their ID (00-59)
- Within each folder, videos follow the naming convention: `XX_[dlc|mlc]_YY.mp4`

**Naming Convention:** `XX_[dlc|mlc]_YY.mp4`
- `XX`: Participant ID (00-59)
- `dlc` or `mlc`: Lane-change type (Discretionary or Mandatory)
- `YY`: Scenario ID (00-13 for DLC, 00-07 for MLC)

**Examples:**
- `00/00_dlc_00.mp4` - Participant 00, DLC Mixed Scenario 0
- `00/00_dlc_12.mp4` - Participant 00, DLC Traditional Scenario 12
- `00/00_mlc_01.mp4` - Participant 00, MLC Mixed Scenario 1
- `00/00_mlc_06.mp4` - Participant 00, MLC Traditional Scenario 6

**Note:** Not all participants have all scenario videos. Each participant completed only 16 out of 22 scenarios. Refer to [trials_info/README.md](../trials_info/README.md) for the complete trial assignment matrix showing which scenarios each participant completed.

## Download

**Full Video Dataset:**

https://drive.google.com/drive/folders/1kNBfQqfUy5rppLzUsyBjeCDs8ejb-bLU?usp=share_link


**Note:** Due to the large file size, videos are hosted on Google Drive. Please ensure sufficient storage space before downloading.

## Usage Recommendations

**For Qualitative Analysis:**
- Review driver behavior patterns and strategies
- Identify critical lane-change moments
- Observe CAV platoon responses
- Study gap selection decisions

**For Machine Learning:**
- Extract frames for computer vision models
- Train driver behavior prediction models
- Develop lane-change intention recognition algorithms
- Analyze time-series patterns

**For Visualization:**
- Create demonstration videos for presentations
- Generate animated figures for publications
- Produce educational materials


## Contact

For questions about video recordings or access issues, please refer to the main dataset documentation or contact the research team.