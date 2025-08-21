# BeyondMimic Motion Tracking Code

[![IsaacSim](https://img.shields.io/badge/IsaacSim-4.5.0-silver.svg)](https://docs.omniverse.nvidia.com/isaacsim/latest/overview.html)
[![Isaac Lab](https://img.shields.io/badge/IsaacLab-2.1.0-silver)](https://isaac-sim.github.io/IsaacLab)
[![Python](https://img.shields.io/badge/python-3.10-blue.svg)](https://docs.python.org/3/whatsnew/3.10.html)
[![Linux platform](https://img.shields.io/badge/platform-linux--64-orange.svg)](https://releases.ubuntu.com/20.04/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/license/mit)

[[Website]](https://beyondmimic.github.io/)
[[Arxiv]](https://arxiv.org/abs/2508.08241)
[[Video]](https://youtu.be/RS_MtKVIAzY)

## 🚀 Overview

BeyondMimic is a versatile humanoid control framework that provides highly dynamic motion tracking with state-of-the-art motion quality on real-world deployment and steerable test-time control with guided diffusion-based controllers.

This repository covers the **motion tracking training** component of BeyondMimic. **After adaptive sampling is added, you should be able to train any sim-to-real-ready motion in the LAFAN1 dataset without tuning any parameters**.

## ✨ Features

- 🎯 **High-Quality Motion Tracking**: State-of-the-art motion imitation quality
- 🤖 **Multi-Robot Support**: Compatible with Unitree G1 and other humanoid robots
- 🔄 **Adaptive Sampling**: Intelligent motion processing pipeline
- 💾 **Local Workflow**: Complete offline processing without external dependencies
- 🚀 **Sim-to-Real Ready**: Optimized for real-world deployment
- 📁 **Flexible Data Management**: Support for local NPZ files and direct model paths

## 📋 TODO List

- [ ] **Adaptive Sampling**: Fixing bugs from numerical issues
- [ ] **Deployment**: Will be available in another repository

## 🛠️ Installation

### Prerequisites

- **Isaac Lab v2.1.0**: Follow the [installation guide](https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/index.html)
- **Python 3.10**: Required for compatibility
- **Linux 64-bit**: Ubuntu 20.04+ recommended

### Step-by-Step Setup

1. **Clone Repository**
   ```bash
   # Option 1: SSH
   git clone git@github.com:HybridRobotics/whole_body_tracking.git
   
   # Option 2: HTTPS
   git clone https://github.com/HybridRobotics/whole_body_tracking.git
   ```

2. **Download Robot Assets**
   ```bash
   cd whole_body_tracking
   
   # Download and extract robot description files
   curl -L -o unitree_description.tar.gz \
     https://storage.googleapis.com/qiayuanl_robot_descriptions/unitree_description.tar.gz
   
   tar -xzf unitree_description.tar.gz -C source/whole_body_tracking/whole_body_tracking/assets/
   rm unitree_description.tar.gz
   ```

3. **Install Library**
   ```bash
   # Using Python interpreter with Isaac Lab installed
   python -m pip install -e source/whole_body_tracking
   ```

## 🎭 Motion Tracking Workflow

### 1. Motion Preprocessing (Local)

We support local motion processing without requiring WandB. **Note**: Reference motions should be retargeted and use generalized coordinates only.

#### Available Datasets

- **LAFAN1 Dataset**: Available on [HuggingFace](https://huggingface.co/datasets/lvhaidong/LAFAN1_Retargeting_Dataset)
- **Sidekicks**: From [KungfuBot](https://kungfu-bot.github.io/)
- **Cristiano Ronaldo Celebration**: From [ASAP](https://github.com/LeCAR-Lab/ASAP)
- **Balance Motions**: From [HuB](https://hub-robot.github.io/)

#### Convert Motions (Local Mode)

```bash
# Convert CSV to NPZ with local saving (no WandB required)
python scripts/csv_to_npz.py \
  --input_file {motion_name}.csv \
  --input_fps 30 \
  --output_name {motion_name} \
  --save_to assets/motions/{motion_name}.npz \
  --no_wandb \
  --headless
```

This saves the processed motion locally as NPZ files.

#### Test Motion Replay (Local)

```bash
# Verify motion files work locally
python scripts/replay_npz.py \
  --motion_file assets/motions/{motion_name}.npz \
  --headless
```

### 2. Policy Training (Local)

```bash
python scripts/rsl_rl/train.py \
  --task=Tracking-Flat-G1-v0 \
  --motion_file assets/motions/{motion_name}.npz \
  --headless
```

### 3. Policy Evaluation (Local)

```bash
python scripts/rsl_rl/play.py \
  --task=Tracking-Flat-G1-v0 \
  --motion_file assets/motions/{motion_name}.npz \
  --load_run {experiment_timestamp} \
  --checkpoint {checkpoint_number} \
  --num_envs 2 \
  --headless
```

**Note**: Checkpoint information can be found in `logs/rsl_rl/{task_name}/{timestamp}/`

### 4. Advanced: Direct Model Path

For more control, you can directly specify the model file path:

```bash
python scripts/rsl_rl/play.py \
  --task=Tracking-Flat-G1-v0 \
  --motion_file assets/motions/{motion_name}.npz \
  --model_path logs/rsl_rl/{task_name}/{timestamp}/model_{checkpoint}.pt \
  --num_envs 2 \
  --headless
```

## 🏗️ Code Structure

```
whole_body_tracking/
├── source/whole_body_tracking/
│   ├── tasks/tracking/
│   │   ├── mdp/                    # MDP definition components
│   │   │   ├── commands.py         # Motion commands & error computation
│   │   │   ├── rewards.py          # DeepMimic reward functions
│   │   │   ├── events.py           # Domain randomization
│   │   │   ├── observations.py     # Observation definitions
│   │   │   └── terminations.py     # Early termination logic
│   │   ├── config/g1/              # G1 robot configuration
│   │   └── tracking_env_cfg.py     # Environment hyperparameters
│   └── robots/                     # Robot-specific settings
├── scripts/                         # Utility scripts
│   ├── csv_to_npz.py              # Motion preprocessing
│   ├── train.py                    # Policy training
│   ├── play.py                     # Policy evaluation
│   └── replay_npz.py              # Motion replay
└── assets/                         # Robot descriptions & motions
```

### Key Components

- **`commands.py`**: Motion commands, error calculations, adaptive sampling
- **`rewards.py`**: DeepMimic reward functions with smoothing
- **`events.py`**: Domain randomization for robustness
- **`observations.py`**: Motion tracking observations
- **`terminations.py`**: Early termination and timeout logic

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for more details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LAFAN1 Dataset**: For motion data
- **KungfuBot**: For sidekick motions and inspiration
- **ASAP**: For celebration motions
- **HuB**: For balance motions
- **Isaac Sim**: For simulation environment
- **RSL-RL**: For reinforcement learning framework

## 📞 Contact

For questions and support, please open an issue on GitHub or contact the maintainers.

---

**Star this repository if you find it helpful! ⭐**
