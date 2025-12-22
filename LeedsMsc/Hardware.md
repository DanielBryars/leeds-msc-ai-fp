Robots:

https://neura-robotics.com/

Cameras

Photoneo (owned by Zebra)
https://www.zebra.com/gb/en/products/spec-sheets/industrial-machine-vision-fixed-scanners/3d-sensors/3s-series/3s40.html


Phospho SO-101 Wrist Camera Specifications

  The recommended camera is an InnoMaker 32x32mm USB camera module:

  | Model        | Resolution    | FOV (Diagonal) | FOV (Horizontal) | FOV (Vertical)* |
  |--------------|---------------|----------------|------------------|-----------------|
  | U20CAM-720P  | 720p @ 30fps  | 120°           | 102°             | ~86°            |
  | U20CAM-1080P | 1080p @ 30fps | 130°           | 103°             | ~71°            |

  *Vertical FOV calculated from horizontal FOV and aspect ratio

  For MuJoCo fovy setting:

  - If using 640x480 (4:3): fovy="85" to fovy="90"
  - If using 1080p (16:9): fovy="70" to fovy="75"

  Physical specs:

  - PCB: 32 x 32 x 6.5mm
  - Mounting: 4x M2 screw holes
  - Lens: M12 thread (swappable)
  - Manual focus adjustment via lens rotation

  Your current fovy="75" is a reasonable middle-ground. If you want to match the 720p camera at 640x480, bump it up to ~85°.

  Sources:
  - https://github.com/TheRobotStudio/SO-ARM100/tree/main/Optional/SO101_Wrist_Cam_Hex-Nut_Mount_32x32_UVC_Module
  - https://www.inno-maker.com/product/u20cam-720p/
  - https://www.inno-maker.com/product/u20cam-1080p/
  - https://docs.phospho.ai/learn/cameras






