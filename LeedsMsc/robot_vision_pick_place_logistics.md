12/08/2025
# Conversation: Robot Vision for Pick and Place in Logistics

## User
Can you give me a summary of recent papers and research in robot vision for pick and place in logistics?

## Assistant
Here’s a tight, logistics‑focused snapshot of what’s new and actually moving the needle (≈2024–2025):

### What’s new
- **6D pose—now for brand‑new SKUs**: BOP expanded beyond “known CADs” to **model‑free** onboarding from short reference videos; SOTA accuracy for seen objects is now ~85% AR, and the 2024/25 challenges emphasise cluttered, real‑world bin picking.
- **Diffusion‑based visuomotor policies**: diffusion policies are becoming the default for learned pick/place controllers (stronger multi‑modal action modelling; new work adds test‑time geometry/control priors). Good fit for short‑horizon picking.
- **Foundation/VLMs for open‑vocab picking**: open‑world grasping and VL‑guided manipulation reduce SKU‑specific training and help with long‑tail items.
- **General‑purpose grasp detectors maturing**: AnyGrasp and successors remain a practical baseline for parallel‑jaw bin‑picking, with active SDK updates through 2024.
- **Hard objects (transparent, glossy, deformable)**: stereo+sim2real and depth‑completion pipelines; dedicated transparent‑object grasping with active‑stereo; deformable foods and DLOs tackled with task‑specific pipelines.

### Benchmarks & datasets to watch
- **BOP 2024/25** (6D pose, incl. model‑free tracks).
- **GraspNet‑1Billion** (cluttered RGB‑D grasping; still the workhorse for training/eval).
- **GraspClutter6D** (2025): real‑world clutter for segmentation/pose/grasping; shows gains over older sets.
- **CEPB** (heavily cluttered bin‑picking scenes, photorealistic).
- **SYN‑PBOX** (box‑shaped items; instance seg + pose for bin‑picking).
- **OakInk / OakInk2** (affordances, bimanual/hand–object interactions; useful for policy pretraining/transfer).

### What’s working in production‑adjacent settings
- Pose → grasp stacks on BOP objects for rigid, textured SKUs; increasingly swap‑in **model‑free** onboarding for new items.
- AnyGrasp‑style dense 6‑DoF grasp proposals as a robust default for parallel grippers; model‑free **multi‑suction** planners for totes with mixed shapes.
- Diffusion policies trained from teleop or scripted data for short horizon pick/place; now with test‑time adaptation and constraints.

### Still hard (open problems)
- Transparent/specular packaging and shrink‑wrap: active‑stereo + depth completion helps, but generalisation in clutter remains brittle.
- Deformables & entanglement (apparel, cables, food): progress, but reliable disentangling/picking at scale still researchy.
- Success prediction & handoffs: fewer standardised metrics; most work bakes success scoring into grasp quality or policy value rather than explicit calibrated predictors.

---

## User
Can ypu find me a video?

## Assistant
Here are a couple of great video demos that showcase real-world robot vision in pick-and-place tasks within logistics settings:

- **[DHL’s Supply Chain Robotic Picking Cell (Zivid 3D Vision)](https://www.youtube.com/watch?v=2FAghHTAH40)**  
  A polished demonstration of a DHL automated picking cell powered by Zivid’s 3D vision technology—highly relevant for logistics and bin-picking applications.

- **[Handle Robot Reimagined for Logistics](https://www.youtube.com/watch?v=5iV_hB08Uns)**  
  This video highlights the Handle robot, a mobile manipulation system designed for pallet building and depalletizing, showcasing its application in logistics environments.

| Video | What It Demonstrates | Why It’s Useful |
|-------|----------------------|-----------------|
| DHL + Zivid | Stationary robotic arm with high-fidelity 3D vision, performing bin picking | Shows precision & reliability in supply-chain-grade systems |
| Handle Robot | Mobile manipulator autonomously handling pallets & SKUs | Insight into mobile pick-and-place for flexible logistics setups |

---

## User
Something a little.more academic?

## Assistant
You're looking for a more academic-style video—something rooted in research, focusing on robot vision for pick‑and‑place in logistics domains. I found a stellar one that fits the bill:

- **[Stanford Seminar – Stowing and Picking Items in E‑Commerce Robotics (Aaron Parness, Amazon Robotics)](https://www.youtube.com/watch?v=PrcypjtWse4)**  
  **Why it’s worth your time:**
  - Academic depth: Seminar by Amazon Robotics, covering cutting-edge challenges and solutions.
  - Vision-integrated logistics: Focus on robotic stowing & picking in warehouse automation.
  - Credibility: Presented by a researcher from Amazon Robotics.

Also worth noting:
- Vision + touch pick-and-place demos exist ([example](https://www.youtube.com/watch?v=NihilhQfF1M)).
- Vision-LfD pipelines ([paper](https://www.mdpi.com/1424-8220/22/7/2678)).

---
