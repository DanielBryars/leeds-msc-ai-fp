
- **Collect small, high-quality robot demos**
    
    - Use your own robot setup. Record visual input (RGB or video) + robot state + action command.
        
    - The survey emphasises data-collection strategies for VLA deployment. [VLA Models Survey+1](https://vla-survey.github.io/?utm_source=chatgpt.com)
        
    - Paper (LLaRA) shows that when demo data is limited, you must maximise its value. [arXiv](https://arxiv.org/abs/2406.20095?utm_source=chatgpt.com)
        
- **Generate language annotations with a large language model**
    
    - For each demo: generate a natural-language instruction, multiple paraphrases, step-wise descriptions if needed.
        
    - This aligns with the “vision-language” part of VLA—many papers emphasise mapping vision+language → action. (e.g., the Fine-Tuning VLA paper) [arXiv](https://arxiv.org/abs/2502.19645?utm_source=chatgpt.com)
        
    - By enriching instruction-embedding you help the model generalise.
        
- **Model choice**
    
    - Choose a base VLA or vision-language model you can fine-tune. For example π₀ uses a pretrained VLM backbone + action expert. [physicalintelligence.company](https://www.physicalintelligence.company/download/pi0.pdf?utm_source=chatgpt.com)
        
    - Depending on your compute: full VLA fine-tuning (vision+action) or simpler behavioural-cloning (image+instruction → action) if you’re limited.
        
- **Fine-tuning strategy**
    
    - Behaviour Cloning (BC): train model to predict next action given frames + language.
        
    - For full VLA fine-tuning: freeze large parts (vision encoder, language backbone) and fine-tune adapters / action head. E.g., the “Enhancing Generalization” paper found freezing helps retain pretrained features. [arXiv](https://arxiv.org/abs/2509.11417?utm_source=chatgpt.com)
        
    - The Fine-Tuning VLA paper studies how action decoding / representation choices affect performance. [arXiv](https://arxiv.org/abs/2502.19645?utm_source=chatgpt.com)
        
- **Hardware**
    
    - Use what you have: e.g., GPU with ~24 GB VRAM is good. If limited, do smaller models or BC only.
        
    - Many papers assume large compute but show strategies for data-efficient fine-tuning (e.g., LLaRA) which is accessible for smaller setups. [arXiv](https://arxiv.org/abs/2406.20095?utm_source=chatgpt.com)
        
- **Pipeline**
    
    - Collect demos → annotate language → preprocess frames → train BC or fine-tune VLA → export model → deploy on robot.
        
    - The survey emphasizes that data + model pipeline matters for real-robot deployment. [arXiv+1](https://arxiv.org/abs/2510.07077?utm_source=chatgpt.com)
        
- **Data quality over quantity**
    
    - Many papers emphasise that small but good datasets + correct architecture beat large noisy sets. E.g., LLaRA emphasises making the most of limited demonstrations. [arXiv](https://arxiv.org/abs/2406.20095?utm_source=chatgpt.com)
        
    - Also “Enhancing Generalization” emphasises preserving pretrained features to generalise rather than over-fit to noisy data. [arXiv](https://arxiv.org/abs/2509.11417?utm_source=chatgpt.com)

|#|Paper & citation|What it focuses on|Practical takeaways for your setup|
|---|---|---|---|
|1|Fine‑Tuning Vision‑Language‑Action Models: Optimizing Speed and Success (Kim, Finn, Liang 2025) ([arXiv](https://arxiv.org/abs/2502.19645?utm_source=chatgpt.com "Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success"))|Investigates fine-tuning of VLAs via design choices: action decoding, action representations, objective functions.|Shows that architecture & loss choices matter a lot. Use continuous action representation + L1 rather than naive discrete tokenizing. Good benchmark.|
|2|Actions as Language: Fine‑Tuning VLMs into VLAs Without Catastrophic Forgetting (Hancock et al 2025) ([arXiv](https://arxiv.org/abs/2509.22195?utm_source=chatgpt.com "Actions as Language: Fine-Tuning VLMs into VLAs Without Catastrophic Forgetting"))|How to fine-tune a vision-language model to VLA without losing its original VLM capabilities.|Highlights risk of forgetting. For home setup: freeze large pre-trained vision/language parts, fine-tune minimal adapters to preserve original reasoning.|
|3|Improving Vision‑Language‑Action Model with Online Reinforcement Learning (Guo et al 2025) ([arXiv](https://arxiv.org/abs/2501.16664?utm_source=chatgpt.com "Improving Vision-Language-Action Model with Online Reinforcement Learning"))|Investigates combining supervised fine-tuning with online RL to improve VLA models.|If you plan to deploy on real robot and collect new data, this helps: alternate supervised BC + small online RL loops.|
|4|Vision‑Language‑Action Reinforcement Fine‑tuning (VLA‑RFT) (Li et al 2025) ([arXiv](https://arxiv.org/abs/2510.00406?utm_source=chatgpt.com "VLA-RFT: Vision-Language-Action Reinforcement Fine ..."))|Uses world-model based RL fine-tuning of VLA models with very few steps.|Practical for home: if you can simulate or collect small real data, RL fine-tuning gives big gains with few iterations.|
|5|RoboMamba: Efficient Vision‑Language‑Action Model for Robotics (Liu 2024) ([papers.nips.cc](https://papers.nips.cc/paper_files/paper/2024/hash/46a126492ea6fb87410e55a58df2e189-Abstract-Conference.html?utm_source=chatgpt.com "RoboMamba: Efficient Vision-Language-Action Model for ..."))|Proposes efficient VLA model that fine-tunes minimal parameters (~0.1%) to get manipulation skills.|Encouraging for budget/compute-limited setups: you don’t always need to train large model from scratch.|
|6|Align‑Then‑steEr: Adapting the Vision‑Language Action Models through Unified Latent Guidance (Zhang et al 2025) ([arXiv](https://arxiv.org/abs/2509.02055?utm_source=chatgpt.com "Align-Then-stEer: Adapting the Vision-Language Action Models through Unified Latent Guidance"))|Adapts VLA models across embodiments/tasks via latent alignment + guidance.|Good if you change robot hardware (you are using UR5e) — the approach helps cross-embodiment transfer.|
|7|Knowledge Insulating Vision‑Language‑Action Models (Physical Intelligence team 2025) ([physicalintelligence.company](https://www.physicalintelligence.company/download/pi05_KI.pdf?utm_source=chatgpt.com "Knowledge Insulating Vision-Language-Action Models"))|Discusses architecture choices to insulate VLM knowledge while adding action modality (continuous + discrete).|Provides strong guidance on action representation decisions (discrete tokens vs continuous).|
|8|VISION‑LANGUAGE‑ACTION INSTRUCTION TUNING (InstructVLA team) ([OpenReview](https://openreview.net/pdf/da565a042d9518954b10ef2b095d725cf65b6f61.pdf?utm_source=chatgpt.com "VISION-LANGUAGE-ACTION INSTRUCTION TUNING"))|Focus on tuning vision-language models with instruction-following for robotic control.|Reinforces importance of the “language” part of VLA: your demo language annotation strategy is supported.|
|9|TGRPO: Fine‑tuning Vision‑Language‑Action Model via Trajectory‑wise Group Relative Policy Optimization (Chen et al 2025) ([Papers with Code](https://paperswithcode.com/paper/tgrpo-fine-tuning-vision-language-action?utm_source=chatgpt.com "TGRPO :Fine-tuning Vision-Language-Action Model via Trajectory ..."))|RL fine-tuning method for VLA using trajectory‐wise grouped advantage signals.|If you intend to do few demonstration trajectories + RL, this method is relevant.|
|10|ConRFT: A Reinforced Fine‑tuning Method for VLA Models via Consistency Policy (Chen et al 2024) ([Robotics Proceedings](https://www.roboticsproceedings.org/rss21/p019.pdf?utm_source=chatgpt.com "[PDF] ConRFT: A Reinforced Fine-tuning Method for VLA Models via ..."))|Fine‐tuning VLA models via combined BC + Q-learning + online human intervention for real-world tasks.|Real‐robot example with limited data and quick adaptation. Good benchmark for real robot fine-tuning.|
