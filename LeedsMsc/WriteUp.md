# Improving Generalisation Performance of Imitation-Learnt Tasks of Small Vision-Based Policies for Robot Control Under Low-Cost Constraints

## Background

### LLMs and the AI Renaissance

ChatGPT has excited the public consciousness towards an AI-backed future. From the "Attention is All You Need" breakthrough (Vaswani et al., 2017), transformer-based architectures have spawned research into the emergent behaviour of Large Language Models. Along with Chain-of-Thought prompting (Wei et al., 2022), LLMs are now used in a variety of tasks which are transforming society in many areas. In addition to the transformer, two other ingredients are required to derive the latent knowledge and reasoning gains we have seen: lots of data and lots of compute (Kaplan et al., 2020). The volume of AI-related scientific publications has grown exponentially, with submissions to conferences such as NeurIPS and ICML roughly doubling every two to three years (Sevilla et al., 2022).

The increased interest and investment in AI — global private AI investment exceeded $90 billion in 2024 (Stanford HAI, 2024) — has led to the significant availability of GPU compute, both cloud-based (e.g. vast.ai, Lambda Labs, RunPod) and in consumer hardware (e.g. NVIDIA RTX 5090 with 32GB VRAM). Open models, through platforms such as HuggingFace and Kaggle, have improved the availability of foundation models (pretrained models) which can be finetuned. These websites also provide a nexus for datasets and a community to drive progress. Experiment tracking tooling such as Weights & Biases, and advances in frameworks such as PyTorch (Paszke et al., 2019) help democratise access to AI research and development, providing access to independent researchers as well as universities and large companies.

### Combining Foundation Models for Robotics

Combining vision models and language models into a VLM (such as SigLIP (Zhai et al., 2023) and Gemma, see PaliGemma (Beyer et al., 2024)) allows interesting problems to be solved, such as image captioning and visual question answering (Zhou, Liu and Gao, 2024).

Recently there has been interest in combining Vision, Language and "Action Heads" — so-called VLAs (Vision-Language-Action models) to perform generalised robotic control - introduced by RT-2 (Brohan et al., 2023), with examples such as Octo (Team et al., 2024), OpenVLA (Kim et al., 2024), and Pi0 (Black et al., 2024). The theory is that the vision model provides the features to recognise objects in the world, the LLM provides a semantic link between those objects and language, and through training with large numbers of robot demonstration episodes we can build a model which generalises over robotic tasks. Essentially: leverage the existing investment and bring the advances in LLMs and vision models into the realm of robots. 

### Problem with Current VLAs for Experimentation under constrained resources

OpenVLA (Kim et al., 2024), Pi0, and Pi0.5 (Physical Intelligence, 2025) are still quite large models for a self-funded individual to experiment with. For example, a Pi0 checkpoint is 13GB and training requires at least 48GB of VRAM. Inference, even on a 32GB RTX 5090, runs at best at 4Hz. Zero-shot performance is weak, so some finetuning is required to get any results. I tried these models and found training time and resource requirements unwieldy.

Not everything is open source. Datasets are generally proprietary — for example, the sub-task annotations used to train Pi0 and Pi0.5 — because collecting robot data is expensive (Mandlekar et al., 2018).

### Low-Cost Approaches

The paper "Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware" (Zhao et al., 2023) provides a way to use Behavioural Cloning (Pomerleau, 1991) to teach a model to perform a task such as tying shoelaces or picking up a block. This model is known as ACT (Action Chunking with Transformers) and is small, cheap to train, and inference is very fast (~200Hz), allowing rapid simulation-based experimentation.

However, my tests with ACT show that it learns a task very well with just an hour of training, but does not generalise well — it essentially learns a trajectory based on visual feedback. Within the training distribution the policy works well, but after training on a task such as picking up a block, it cannot pick up the block at a different location (see Results).

## Proposal

Walking is a different skill to tying shoelaces.

Use ACT as a basis for a model to learn position-invariant subtasks. Use a larger, more capable LLM to orchestrate those tasks — effectively hoisting the "L" from VLA and handling language-conditioned planning separately.

Long-term horizon problems with Behavioural Cloning include compounding errors (Ross et al., 2011) and multi-modal action distributions. "Blinkering" — the tendency of BC policies to commit to a single mode and ignore alternatives — is a related failure pattern.

## Setup

This project uses LeRobot by HuggingFace (Cadene et al., 2024). LeRobot is designed to make it more accessible to experiment with robotics, comprising a collection of models based on PyTorch (for example, they rewrote the Pi0/Pi0.5 models from JAX to PyTorch), a dataset format and viewer, and an open-source design for a 3D-printed robot (SO-100/SO-101).

I have two 6-DOF SO-100 robot arms. These use Feetech servo motors with counts from 0–4095 and an offset which handles wrap-around. The arm was calibrated in joint-angle space, mapping counts to degrees, with the gripper mapped 0–100 for closed and open. The URDF model from the SO-100 robot repository was used to normalise the data to [-1, 1] for training and denormalise to joint angles at inference. Normalisation is important to maximise dynamic range during training and ensure stable gradient flow (Ioffe & Szegedy, 2015). This sounds simple but took a surprisingly long time to get right. Some datasets are recorded in radians (e.g. the Open X-Embodiment format (Open X-Embodiment Collaboration, 2024)) while others use delta actions (e.g. Pi0) instead of absolute positions.

A simple teleoperation script was used to test the calibration of the robots, configuring one as a follower and one as a leader to ensure they were in sync.

A simulation based on the SO-100 MJCF model was built in MuJoCo (Todorov et al., 2012), and a teleoperation script was built with the real leader SO-100 set up to drive the simulation — this proved the calibration. Friction coefficients were configured between the gripper and the block through trial and error.

The simulation environment was extended using MuJoCo for physics and OpenXR to view the simulation environment through a Meta Quest 3 headset for training. The human expert would move the real leader arm to generate demonstration episodes.

*Note: observed state was used, not the demand, for training — need to verify this.*

I experimented with training the model in end-effector space, using forward kinematics (FK) during training to convert joint positions to XYZ position and a quaternion orientation. And an inverse kinematics (IK) solver after inference to convert back to joint angles — the idea being that end-effector space would be easier to learn in (cf. Goodfellow et al., 2016, §5.3 on the effect of coordinate representations on learning), and could potentially transfer to other robot topologies without retraining. However, results were inconclusive (see Results) and all remaining experiments were performed in joint space.

## Delta vs Absolute

*Section to be completed.*


References (to be tidied up)

"Attention is All You Need" (Vaswani et al., 2017) https://arxiv.org/abs/1706.03762
"Chain-of-Thought..." (Wei et al., 2022) https://arxiv.org/abs/2201.11903
"Scaling Laws for Neural Language Models" (Kaplan et al., 2020)  https://arxiv.org/abs/2001.08361
"Compute Trends Across Three Eras of Machine Learning" (Sevilla et al., 2022)  https://arxiv.org/abs/2202.05924
The 2024 AI Index Report (Stanford HAI, 2024) https://hai.stanford.edu/ai-index/2024-ai-index-report
"PyTorch..." (Paszke et al., 2019) https://arxiv.org/pdf/1912.01703
"SigLIP" (Zhai et al., 2023) https://arxiv.org/pdf/2303.15343
"PaliGemma" (Beyer et al., 2024) https://arxiv.org/abs/2407.07726
Zhou, K., Liu, Z. and Gao, P. (eds.) (2024) Large Vision-Language Models: Pre-training, Prompting, and Applications. Cham: Springer
OpenVLA (Kim et al., 2024) https://arxiv.org/abs/2406.09246