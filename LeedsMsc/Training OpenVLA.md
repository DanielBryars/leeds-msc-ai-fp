
With OpenVLA what are the joint angles in, are they normalised, how should it be trained?

###### ChatGPT said:

Thought for 1m 10s

Short version: OpenVLA doesn’t really “think in joint angles” out of the box. It thinks in a **normalized action vector** (typically 7-DoF end-effector deltas + gripper), which is then **discretized into tokens**. If you _do_ want to use joint angles, you should still normalize them to a common range (e.g. [-1,1]) and let OpenVLA see only that normalized vector.

---

### 1. What action space does vanilla OpenVLA use?

For the main openvla-7b checkpoint (Bridge-style setups):

- The model is trained on a **7-DoF action**:
    
    - Δx,Δy,Δz\Delta x, \Delta y, \Delta zΔx,Δy,Δz (end-effector translation)
        
    - Δroll,Δpitch,Δyaw\Delta \text{roll}, \Delta \text{pitch}, \Delta \text{yaw}Δroll,Δpitch,Δyaw (orientation)
        
    - gripper open/close
        
- This is an _end-effector_ pose delta, not joint space. [jetson-ai-lab.com+1](https://www.jetson-ai-lab.com/openvla.html?utm_source=chatgpt.com)
    

Internally:

1. Each action dimension is **normalized** to a common numeric range (per-dimension scaling).
    
2. The **original OpenVLA** then **discretizes each dimension into 256 bins**, and those bin indices are mapped to **discrete action tokens** that the LLM predicts. [arXiv](https://arxiv.org/html/2502.19645v1?utm_source=chatgpt.com)
    
3. At inference, the tokens are decoded back to a normalized vector, and then **“unnormalized” with a key like `bridge_orig`** to recover metric units for that robot. [GitHub+1](https://github.com/openvla/openvla)
    

So by default, nothing is in “degrees vs radians” from the model’s point of view; it sees a **dimensionless normalized vector**.

---

### 2. If I _do_ use joint angles, what are they “in”?

If you decide to train/fine-tune OpenVLA on **joint-based actions** instead of end-effector deltas:

- **Use radians** for joint angles at the raw data stage (this is standard in robotics libraries and IK solvers).
    
- Decide whether your actions are:
    
    - **Absolute joint positions** (e.g. 6 joint angles + gripper), or
        
    - **Joint deltas** (change in angles per step + gripper), or
        
    - **Joint velocities** (rare in this ecosystem but possible).
        

For OpenVLA, the important thing is:

> The **final vector you pass into the action tokenizer / training pipeline must be normalized** per dimension (not necessarily “radians” any more).

So the pipeline would be:

1. Start with raw joint angles in radians.
    
2. Decide ranges, e.g. qi∈[qimin⁡,qimax⁡]q_i \in [q_i^{\min}, q_i^{\max}]qi​∈[qimin​,qimax​] from your robot’s joint limits or empirical data.
    
3. Normalize each joint dimension to something like [−1,1][-1, 1][−1,1], e.g.
    
    ai=2⋅qi−qimin⁡qimax⁡−qimin⁡−1a_i = 2 \cdot \frac{q_i - q_i^{\min}}{q_i^{\max} - q_i^{\min}} - 1ai​=2⋅qimax​−qimin​qi​−qimin​​−1
    
    or use quantile normalization (map 1st/99th percentile to −1,1-1,1−1,1) like Pi-0/FAST do. [Hugging Face+1](https://huggingface.co/blog/pi0?utm_source=chatgpt.com)
    
4. Feed this **normalized action vector** into the OpenVLA training code (which will either discretize to tokens or, in OFT, keep it continuous).
    
5. At inference, **invert the normalization** to get back joint angles in radians, then send those to your low-level controller.
    

---

### 3. Are actions always normalized? (Yes, in vanilla OpenVLA)

From the OFT fine-tuning paper (same authors):

> “OpenVLA originally uses discrete action tokens where each action dimension is **normalized to ([-1,+1]** and uniformly discretized into **256 bins**.” [arXiv](https://arxiv.org/html/2502.19645v1?utm_source=chatgpt.com)

So for the **original** OpenVLA:

- Every action component is:
    
    1. Normalized (per dimension, to [−1,1][-1,1][−1,1]),
        
    2. Discretized into 256 bins,
        
    3. Represented as a token.
        

Newer OFT recipes switch to continuous actions, but they **still assume a normalized action space**, just without the 256-bin discretization. [openvla-oft.github.io+1](https://openvla-oft.github.io/?utm_source=chatgpt.com)

---

### 4. How should _you_ train it (for SO100 / your setup)?

Given what you’re doing:

**Recommended pattern:**

1. **Action representation**
    
    - Prefer **Cartesian 7-DoF deltas + gripper** (like OpenVLA’s native setup):
        
        - Translation in metres (or similar), rotation as RPY or quaternion-like parameterisation, plus gripper.
            
        - Let a standard IK solver handle joint angles.
            
    - Or, if you really want joint space, use **joint positions or deltas in radians + gripper** as your action vector.
        
2. **Normalization**
    
    - Compute per-dimension stats on your dataset:
        
        - Either joint limits / workspace limits, _or_
            
        - 1st and 99th percentiles per dimension.
            
    - Map each dimension → [−1,1][-1,1][−1,1], and optionally clip beyond that.
        
3. **Training**
    
    - If you’re using the **vanilla OpenVLA discrete action head**:
        
        - Provide **normalized continuous actions**; the OpenVLA action tokenizer will discretize to 256 bins internally.
            
    - If you’re using **OFT / continuous actions**:
        
        - Train directly on **normalized continuous vectors** with a regression loss (e.g. MSE in normalized space); inversion to physical units only happens after prediction. [openvla-oft.github.io+1](https://openvla-oft.github.io/?utm_source=chatgpt.com)
            
4. **Inference**
    
    - Model outputs normalized (or decoded) action vector.
        
    - Apply your inverse normalization:
        
        - For joint space: get joint angles in radians, send to your controller.
            
        - For Cartesian: get pose deltas in metres/radians, then run IK → joint angles.
            

---

If you tell me whether you’re planning to follow the **OFT (continuous)** route or stick with **discrete tokens**, I can sketch an explicit normalization scheme and unnorm function for your SO100 (joint limits in, code out).