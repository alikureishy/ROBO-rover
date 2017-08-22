[//]: # (Image References)

[RoverImage]: misc/rover_image.jpg
[GridExample]: https://github.com/safdark/ROBO-rover/blob/master/calibration_images/example_grid1.jpg
[GoldExample]: https://github.com/safdark/ROBO-rover/blob/master/calibration_images/example_rock1.jpg

[![GridExample][GridExample]](https://www.youtube.com/watch?v=m11V6zPe1YY "Click to autonomous rover video")

# Project: Search and Sample Return

## Overview

This is the first project of Udacity's Robotics Nanodegree program. It involves programming a rover to navigate unknown territory (presumably on another planet like Mars) that had a sprinkling of gold rocks.

The primary [goal](https://review.udacity.com/#!/rubrics/916/view) was to have the rover explore at least 40% of the ground truth, with at least 60% fidelity, and to locate at least 1 gold rock in the process.

The ultimate goal (still a work-in-progress) is to explore the majority of the ground truth, or at least enough to be able to locate and pick-up all 6 gold rocks in the process, and to then return to the original position where the rover had started out, all within a reasonable amount of time. This requires more advanced algorithms for improving exploration efficiency, seeking out and picking up rocks whenever visible, increasing mapping fidelity, and developing an efficient return strategy.

Here I'll talk about the approach I took for the primary goal above -- what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further. (I will update this with additional implementation details for the more advanced challenges above later).

---
## Implementation

### Notebook Illustration

Please see [here](https://github.com/safdark/ROBO-rover/blob/master/code/Rover_Project_Test_Notebook.ipynb) for the notebook illustrations and image/video outputs.

#### Process-Image
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

Here is the psuedocode for the perception step, given an input image from the front-facing camera:

```
Warp the image by transforming the perspective to birds-eye view
Threshold the warped image to extract image-based coordinates for:
   Navigable pixels
   Obstacles
   Gold pixels
   Save this information in a "vantage map"
Transform the 3 items above to rover-based coordinates:
   Save this information in a "vision map"
Transform the 3 items above to world-based coordinates:
   Save this information in a "world map"
Transform the rover-based navigation coordinates into polar coordinates:
   Save this information in a "polar map" (this helps to calculate the forward steering angle)
```

#### Test video
Available [here](https://github.com/safdark/ROBO-rover/blob/master/output/test_mapping.mp4)

### Rover In Action

#### Perception

The perception processing from the Process-Image notebook section above is replicated here, except that here it is stored in a rover data object.

#### Decision

The decision step involves the following strategy:

```
There are 2 modes : 'forward' and 'stop'.
If there is navigation information available:
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
Else: (If no navigation information is present)
   Set throttle to max
   Steer forward
```

The above decision step is taken at each time step (i.e, frame), but it is often the case that an action (such as breaking, or accelerating, or steering) can be spread across multiple such decision steps. This actually simplifies the operation of the rover. The incremental approach to executing actions helps it to adapt those actions quickly to changes in the input.

New modes can be added to the rover to optimize its behavior. The behavior above is a very simple approach that fulfills the basic project rubric. I will be optimizing this eventually and will update this document at that time.



