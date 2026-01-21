# Experiments Log

## 2026-01-21: ACT Spatial Generalization Evaluation

**Model**: `outputs/train/act_20260118_155135/checkpoint_045000`
**Task**: Pick up the block and place it in the bowl
**Training position**: (0.217, 0.225)

### Experiment Setup

Evaluated ACT policy at a 5x5 grid of block positions across the workspace:
- X range: 0.15 to 0.35 (forward from robot)
- Y range: -0.15 to 0.30 (side to side)
- 20 episodes per position = 500 total episodes
- Position sorted by distance from training position (center-out evaluation)

### Results Summary

**Overall Success Rate: 12.6%**

| Distance from Training | Success Rate | Notes |
|------------------------|--------------|-------|
| d < 0.05m | 60-70% | Near training distribution |
| d = 0.07-0.10m | 10-35% | Some generalization |
| d > 0.11m | 0-5% | Near complete failure |

### Key Findings

1. **ACT has very limited spatial generalization**
   - Performance degrades sharply beyond ~5cm from training position
   - Near-zero success beyond ~10cm displacement

2. **Directional asymmetry**
   - Same distance, different directions yield different results
   - e.g., d=0.077: 15% at (0.15, 0.19) vs 35% at (0.20, 0.30)

3. **False positives near goal**
   - Positions near y=-0.15 (near bowl) showed "1 step" successes
   - Block randomly landed in/near bowl due to position noise, not policy skill

### Raw Data by Position (sorted by distance)

| Distance | Position | Success Rate |
|----------|----------|--------------|
| 0.041 | (0.20, 0.19) | 60% |
| 0.050 | (0.25, 0.19) | 70% |
| 0.077 | (0.15, 0.19) | 15% |
| 0.077 | (0.20, 0.30) | 35% |
| 0.082 | (0.25, 0.30) | 35% |
| 0.091 | (0.30, 0.19) | 10% |
| 0.101 | (0.15, 0.30) | 20% |
| 0.112 | (0.30, 0.30) | 0% |
| 0.138 | (0.35, 0.19) | 0% |
| 0.151+ | (various) | 0-10% |

### Files

- CSV: `outputs/experiments/spatial_eval_20260121_154657.csv`
- JSON: `outputs/experiments/spatial_eval_20260121_155655.json`

---

## 2026-01-21: ACT Fine-Grained Spatial Evaluation

**Model**: `outputs/train/act_20260118_155135/checkpoint_045000`
**Grid**: 7x7 centered on training position (0.217, 0.225)
- X range: 0.17 to 0.27 (±5cm)
- Y range: 0.15 to 0.30 (±7.5cm)
- 10 episodes per position = 490 total episodes

### Results Summary

**Overall Success Rate: 51.6%**

| Distance | Success Rate |
|----------|--------------|
| d < 0.02m | 90-100% |
| d = 0.02-0.04m | 70-100% |
| d = 0.04-0.06m | 60-90% |
| d = 0.06-0.08m | 10-50% (varies by direction) |
| d > 0.08m | 0-30% |

### Key Finding: Directional Asymmetry

At the same distance (~7.5cm), success varies dramatically by direction:

| Direction | Position | Distance | Success |
|-----------|----------|----------|---------|
| +Y (away from bowl) | (0.20, 0.30) | 0.076 | 50% |
| -Y (toward bowl) | (0.20, 0.15) | 0.076 | 0% |
| +Y | (0.22, 0.30) | 0.075 | 20% |
| -Y | (0.22, 0.15) | 0.075 | 0% |

**Interpretation**: The robot learned to move blocks in the -Y direction (toward bowl at y=-0.225).
- Blocks at y > training: Robot just moves further in learned direction → some success
- Blocks at y < training: Robot overshoots or has wrong geometry → failure

### Files

- CSV: `outputs/experiments/spatial_eval_fine_grid.csv`
- JSON: `outputs/experiments/spatial_eval_20260121_160613.json`

### Heatmap Visualizations

- Wide grid (5x5): `outputs/experiments/spatial_heatmap_wide.png`
- Fine grid (7x7): `outputs/experiments/spatial_heatmap_fine.png`
- Success vs Distance: `outputs/experiments/spatial_success_vs_distance.png`

### Combined Analysis (990 episodes - initial)

| Distance (m) | Success Rate | N Episodes |
|--------------|--------------|------------|
| 0.01 | 97% | 30 |
| 0.03 | 79% | 100 |
| 0.05 | 64% | 200 |
| 0.07 | 25% | 160 |
| 0.09 | 18% | 120 |
| 0.11+ | 0-10% | 200+ |

**Key Finding: 50% success threshold crossed at approximately 7cm from training position.**

---

## 2026-01-21: Extended Spatial Evaluation (2630 episodes)

**Model**: `outputs/train/act_20260118_155135/checkpoint_045000`

Expanded spatial evaluation to fill coverage gaps and extend testing range to 30cm from training position.

### Additional Evaluation Runs

