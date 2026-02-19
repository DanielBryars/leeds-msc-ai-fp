

# Modern Robot Policy Models — Verified Comparison Table

> **Important notes:**
> - All data has been cross-checked against original papers, repos, and model cards (Feb 2025).
> - **Inference Rate** is reported as the model's forward-pass frequency. For chunk-based models (ACT, Pi0, Pi0.5), one forward pass produces many future actions; the robot executes from a buffer at a higher control frequency (e.g. 50 Hz). The inference hardware is noted per-model in the table.
> - **Home Gamer** ratings assume a single consumer GPU. "Easy" = any 8 GB+ GPU. "Moderate" = RTX 4090 (24 GB) for inference, LoRA fine-tuning possible. "Hard" = needs datacenter GPU (A100/H100) or no public weights.


## Comparison Table

| Model | Pub. Date | Params | Inf. VRAM | Train VRAM | Inference Rate (HW) | Architecture Summary | Open Source? | Home Gamer | Paper / Repo |
|---|---|---|---|---|---|---|---|---|---|
| **RT-1** | Dec 2022 | 35 M | ~2–4 GB | ~6–8 GB | 3 Hz (TPU v3) | EfficientNet-B3 + FiLM conditioning + TokenLearner + 8-layer Transformer | Yes | **Easy** — tiny model, runs on any modern GPU | [Paper](https://arxiv.org/abs/2212.06817) / [Repo](https://github.com/google-research/robotics_transformer) |
| **Diffusion Policy** | Jun 2023 (RSS) | 40–90 M | ~4–6 GB | ~8–12 GB | 4–10 Hz (RTX 3090) | Conditional denoising diffusion (CNN U-Net or Transformer variants) for action trajectories | Yes | **Easy** — trains and infers on 8–12 GB GPU | [Paper](https://arxiv.org/abs/2303.04137) / [Repo](https://github.com/real-stanford/diffusion_policy) |
| **ACT** | Jul 2023 (RSS) | ~80 M | ~2–4 GB | ~8–11 GB | ~50 Hz (RTX 2080 Ti); chunks of 100 actions | CVAE: ResNet-18 vision backbone + Transformer encoder-decoder; predicts action chunks | Yes (MIT) | **Easy** — trains on RTX 2080 Ti (11 GB) | [Paper](https://arxiv.org/abs/2304.13705) / [Repo](https://github.com/tonyzhaozh/act) / [LeRobot](https://github.com/huggingface/lerobot) |
| **RT-2** | Jul 2023 | 5 B / 12 B / 55 B | 12–20 GB (5 B) to 100+ GB (55 B) | Multi-TPU pod | 1–5 Hz (TPU v4 pod) | Vision-language model (PaLI-X or PaLM-E) fine-tuned to output tokenized robot actions | No (paper only) | **Hard** — no public weights; 55 B model needs datacenter HW | [Paper](https://arxiv.org/abs/2307.15818) / [Site](https://robotics-transformer2.github.io) |
| **Open X-Embodiment (RT-X)** | Oct 2023 | RT-1-X: 35 M; RT-2-X: 55 B | 2–4 GB (RT-1-X); 100+ GB (RT-2-X) | Same as RT-1 / RT-2 | 3 Hz (RT-1-X on TPU) | RT-1 / RT-2 architectures trained on cross-embodiment dataset (22 robots) | Partially (dataset + RT-1-X weights) | **Easy** for RT-1-X; **Hard** for RT-2-X | [Paper](https://arxiv.org/abs/2310.08864) / [Repo](https://github.com/google-deepmind/open_x_embodiment) |
| **OpenVLA** | Jun 2024 | 7 B | ~15 GB (bf16); ~8 GB (4-bit) | ~40–60 GB full; ~16–24 GB LoRA | ~6 Hz (RTX 4090, bf16) | Prismatic VLM (DINOv2 + SigLIP) + Llama 2 7B backbone, discretized action output | Yes | **Moderate** — inference w/ quantization on 8 GB; LoRA fine-tuning on 24 GB | [Paper](https://arxiv.org/abs/2406.09246) / [Repo](https://github.com/openvla/openvla) |
| **Pi0** | Oct 2024 | 3.3 B | >8 GB (RTX 4090) | >22.5 GB LoRA; >70 GB full | ~12 Hz (RTX 4090); chunks of 50 actions | VLA flow model: PaliGemma (SigLIP + Gemma) backbone + flow-matching action expert | Yes (OpenPI) | **Moderate** — inference on RTX 4090; LoRA on 24 GB; full train needs A100 | [Paper](https://arxiv.org/abs/2410.24164) / [Repo](https://github.com/Physical-Intelligence/openpi) |
| **HIL-SERL** | Oct 2024 | Small (ResNet + MLP policy) | ~2–4 GB | ~8–12 GB (online RL) | >20 Hz (consumer GPU) | SAC-based RL with human demonstrations and interventions; pretrained visual backbone | Yes | **Easy** (compute), but requires real robot for RL training loop | [Paper](https://arxiv.org/abs/2410.21845) / [Repo](https://github.com/rail-berkeley/hil-serl) |
| **MiniVLA** | Dec 2024 | ~1 B | ~4–6 GB | ~12–16 GB | ~10–15 Hz (est.) | Compact VLA: Qwen 2.5 0.5B language backbone + OpenVLA-style ViT encoder | Yes | **Easy** — inference and fine-tuning on 12–16 GB GPU | [Blog](https://ai.stanford.edu/blog/minivla/) / [Repo](https://github.com/Stanford-ILIAD/openvla-mini) |
| **RoboMM** | Dec 2024 | ~3–7 B | ~12–20 GB | ~40–60 GB | ~2–5 Hz (est.) | Multi-modal encoder (vision + depth + proprio) + OpenFlamingo LLM decoder + action head | Yes | **Moderate** — inference on 16–24 GB GPU | [Paper](https://arxiv.org/abs/2412.07215) / [Repo](https://github.com/RoboUniview/RoboMM) |
| **Pi0.5** | Apr 2025 | ~4 B | >8 GB (RTX 4090) | >22.5 GB LoRA; >70 GB full | ~1–2 Hz model calls (RTX 4090); actions buffered at 50 Hz | Hierarchical VLA: PaliGemma + FAST tokenizer; System-2 subtask planner → System-1 flow-matching action controller | Yes (OpenPI) | **Moderate** — inference on RTX 4090; LoRA on 24 GB; full train needs A100/H100 | [Paper](https://arxiv.org/abs/2504.16054) / [Repo](https://github.com/Physical-Intelligence/openpi) |
| **SmolVLA** | Jun 2025 | ~450 M | ~4–6 GB | ~8–12 GB | ~10–15 Hz (est.) | Compact VLA based on SmolVLM2-500M backbone, designed for edge deployment | Yes (HuggingFace) | **Easy** — small enough for any 8 GB+ GPU | [Paper](https://arxiv.org/abs/2506.01844) / [LeRobot](https://github.com/huggingface/lerobot) |


## Home Gamer Summary

| Rating | What you need | Models |
|---|---|---|
| **Easy** | Any 8–12 GB GPU (RTX 3060, RTX 2080 Ti, etc.) | RT-1, Diffusion Policy, ACT, RT-1-X, HIL-SERL, MiniVLA, SmolVLA |
| **Moderate** | RTX 4090 (24 GB) for inference; LoRA fine-tuning possible | OpenVLA, Pi0, Pi0.5, RoboMM |
| **Hard** | Datacenter GPUs (A100/H100) or no public weights | RT-2, RT-2-X |

