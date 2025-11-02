
## Background

NeoIntralogistics is a warehouse automation company. In our system items are stored in bins  which are kept on shelves in isles within a warehouse. When an order is placed in the system, a specialised carrier robot collects the bin and transfers it to a station.

In this station a Universal Robot robot arm takes the bin and places it on a shelf near a human operator. Humans transfer specific items from bins either into a package for direct sending, or into another bin for consolidation with other items.  This process is called picking. There is an opposite process called stowing where items are placed into bins and the robots put them on shelves, once stowed the item is then classified as "in stock" and is ready to sell.

![[Pasted image 20250819130905.png]]

The bins are about the size of a large shoebox and contain a mixture of item types (or SKUs), for example a single bin might contain an iPhone, a teddy bear, a pair of scissors and a T-Shirt. Distribution is random. Usually there's about 5 items per bin. Items can overlap each other in the bin.  

![[Pasted image 20250822114411.png]]

## GAP

The last stage is performed by a human which is expensive. Automating this last step would enable higher throughput at lower cost.

Commercial applications which take items from a container historically require a "model", for example from CAD, for the robot arm to plan a grasp orientation for a successful grab. Dropping the item into a bin or box is then straightforward. Building a library of models for each SKU is expensive and laborious. If possible a model free approach should be adopted. "Model-free approaches are attractive due to their generalization capabilities to novel objects, but are mostly limited to top-down grasps and do not allow a precise object placement which can limit their applicability." [A Survey on Learning-Based Robotic Grasping](https://link.springer.com/content/pdf/10.1007/s43154-020-00021-6.pdf)

Not only do we lack a model of each SKU we also don't have good images of all the items, and in some cases rely on the human to recognise the item from it's description.

Note the more complicated job of "packing" an item is out of scope for the time being, since it would specialised end effectors.

## Title
Evaluating Foundation Models for Model-Free Robotic Bin Picking in Warehouse Automation

## Abstract

This project investigates whether foundation models for vision can enable SKU recognition without exhaustive per-SKU training, and how model-free grasp planning can integrate with segmentation to achieve reliable autonomous picking in warehouse bins. It will also explore confidence-based handover mechanisms to determine when human intervention remains preferable.

## Implementation Approach
Create an automated mechanism which using an RGB (perhaps RGBD) camera and a pretrained foundation model to segment the items in a bin and store a visual feature map against each "segmented" area. Cross reference this against the knowledge we have about the distribution of items to map the features against the actual SKUs. For example if we know a bin was empty and we've just added SKU1 then the item features extracted for that one item are probably SKU1. If bin A has SKU1, SKU2, and bin B SKU2, SKU3 we should be able to map the features for all three from pictures of both. YOLOe looks like a possible to get a set of "parameter". Scanning of items could be performed during stowing process, and/or during "stock taking" events.

At picking time use a pretrained model-free to grasp foundation model to create a grasp affordance map, overlap this with a segmented image from the visual model to restrict the potential grasps to the item we want to pick. If the item can be "seen" and is "pickable" route the bin to the robot arm to be automatically picked, optionally we can then "dig" in the bin to rearrange the items and repeat the process. If the confidence of picking by robot is low, route the bin to a human to pick.  
## Motivation

There are amazing models being released in vision and robotics at the moment, this project serves as a really great way to learn and evaluate the different model types and how they can be used to build the system described. For example, here are some models which may be evaluated:

YOLOe - a segmentation and recognition model which can recognise new objects though a simple 1 shot step that extracts abstract features. The item in question can then be recognised from these abstract features.

VLAs which can take a language description and plan a robot actions, eg pick up the banana.

## Expectation 

#### Taxonomy 
Create a detailed review and taxonomy of foundation models which can help in this area,
#### Prototype 
Create a working prototype on the bench using RGBD (photoneo) and SO100 robots (I have 2 on order). 

#### Evaluation
Evaluate and document the performance of the bench system

#### Stretch
implement the design using a real UR robot.

## Plan

September: 
-  W1 Review image segmentation models, including fusion models (for RGB + D)
-  W2 Design, build, and test camera capture system on the bench
-  W3 Review model-free grasp planning models
-  W4 Build test environment for model-free grasp planning model on the bench (or simulation)
October 
- W1 deploy camera capture system in warehouse (then continually capture images)
- W2 review available public test datasets of bin data (eg **GraspNet‑1Billion**) to augment real image captures, perhaps simulate bin contents 
- W3 + W4 implement process to run segmentation model over bin images and build catalog
November
- W1-2 Evaluate system on the bench
- W2-4 Evaluate system on bench with available datasets
December
	W1 - Evaluate system with real Universal Robot (optional)
	Write up

## Challenges

- Time management
- Low light
- Occluded/overlapping items
- Random Orientation
- Random Labels on things
- Similar looking items (for example items which only differ by label colour)
- Deformable items
- Items where the packaging changes over time for the same SKU (eg Christmas packaging is a -different colour to the normal packaging)

# Appendices

## Literature 

2401.12963v2 Emboddied Models.pdf
2403.19578v3.Keypoint Action Tokens Enable.pdf
2412.15182v1 ROBOT SUB-TRAJECTORY RETRIEVAL FOR.pdf
2503.20020v1 Gemini Brining AI into the Physical World.pdf
Yolo 9000 1612.08242v1.pdf
You Only Look Once 1506.02640v5.pdf

Deep Learning for Detecting Robotic Grasps
[1301.3592](https://arxiv.org/pdf/1301.3592)

Yolo 9000 Better, Faster, Stronger
https://arxiv.org/abs/1612.08242

You Only Look Once: Unified, Real-Time Object Detection
[[1506.02640] You Only Look Once: Unified, Real-Time Object Detection](https://arxiv.org/abs/1506.02640)

## Videos:
[Robotics Today - A Series of Technical Talks](https://roboticstoday.github.io/)
["From SLAM to Spatial AI" - Andrew Davison](https://www.youtube.com/watch?v=lGIM2WVp5t0&t=3s)
[SLAM-Handbook-contributors/slam-handbook-public-release: Release repo for our SLAM Handbook](https://github.com/SLAM-Handbook-contributors/slam-handbook-public-release)

## Competition
- Brightpick
- Amazon

## Simulation Environments

- [MuJoCo — Advanced Physics Simulation](https://mujoco.org/)
- Isaak Sim
- ROS Gazebo 
- Unity and C#