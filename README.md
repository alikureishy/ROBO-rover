[//]: # (Image References)

[image1]: misc/rover_image.jpg
[image2]: ./calibration_images/example_grid1.jpg
[image3]: ./calibration_images/example_rock1.jpg 

![alt text][image1]
[![image1][VehicleDetector1]](https://www.youtube.com/watch?v=m11V6zPe1YY "Click to see video on youtube")

# Project: Search and Sample Return

## Overview

This is the first project of Udacity's Robotics Nanodegree program. It involves programming a rover to navigate unknown territory (presumably on another planet like Mars) that had a sprinkling of gold rocks.

The primary [goal](https://review.udacity.com/#!/rubrics/916/view) was to have the rover explore at least 40% of the ground truth, with at least 60% fidelity, and to locate at least 1 gold rock in the process.

The ultimate goal (still a work-in-progress) is to explore the majority of the ground truth, or at least enough to be able to locate and pick-up all 6 gold rocks in the process, and to then return to the original position where the rover had started out, all within a reasonable amount of time. This requires more advanced algorithms for improving exploration efficiency, seeking out and picking up rocks whenever visible, increasing mapping fidelity, and developing an efficient return strategy.

Here I'll talk about the approach I took for the primary goal above -- what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further. (I will update this with additional implementation details for the more advanced challenges above later).

---
## Implementation

### Notebook Illustration

#### Perception
Perception involves sensing and keeping track of the environment. The rover keeps track of 3 pieces of information:
- Navigable terrain
- Obstacles
- Gold

...along 3 coordinate systems:
- The image coordinates
- The rover coordinates
- The world coordinates

It determines all of these by performing color thresholding on the input image, followed then by coordinate transformation/rotations etc.

Though it could theoretically be possible to utilize just the world coordinates, having these different systems makes things easier. This will be clear in the decision step, described in the next section.

Color thresholding is done for just 2 items -- the bright sand on which the rover is moving, and the golden rocks that it is eventually to pick up. Anything else in the line of sight that is not those two, is considered an obstacle. After conversion into the different coordinate systems, the pixels comprising these regions are then set with corresponding colors on the world map, for visualization, and that information is stored in the rover information object. The same information, expressed in the rover coordinate system, is also stored.

#### Test video
Please see the github repository for the output file (output/test_mapping.mp4).

### Rover In Action

#### Perception

The perception processing from the notebook section above is pretty much replicated here, except that here it is stored in a rover data object.

#### Decision

The decision step involves the following strategy:

'''
There are 2 modes : 'forward' and 'stop'.
If the rover is in 'forward' mode:
   If there is an obstacle:
      Break
      Stop steering
   Else:
      If velocity is less than max:
         Set throttle to max
      Else:
         Stop throttling
      Steer toward mean of availalbe navigable angles
Else if rover is in 'stop' mode:
   If we're still moving:
      Break
      Stop steering
   Else:
      If there is an obstacle:
         Steer right by 15 degrees
      Else:
         Set throttle to max
         Steer towards mean of available navigable angles
'''

The above decision step is taken at each time step (i.e, frame), but it is often the case that an action (such as breaking, or accelerating, or steering) can be spread across multiple such decision steps. This actually simplifies the operation of the rover. The incremental approach to executing actions helps it to adapt those actions quickly to changes in the input.




