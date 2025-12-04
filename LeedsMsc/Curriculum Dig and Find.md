
I’d think of it as a **curriculum**:

---

## 1. Phase 1 – One block, but “future-proofed”

You’re already here.

Design this so it **extends naturally** to multiple blocks later:

- **Always mention the colour even if there’s only one block.**
    
    - e.g. “Move the **red** block from the left square to the right square.”
        
    - That way the model already treats _colour_ as part of the semantics, not a later bolt-on.
        
- Keep doing what we discussed:
    
    - Multiple start poses
        
    - All (source, target) combos between your tape regions
        
    - LLM-generated paraphrases per episode, but **all consistent** with the behaviour
        

Aim:  
Robot reliably moves the single red block around all regions from natural language commands.

---

## 2. Phase 2 – Multiple coloured blocks, no occlusion

Now add 2–3 blocks (e.g. red, blue, yellow) **fully visible** on the mat.

Design the dataset so the instruction–behaviour mapping is crystal clear:

- Instructions like:
    
    - “Move the **blue block** to the left square.”
        
    - “Put the **red block** on the triangle.”
        
- Constraints:
    
    - The robot **must always move the requested colour** and never the others.
        
    - Randomise positions of all blocks each episode so the model can’t just memorise “leftmost block = red”.
        

Your auto-labelling pipeline can now:

1. Identify **start and end regions** (like before)
    
2. Also classify **which colour block** moved
    
3. Generate instructions:
    
    - “Move the blue block from [start] to [end].”
        
    - Plus paraphrases.
        

This phase teaches:

- Colour grounding
    
- “Pick the specified one, ignore distractors”
    

Even here, you’ll see a big jump: it starts to look like “finding” the correct block.

---

## 3. Phase 3 – Mild clutter and partial occlusion

Before full “digging”, add **gentle occlusion**:

- Blocks slightly overlapping
    
- One partially behind another
    
- Maybe some neutral clutter that should be ignored
    

Instructions stay the same:

- “Move the blue block to the right square.”
    

What changes is the **visual complexity**, so the model must rely on:

- Colour
    
- Shape
    
- Context
    

rather than “isolated nice block in the middle of the frame”.

Your pipeline still works: it just has harder images to classify, but that’s fine.

---

## 4. Phase 4 – Actual “digging” behaviour

Now you move into the “this would be completely awesome” zone.

Here you need to decide what “digging” means operationally:

- Examples:
    
    - Pushing other blocks aside until the red one is reachable
        
    - Grasping and moving occluding blocks to a “parking” region
        
    - Then finally grasping the target block
        

You’ll likely need _multi-step_ demonstrations:

1. Clear space / move occluders
    
2. Grab target block
    
3. Place in goal region
    

Instructions might be:

- “Dig out the red block and place it in the left square.”
    
- “Move the other blocks away and put the blue block on the triangle.”
    

As long as every demo **faithfully follows the instruction**, the VLA can, in principle, learn “clear then pick” as a pattern.

You can still use the start/end-frame pipeline for:

- Identifying **which block ended where**
    
- Which regions became clear
    
- Generating grounded descriptions.
    

If you want to be fancy later, you can add intermediate frame analysis, but you don’t need that to start.

---

## 5. Will this help performance even on the “simple” task?

Yes:

- Starting now with **colour in the instruction**, even with a single block, means:
    
    - Later “find the blue block” is just a natural extension.
        
- Instruction paraphrasing plus growing visual complexity:
    
    - Improves robustness even when it’s just “move the red block from A to B”.
        
- The same SmolVLA policy can slowly **grow its repertoire**:
    
    - one block → many blocks → clutter → digging  
        without throwing away earlier work.
        

---

If you like, next step we can sketch a **minimal data schema** for your episodes, something like:

`episode_id source_region target_region target_color distractor_colors[] occlusion_level`

so you don’t have to restructure anything later when you go from 1 block → many blocks → digging