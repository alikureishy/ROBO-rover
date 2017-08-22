[//]: # (Image References)

[image1]: ./misc/rover_image.jpg
[image2]: ./calibration_images/example_grid1.jpg
[image3]: ./calibration_images/example_rock1.jpg 

[![image1][VehicleDetector1]](https://www.youtube.com/watch?v=m11V6zPe1YY "Click to see video on youtube")

# Project: Search and Sample Return

## Overview

This is the first project of Udacity's Robotics Nanodegree program. It involves programming a rover to navigate unknown territory (presumably on another planet like Mars) that had a sprinkling of gold rocks.

The primary [goal](https://review.udacity.com/#!/rubrics/916/view) was to have the rover explore at least 40% of the ground truth, with at least 60% fidelity, and to locate at least 1 gold rock in the process.

The ultimate goal (still a work-in-progress) is to explore the majority of the ground truth, or at least enough to be able to locate and pick-up all 6 gold rocks in the process, and to then return to the original position where the rover had started out, all within a reasonable amount of time. This requires more advanced algorithms for improving exploration efficiency, seeking out and picking up rocks whenever visible, increasing mapping fidelity, and developing an efficient return strategy.

Here I'll talk about the approach I took for the primary goal above -- what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further. (I will update this with additional implementation details for the more advanced challenges above later).

---
## Implementation

### Perception

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

### Decision

The decision step 


## Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.
Here is an example of how to include an image in your writeup.

![alt text][image1]

#### 1. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result. 
And another! 

![alt text][image2]





![alt text][image3]


