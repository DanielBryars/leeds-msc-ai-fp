### 1. **Automated Stock-Taking with RGBD Vision**

- **Problem:** Manual stock audits are slow and error-prone.
    
- **Research Idea:** Use RGBD vision to automatically detect and count objects in bins.
    
- **Challenge:** Items overlap, and no canonical models exist.
    
- **Contribution:** Develop a method that _progressively estimates certainty_ (empty → one item → many items). Could include uncertainty quantification so the system decides when human intervention is required.
    
- **Evaluation:** Accuracy of “is this bin empty? how many items? which items?” vs human/manual counts.
    

---

### 2. **Self-Supervised Item Library Creation**

- **Problem:** No CAD models or labelled data for stock.
    
- **Research Idea:** Exploit repeated co-occurrence of items across bins to build visual prototypes of each item without explicit annotation (like a “warehouse-specific foundation model”).
    
- **Challenge:** Discovering that “the object that looks like this in bin 1 is the same as that in bin 2.”
    
- **Contribution:** Graph-based clustering or contrastive self-supervised learning to bootstrap a library of item embeddings.
    
- **Evaluation:** How fast/accurate does the library converge given N bins/day? Could simulate with your ~1200 bins/day throughput.
    

---

### 3. **Pickability Prediction**

- **Problem:** Not all items are easy for a robot to grasp (irregular shapes, occlusions).
    
- **Research Idea:** Train a classifier that predicts _success likelihood of robotic grasp_ directly from an RGBD view.
    
- **Challenge:** Requires labelled data (“success/failure” of grasp attempts). Could start with human labels or simulated grasp trials.
    
- **Contribution:** A decision policy for robot/human handover — system routes easy picks to robots, tricky ones to humans.
    
- **Evaluation:** Success rate improvement, throughput, human workload reduction.
    

---

### 4. **Active Vision for Bin Scanning**

- **Problem:** A single camera angle may not reveal all items (occlusions).
    
- **Research Idea:** Mount an RGBD camera on the UR end-effector, plan motions to scan bin from multiple angles, fuse views into a 3D reconstruction.
    
- **Contribution:** Novel active-perception strategy optimised for speed vs completeness (fewest extra views needed to resolve occlusion).
    
- **Evaluation:** Completeness of item detection vs scan time. Could benchmark “how many items seen after 1, 2, 3 views.”
    

---

### 5. **Automated Consolidation via Multi-Object Grasping**

- **Problem:** Consolidation is manual.
    
- **Research Idea:** Develop a two-stage pipeline:
    
    1. Predict pickability (above).
        
    2. Plan grasp pose using RGBD + learned grasp synthesis (e.g., Dex-Net style).
        
- **Contribution:** Focus on _uncertainty-aware grasp planning_: robot only acts if confidence > threshold.
    
- **Evaluation:** Success rate, wasted robot motions, number of human escalations.
    

---

### 6. **Uncertainty-Aware Perception in Bin Picking**

- **Problem:** Errors in detection cascade downstream.
    
- **Research Idea:** Extend bin recognition pipeline with probabilistic reasoning (Bayesian networks or learned uncertainty estimates).
    
- **Contribution:** Formalism for “partial knowledge” — system doesn’t need to be 100% sure, just know when to defer.
    
- **Evaluation:** Compare throughput/accuracy with vs without uncertainty-aware decision layer.
    

---

### 7. **Domain-Specific Foundation Models**

- **Problem:** Generic pretrained vision models (e.g., CLIP, SAM) don’t directly transfer to cluttered, warehouse-specific bins.
    
- **Research Idea:** Fine-tune or adapt open-source foundation models using warehouse bin images to handle occlusion, small dataset sizes, and domain shift.
    
- **Contribution:** Study how far off-the-shelf models get you vs lightweight adaptation.
    
- **Evaluation:** Recognition accuracy on your data vs baseline.
    

---

💡 If you want a single tight thesis topic, I’d suggest **“Predicting Robot Grasp Success in Warehouse Bin Picking from RGBD Data under Occlusion.”**  
It ties together _perception (RGBD)_, _uncertainty (success prediction)_, and _operations (handover to humans)_ — concrete, measurable, and publishable.

---

Do you want me to sketch how these could be prioritised (quick wins vs ambitious research), so you can pick one that fits your 6-month MSc timeframe?