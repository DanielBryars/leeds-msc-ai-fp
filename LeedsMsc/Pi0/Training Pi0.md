
This guy used both cameras as wrist and so on which is interesting!!!!

[(516) Pi0 - generalist Vision Language Action policy for robots (VLA Series Ep.2) - YouTube](https://www.youtube.com/watch?v=ejk6-ffDXFw&t=25s)


[openpi — Trossen Robotics Trossen Arm Documentation](https://docs.trossenrobotics.com/trossen_arm/v1.9/tutorials/openpi.html?utm_source=chatgpt.com)


Need to make a policy + 

And then add a class in here for a train config
training/config.py

I should do LORA and NOT LORA.


AHHH DELTA VS ACTION ACTIONS, this needs sorting.
Some dude has made a policy for Pi0 with 101

So we need a mask too

5000 steps aparently are more than enough???? Acording to Ilia.

[Comparing Physical-Intelligence:main...Maelic:main · Physical-Intelligence/openpi](https://github.com/Physical-Intelligence/openpi/compare/main...Maelic:openpi-SO100:main)


Interesting in Pi0.5 there are two different training losses:
1) loss on the actions predicted. all the way through
2) some sort of freezing of the VLM and only train the head.


