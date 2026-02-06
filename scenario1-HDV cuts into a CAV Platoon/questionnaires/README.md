# Questionnaire Data

## Overview

This folder contains all questionnaire-related data from Scenario 1 experiments, including participant demographics, subjective assessments, and questionnaire templates. All participant information has been fully anonymized to protect privacy.

## Data Files

### 1. demographics_data.xlsx

Anonymized participant demographic information collected before the experiment:

**Included Variables:**
- Participant ID (anonymized, 0-59)
- Age range grouping
- Gender
- Driving experience (years)
- Annual mileage categories
- Prior exposure to automated vehicles
- Education level

**Privacy Protection:** All personally identifiable information (names, contact information, specific birth dates) has been removed.

**Format:** Excel file with one row per participant (N=60)

### 2. PEQ_SSQ_data.xlsx

Combined data from two post-trial questionnaires:

#### Perception Evaluation Questionnaire (PEQ)
Subjective assessments of each trial, measuring:
- **Perceived Risk**: How dangerous the scenario felt
- **Comfort Level**: Driver's comfort during the maneuver
- **Platoon Perception**: Awareness and understanding of CAV platoon behavior
- **Scenario Difficulty**: Task complexity rating

**Administered:** After each of the 16 trials per participant

#### Simulation Sickness Questionnaire (SSQ)
Standard VR sickness assessment measuring:
- **Nausea**: General discomfort, stomach awareness, increased salivation
- **Oculomotor**: Eye strain, difficulty focusing, blurred vision
- **Disorientation**: Dizziness, vertigo, balance issues

**Administered:** At three time points per participant:
- Pre-experiment baseline
- Mid-session (after 8 trials)
- Post-experiment

**Format:** Excel file with multiple sheets for PEQ and SSQ responses

### 3. SRQ_data.xlsx

Simulation Realism Questionnaire (SRQ) responses assessing the fidelity of the VR driving experience:

**Measured Dimensions:**
- **Visual Realism**: Graphics quality, environment detail
- **Behavioral Realism**: Vehicle dynamics, traffic behavior
- **Control Realism**: Steering wheel, pedals responsiveness
- **Physical Realism**: Motion cues, sense of speed
- **Overall Fidelity**: General immersion and believability

**Administered:** Once per participant at the end of the experiment session

**Scale:** 7-point Likert scale (1 = Not realistic at all, 7 = Extremely realistic)

**Format:** Excel file with participant-level summary scores

## Questionnaire Templates (PDF)

### English Versions

#### demographics_questionnaire.pdf
Blank demographic survey form used for data collection. Contains questions about:
- Age, gender, education
- Driving experience and habits
- Technology familiarity
- Prior VR/AV experience

#### perception_evaluation_questionnaire_PEQ_and_simulation_sickness_questionnaires_SSQ.pdf
Combined questionnaire booklet including:
- **PEQ Items**: 8 questions per trial (repeated 16 times)
- **SSQ Items**: Standard SSQ-16 items (administered 3 times per session)

#### simulation_realism_questionnaires_SRQ.pdf
End-of-session questionnaire evaluating:
- Realism across multiple dimensions
- Comparison to real-world driving
- Suggestions for improvement

### Chinese Versions (`questionnaire_in_chinese/`)

Identical questionnaires translated to Chinese for participants more comfortable with Chinese language:

1. **驾驶模拟实验-驾驶员基本信息了解.pdf**  
   (Demographic Information Questionnaire - Chinese)

2. **驾驶模拟实验-驾驶员不良反应评估.pdf**  
   (Simulation Sickness Questionnaire - Chinese)

3. **驾驶模拟实验-驾驶员对驾驶模拟体验评价.pdf**  
   (Perception & Realism Evaluation - Chinese)

**Note:** Chinese versions were provided to ensure comprehension across all participants in the predominantly Chinese-speaking sample.

## Data Usage Notes

### Statistical Analysis

**Sample Size:**
- N = 60 participants for demographics and SRQ
- N = 960 trials for PEQ (60 participants × 16 trials)
- N = 180 SSQ measurements (60 participants × 3 time points)

### Recommended Applications

1. **Demographic Analysis**: Characterize sample representativeness, control for confounding variables
2. **Subjective Risk Assessment**: Correlate perceived risk with objective safety metrics
3. **Simulator Validation**: Use SRQ scores to assess ecological validity
4. **Motion Sickness Analysis**: SSQ data for VR usability evaluation
5. **Human Factors Research**: Link subjective assessments to behavioral outcomes

### Data Integrity

- All questionnaires were administered by trained research assistants
- Responses were checked for completeness during data entry
- Missing data is marked explicitly (if any)
- Quality checks performed to identify inconsistent responses

## Privacy and Ethics

- This study was approved by the Institutional Review Board at Southeast University
- All participants provided informed consent before participation
- Demographic data has been aggregated into ranges to prevent re-identification
- No personally identifiable information is included in this public release

## Related Documentation

- [Main Scenario Description](../brief_introduction.md): Experimental procedures and design
- [Dataset Structure](../../README.md): Overview of all data components
- [Trial Information](../trials_info/README.md): Scenario assignment details

## Contact

For questions about questionnaire design, data interpretation, or access to additional materials, please contact the research team at sivanliu@seu.edu.cn
