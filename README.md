# Leeds MSc AI - Final Project Research

Research notes and documentation for an MSc AI final year project focused on automated warehouse bin picking using computer vision and robotics.

## Project Overview

This project explores automated bin picking for warehouse operations, specifically investigating model-free approaches to enable robotic systems to grasp and manipulate items without requiring pre-existing CAD models or extensive labeled datasets.

### Problem Statement

In warehouse automation systems, items are stored in bins containing multiple different products (SKUs). Current systems require human operators to pick items from bins, which is expensive and limits throughput. Automating this "last mile" of warehouse automation is challenging because:

- No CAD models exist for most items
- Items vary in shape, size, and packaging
- Items overlap and occlude each other in bins
- Lighting conditions vary
- Items may be deformable or have changing packaging

### Research Focus

The project investigates using foundation models and modern computer vision techniques to:

1. **Segment and recognize items** in bins using RGB/RGBD cameras and pre-trained models (e.g., YOLOe)
2. **Build item catalogs** automatically through self-supervised learning during stowing operations
3. **Generate grasp affordances** using model-free grasp planning models
4. **Decide robot vs human handling** based on confidence scores for pickability

## Research Topics Explored

The repository contains research notes on several key areas:

- **Vision Language Action (VLA) Models** - Models that can plan robot actions from language descriptions
- **Zero-Shot Learning** - Recognizing new objects without explicit training
- **SLAM and Robotics** - Simultaneous Localization and Mapping techniques
- **Bin Picking Datasets** - Including GraspNet-1Billion and others
- **Foundation Models** - Adapting models like CLIP and SAM for warehouse domains
- **Grasp Planning** - Model-free approaches to predicting successful grasps

## Proposed Research Ideas

Several potential thesis directions are documented, including:

1. Automated stock-taking with RGBD vision
2. Self-supervised item library creation
3. Pickability prediction for robot/human handover
4. Active vision for multi-angle bin scanning
5. Uncertainty-aware perception in bin picking
6. Domain-specific foundation model adaptation

## Project Timeline

- **September**: Review image segmentation and grasp planning models, build test bench
- **October**: Deploy camera system, evaluate datasets, build item catalog
- **November**: System evaluation on bench and with datasets
- **December**: Optional real robot evaluation, write-up

## Technologies & Approaches

- RGB-D cameras for 3D scene understanding
- YOLOe for object segmentation and recognition
- Foundation models for vision (CLIP, SAM)
- Model-free grasp planning
- Universal Robots (UR) arms
- SO100 robots for bench testing
- Self-supervised learning for item recognition

## Repository Structure

- `LeedsMsc/` - Main research notes and documentation
  - `Proposal.md` - Detailed project proposal
  - `Proposal Ideas.md` - Alternative research directions
  - `Papers and Interesting Models.md` - Literature review
  - `Datasets.md` - Relevant datasets for training and evaluation
  - `Key Players.md` - Companies and researchers in the field
  - `robotics_glossary.md` - Key terms and concepts
  - Various topic-specific notes on VLA, SLAM, fusion models, etc.

## Use Case: NeoIntralogistics

The research is motivated by a real warehouse automation scenario where:
- Bins (~shoebox size) contain ~5 mixed items on average
- Items are stored on shelves and retrieved by carrier robots
- Human operators currently perform picking at stations
- Goal: Automate picking to increase throughput and reduce costs

## Key Challenges

- Occlusion and overlapping items
- Random orientation and positioning
- Variable lighting conditions
- Items with similar appearance
- Deformable objects
- Changing packaging (e.g., seasonal variations)
- No pre-existing item models or training data

## Related Work

This research builds on recent advances in:
- Model-free robotic grasping
- Foundation models for vision and robotics
- Self-supervised learning
- Uncertainty quantification in perception
- Active perception strategies