| Region | Grid | Episodes | Success Rate |
|--------|------|----------|--------------|
| Right side (x: 0.27-0.35) | 5×5 | 250 | 12% |
| Lower area (y: 0.05-0.15) | 5×5 | 250 | 10% |
| Left side (x: 0.12-0.18) | 5×5 | 250 | 8% |
| Intermediate lower (y: 0.10-0.16) | 4×4 | 160 | 15% |
| y=-0.05 to 0.05 band | 5×5 | 250 | 0% |
| Far left (x: 0.05-0.15) | 4×4 | 160 | 5% |
| Far right (x: 0.35-0.42) | 4×4 | 160 | 0% |
| Far right-bottom corner | 4×4 | 160 | 0.6% |

### Final Results Summary

**Total Episodes: 2630**
**Overall Success Rate: 17.2%** (453/2630)

| Distance (cm) | Episodes | Interpretation |
|---------------|----------|----------------|
| 0-5 | ~400 | Core training region |
| 5-10 | ~750 | Good generalization zone |
| 10-15 | ~450 | Degraded performance |
| 15-20 | ~350 | Near-complete failure |
| 20-30 | ~500 | Complete failure |

### Coverage Distribution

```
Distance  Episodes  Coverage
0-5cm     ~400      ████████████████
5-10cm    ~750      ██████████████████████████████
10-15cm   ~450      ██████████████████
15-20cm   ~350      ██████████████
20-30cm   ~500      ████████████████████
```

### Visualization

MuJoCo scatter visualization with:
- Green/red flat circles for success/failure at each test position
- Blue distance rings at 5cm, 10cm, 15cm, 20cm from training position
- Overlapping translucent circles show test density

**Files**:
- Combined CSV: `outputs/experiments/spatial_eval_combined.csv`
- Scatter plot: `outputs/experiments/spatial_scatter_1900.png`

### Implications for Thesis

This demonstrates a critical limitation of behavior cloning approaches like ACT:
- Training data was collected at a single position with small noise
- Policy memorizes the exact visual-motor mapping for that position
- No ability to interpolate or extrapolate to novel positions
- Suggests need for either: (a) diverse training data, or (b) policy architecture with better spatial reasoning

---

## 2026-01-21: Pi0 Flow Matching Visualization

**Model**: `danbhf/pi0_so101_lerobot`
**Task**: Pick up the block and place it in the bowl
**Result**: SUCCESS at step 155

### Flow Matching Denoising Analysis

Visualized the 10-step flow matching denoising process from noise (t=1.0) to final actions (t=0.0).

**Screenshot**: `/d/git/leeds-msc-ai-fp/LeedsMsc/CameraShapshots/Pi0 Whisker Convergence.png`

#### Convergence Data (normalized action space)

| Step | t    | mean  | std  | min   | max  |
|------|------|-------|------|-------|------|
| 0    | 1.00 | -0.09 | 1.00 | -3.13 | 3.18 |
| 5    | 0.50 | -0.07 | 0.59 | -1.78 | 1.47 |
| 10   | 0.00 | -0.06 | 0.58 | -1.10 | 0.75 |

#### Key Observations

1. **Flow matching converges gradually in normalized space**
   - std decreases: 1.0 (noise) → 0.5-0.7 (final)
   - Range tightens: [-3, 3] → [-1, 1.5]

2. **Visual chaos explained**
   - Small differences in normalized space → large angle differences after denormalization
   - FK amplifies these into scattered 3D positions
   - The "crystallization" IS happening, just hard to see visually

3. **Model actively steers toward targets**
   - In chunk 4 (step 150), mean shifts from 0.05 → 0.49 during denoising
   - The velocity field is pushing toward the correct action, not just reducing variance

#### How Flow Matching Works

```
Start: x₁ ~ N(0, I)           # Pure noise at t=1.0
For step in range(10):
    v_t = model(x_t, t)       # Predict velocity
    x_{t-dt} = x_t + dt * v_t # Move along velocity field
End: x₀ = actions             # Final actions at t=0.0
```

Each step moves the sample along the learned velocity field. Unlike diffusion which gradually removes noise, flow matching learns direct paths from noise to data.

---

## 2026-01-21: Pi0 Whisker Visualization (First Success)

**Model**: `danbhf/pi0_so101_lerobot`
**Task**: Pick up the block and place it in the bowl
**Result**: SUCCESS at step 145

First successful Pi0 run with FK-based whisker visualization. Confirmed Pi0 works with:
- chunk_size=50, n_action_steps=50 (open-loop within each chunk)
- 224x224 images from overhead_cam and wrist_cam
- ~315ms per chunk prediction (10 internal denoising steps)
- ~5-7ms per step execution

---

## 2026-01-20: ACT Chunking Rollout Length Experiment

**Model**: `outputs/train/act_20260118_155135/checkpoint_045000`
**Results**: See `act_chunking_rollout_20260120_113808.json`

Tested different `n_action_steps` values (rollout length before re-prediction).

### ACT VAE Stochasticity Finding

During variance visualization experiments, discovered:
- ACT is **deterministic** in eval mode (uses zero latent vector)
- To get stochastic sampling, must patch `torch.zeros` to return `torch.randn` for latent-sized tensors
- Even with stochastic sampling, variance is tiny (~0.1mm in FK space)
- The VAE latent has minimal influence on outputs - ACT is very confident
