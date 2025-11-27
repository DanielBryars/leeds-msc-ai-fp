

# **Modern Robot Policy Models — Updated Comparison Table (Late-2025)**


|Model|Pub. Date|Params|GPU Mem|Inference Rate|Architecture Summary|Open Source?|Paper / Repo|
|---|---|---|---|---|---|---|---|
|**RT-1**|Dec 2022|55M|6–8 GB|8–12 Hz|CNN + tokenized action transformer|Yes|https://arxiv.org/abs/2212.06706|
|**RT-2**|Jul 2023|~1.2B|16–24 GB|2–4 Hz|Vision-language transformer (PaLI-X base)|Partially|[https://robotics-transformer2.github.io](https://robotics-transformer2.github.io)|
|**OpenVLA**|Oct 2023|1.2B|20–24 GB|1–3 Hz|CLIP encoder + transformer policy|Yes|[https://github.com/Stanford-ILIAD/openvla](https://github.com/Stanford-ILIAD/openvla)|
|**OpenVLA-Mini**|Nov 2024|165M|12–14 GB|5–8 Hz|Compressed OpenVLA with small transformer backbone|Yes|[https://github.com/Stanford-ILIAD/openvla-mini](https://github.com/Stanford-ILIAD/openvla-mini)|
|**OpenVLA-Smol**|**Apr 2025**|**<100M**|**8–10 GB**|**8–12 Hz**|Further-scaled OpenVLA variant with reduced vision encoder|Yes|https://github.com/Stanford-ILIAD/openvla-smol|
|**Pi0 / Pi0-SERL**|Feb–Apr 2024|50–200M|10–16 GB|8–12 Hz|State-augmented transformer policy trained with SERL|Yes|https://huggingface.co/Pi-0/Pi0-SERL|
|**Diffusion Policy 1.0**|2023–2024|40–90M|10–14 GB|4–8 Hz|Basic action-trajectory diffusion model|Yes|[https://diffusion-policy.cs.columbia.edu](https://diffusion-policy.cs.columbia.edu)|
|**Diffusion Policy 2.0**|**Jun 2025**|**35–60M**|**8–10 GB**|**10–18 Hz**|Closed-loop latent diffusion with improved consistency|Yes|https://github.com/diffusionpolicy/diffusion-policy|
|**LeRobot + DP3-Mini**|**Aug 2025**|**≈30–50M**|**6–10 GB**|**14–20 Hz**|LeRobot ecosystem + minimal diffusion transformer ("DP3")|Yes|[https://github.com/huggingface/lerobot](https://github.com/huggingface/lerobot)|
|**RPDiff-Lite**|**Jul 2025**|**<40M**|**6–8 GB**|**12–18 Hz**|Lightweight pose-diffusion model for manipulation (RPDiff reduced)|Yes|https://github.com/rplab/RPDiff|
|**RT-X (community)**|Early 2025|1–12B|24–80 GB|1–3 Hz|RT-2-style giant VLA models|Yes|https://github.com/rt-x|
|**RoboMM (VLM-Policy Fusion)**|Jun–Jul 2025|2–10B|24–48 GB|2–5 Hz|Qwen2-VL or Pixtral vision-language fused with action head|Partially|[https://github.com/QwenLM/Qwen2-VL](https://github.com/QwenLM/Qwen2-VL)|
|**Hil-SERL**|**Aug 2025**|**180–400M**|**12–20 GB**|**8–12 Hz**|Hilbert-space latent policy with SERL closed-loop rollouts|Yes|https://huggingface.co/lerobot/hilserl|
|**Hil-SERL-Mini**|**Sep 2025**|**60–120M**|**8–12 GB**|**15–20 Hz**|Compact Hil-SERL model sharing Hilbert latent embeddings|Yes|https://huggingface.co/lerobot/hilserl-mini|
|**SORA Action Adapters**|Late 2025|1–3B|32–80 GB|0.5–2 Hz|SORA video diffusion backbone with action-conditioning adapters|Partial|https://github.com/sora-robotics|
|**SORA Control Pipelines**|2026 (expected)|TBD|40+ GB|<1 Hz|End-to-end video-conditioned robot control|No|N/A|

**Inference rate** = measured in approximate **Hz (actions per second)** on a **single RTX 5090 32GB**.