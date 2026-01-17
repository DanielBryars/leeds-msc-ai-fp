
Pi0 used segment annotations - but they didn't publish the data, but these heroes did:

## 🧱 Datasets on Hugging Face with Subtask Segmentation

These aren’t Pi-0, but they _do_ include **temporal segment / subtask labels**:

### ✅ RoboCOIN Family

Several RoboCOIN datasets include **fine-grained subtask segmentation and labeling** alongside robot state, visuals, etc. Examples include:

- **RoboCOIN/R1_Lite_make_tea** – subtask segmentation labels with scene and gripper annotations.
    
- **RoboCOIN/AIRBOT_MMK2_boxs_storage** – similar subtask segment labels.
    
- **RoboCOIN/RMC-AIDA-L_pour_coffee_beans** – long episodes with subtask labelling.
    

These datasets are structured (often in **LeRobot format**) with a `subtask_annotation` field per frame that indicates the current subtask ID, so you _can reconstruct temporal segments_ by grouping identical IDs over time.

👉 This is conceptually very close to Pi-0’s segment annotation goal — just without natural-language labels.

---

### ✅ RealSource World (Hugging Face)

**RealSource World** is a large real-robot manipulation dataset with **fine-grained “atomic skill” segmentation** and quality assessments for each episode.

- Multi-camera real robot data
    
- Actions + states + visual observations
    
- **Atomic skill segmentation** (akin to temporal subtask labels)
    

Although the segmentation there isn’t necessarily _natural-language_, it _is_ explicit skill segmentation that can be used to train hierarchical or segmented models.

---

## 📚 Research Work with Explicit Segment Labels

These aren’t direct Hugging Face datasets, but they show active work in segment annotations:

### 🧠 **GATE-VLAP Dataset**

This is a research dataset that contains **2,124 atomic action segments** derived from manipulation trajectories with planner alignment, STRIPS-style labels, temporal bounds, and pre/postconditions.

- Each segment has start/end frames
    
- Each segment is labeled with a symbolic action + arguments
    
- Aligns low-level data with logical action semantics
    

This is closer to what Pi-0 does _conceptually_ (though smaller and symbolic in nature).

---

## 📌 Related Trends in Segmentation

While not full trajectory segmentation datasets for robot control, these show related directions:

- Some works derive segmentation from trajectories using multimodal reasoning (e.g., vision + proprioception + LLMs) — e.g., **Robo2VLM** extracts sequence phases for QA tasks.
    
- Robotics foundations like **LeRobot** standardise formats with segmentation support, easing shared annotations across benchmarks.
    

---

## 🧩 What’s Still _Rare_

🟥 **Language-conditioned segment annotations** (i.e., segments tagged with natural-language labels like “align gripper”, “lift object”) are still mostly **internal to proprietary datasets** like Pi-0. Public alternatives tend to:

- use **numeric subtask IDs**, or
    
- symbolic STRIPS-style labels, but
    
- rarely full phrase descriptions tied to language models.
    

---

## 📌 Summary

|Dataset|Fine-grained segments|Language labels?|Public|
|---|---|---|---|
|RoboCOIN family|✔️ numeric subtask IDs|❌|✔️|
|RealSource World|✔️ skills per frame|❌|✔️|
|GATE-VLAP|✔️ symbolic action segments|✴️ symbolic (planner actions)|✔️/paper|
|Pi-0 dataset|✔️ language segments|✔️ natural language|❌ published|

---

If you want, I can point you to **code snippets** showing how to load one of these Hugging Face datasets (e.g., RoboCOIN) and extract the temporal segments — just ask!