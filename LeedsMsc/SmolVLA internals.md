
          ┌────────────────────────────────────────┐
                        │               INPUTS                   │
                        └────────────────────────────────────────┘

   Overhead Cam                     Wrist Cam                 Arm State
  (RGB image t)                   (RGB image t)          (joints / EE pose t)
       │                                │                           │
       v                                v                           v
┌───────────────┐              ┌───────────────┐          ┌─────────────────┐
│ Vision Encoder│              │ Vision Encoder│          │ Proprio Encoder │
│   (ViT / CNN) │              │   (ViT / CNN) │          │ (MLP / Linear)  │
└───────────────┘              └───────────────┘          └─────────────────┘
       │                                │                           │
       v                                v                           v
  Img Tokens O_t                    Img Tokens W_t            Proprio Tokens p_t


          Natural Language Inputs (Text)
 ┌─────────────────────────────────────────────────────────┐
 │  "Pick up the red block and place it on the blue one." │
 │  + optional history: previous instructions / summaries │
 └─────────────────────────────────────────────────────────┘
                          │
                          v
                  ┌─────────────────┐
                  │ Text Tokenizer  │
                  │  + Embeddings   │
                  └─────────────────┘
                          │
                          v
                     Text Tokens L_t


                        ┌────────────────────────────────────────┐
                        │        TEMPORAL CONTEXT WINDOW         │
                        │   (last K steps of multimodal tokens)  │
                        └────────────────────────────────────────┘

Time  t-K+1           t-K+2                 …                  t
──────────────┬─────────────────────┬─────────────────────┬──────────────
 Tokens:      │                     │                     │
              │ [O_{t-K+1}, W_{t-K+1}, p_{t-K+1}, L]      │
              │ [O_{t-K+2}, W_{t-K+2}, p_{t-K+2}, L]      │
              │    …                                      │
              │ [O_t,       W_t,       p_t,       L]      │
──────────────┴─────────────────────┴─────────────────────┴──────────────
             (All packed as a single token sequence into the model)


                        ┌────────────────────────────────────────┐
                        │         SMOLVLA CORE MODEL             │
                        └────────────────────────────────────────┘
                                      │
                                      v
         ┌─────────────────────────────────────────────────────────┐
         │         Multimodal Transformer / Policy Backbone       │
         │  - Self-attention over vision + proprio + text tokens  │
         │  - Cross-time reasoning over the context window        │
         │  - Instruction conditioning via text tokens            │
         └─────────────────────────────────────────────────────────┘
                                      │
                                      v
                           ┌───────────────────┐
                           │  Policy Head      │
                           │  (MLP / Linear)   │
                           └───────────────────┘
                                      │
                                      v
                        ┌────────────────────────────┐
                        │   ACTION TOKENS / VECTORS  │
                        └────────────────────────────┘
                                      │
                                      v
   ┌────────────────────────────────────────────────────────────────┐
   │        Low-level control outputs at time t (example)          │
   ├────────────────────────────────────────────────────────────────┤
   │  a_t = [                                                      │
   │    Δq1, Δq2, …, ΔqN,           ← joint deltas or velocities   │
   │    g_open/close,              ← gripper command               │
   │    (optional) mode flags      ← e.g. positional vs velocity   │
   │  ]                                                              │
   └────────────────────────────────────────────────────────────────┘

                                      │
                                      v
                           Robot Controller / Driver
                           (converts a_t into actual
                          motor commands for the arm)