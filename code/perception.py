import numpy as np
import cv2

# Identify pixels above the threshold
# Threshold of RGB > 160 does a nice job of identifying ground pixels only
def color_thresh(img, rgb_thresh=(160, 160, 160)):
    # Create an array of zeros same xy size as img, but single channel
    color_select = np.zeros_like(img[:,:,0])
    # Require that each pixel be above all three threshold values in RGB
    # above_thresh will now contain a boolean array with "True"
    # where threshold was met
    above_thresh = (img[:,:,0] > rgb_thresh[0]) \
                & (img[:,:,1] > rgb_thresh[1]) \
                & (img[:,:,2] > rgb_thresh[2])
    # Index the array of zeros with the boolean array and set to 1
    color_select[above_thresh] = 1
    # Return the binary image
    return color_select

# Identify pixels above the threshold
# Threshold of RGB > 160 does a nice job of identifying ground pixels only
def color_thresh_range(img, rgb_thresh_low=(0, 0, 0), rgb_thresh_high=(255, 255, 255)):
    # Create an array of zeros same xy size as img, but single channel
    color_select = np.zeros_like(img[:,:,0])
    # Require that each pixel be above all three threshold values in RGB
    # above_thresh will now contain a boolean array with "True"
    # where threshold was met
    above_thresh = (img[:,:,0] > rgb_thresh_low[0]) \
                & (img[:,:,1] > rgb_thresh_low[1]) \
                & (img[:,:,2] > rgb_thresh_low[2])

    below_thresh = (img[:,:,0] < rgb_thresh_high[0]) \
                & (img[:,:,1] < rgb_thresh_high[1]) \
                & (img[:,:,2] < rgb_thresh_high[2])
    # Index the array of zeros with the boolean array and set to 1
    color_select[above_thresh & below_thresh] = 1
    # Return the binary image
    return color_select

# Define a function to convert from image coords to rover coords
def rover_coords(binary_img):
    # Identify nonzero pixels
    ypos, xpos = binary_img.nonzero()
    # Calculate pixel positions with reference to the rover position being at the 
    # center bottom of the image.  
    x_pixel = -(ypos - binary_img.shape[0]).astype(np.float)
    y_pixel = -(xpos - binary_img.shape[1]/2 ).astype(np.float)
    return x_pixel, y_pixel


# Define a function to convert to radial coords in rover space
def to_polar_coords(x_pixel, y_pixel):
    # Convert (x_pixel, y_pixel) to (distance, angle) 
    # in polar coordinates in rover space
    # Calculate distance to each pixel
    dist = np.sqrt(x_pixel**2 + y_pixel**2)
    # Calculate angle away from vertical for each pixel
    angles = np.arctan2(y_pixel, x_pixel)
    return dist, angles

# Define a function to map rover space pixels to world space
def rotate_pix(xpix, ypix, yaw):
    # Convert yaw to radians
    yaw_rad = yaw * np.pi / 180
    xpix_rotated = (xpix * np.cos(yaw_rad)) - (ypix * np.sin(yaw_rad))
                            
    ypix_rotated = (xpix * np.sin(yaw_rad)) + (ypix * np.cos(yaw_rad))
    # Return the result  
    return xpix_rotated, ypix_rotated

def translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale): 
    # Apply a scaling and a translation
    xpix_translated = (xpix_rot / scale) + xpos
    ypix_translated = (ypix_rot / scale) + ypos
    # Return the result  
    return xpix_translated, ypix_translated


# Define a function to apply rotation and translation (and clipping)
# Once you define the two functions above this function should work
def pix_to_world(xpix, ypix, xpos, ypos, yaw, world_size, scale):
    # Apply rotation
    xpix_rot, ypix_rot = rotate_pix(xpix, ypix, yaw)
    # Apply translation
    xpix_tran, ypix_tran = translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale)
    # Perform rotation, translation and clipping all at once
    x_pix_world = np.clip(np.int_(xpix_tran), 0, world_size - 1)
    y_pix_world = np.clip(np.int_(ypix_tran), 0, world_size - 1)
    # Return the result
    return x_pix_world, y_pix_world

# Define a function to perform a perspective transform
def perspect_transform(img, src, dst):
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))# keep same size as input image
    mask = cv2.warpPerspective(np.ones_like(img[:,:,0]), M, (img.shape[1], img.shape[0]))
    return warped, mask

def get_perspective_mapping(rover):
    dst_size = 5
    bottom_offset = 6
    x = rover.img.shape[1]
    y = rover.img.shape[0]
    src = np.float32([[14, 140], [301 ,140],[200, 96], [118, 96]])
    dest = np.float32([[x/2 - dst_size, y - bottom_offset], 
                      [x/2 + dst_size, y - bottom_offset],
                      [x/2 + dst_size, y - 2*dst_size - bottom_offset], 
                      [x/2 - dst_size, y - 2*dst_size - bottom_offset]])
    return src, dest


# Apply the above functions in succession and update the Rover state accordingly
def perception_step(rover):
    # Perform perception steps to update Rover()
    # TODO: 
    # NOTE: camera image is coming to you in Rover.img
    # 1) Define source and destination points for perspective transform
    src, dest = get_perspective_mapping(rover)
    

    img = rover.img
    # 2) Apply perspective transform
    warped, mask = perspect_transform(img, src, dest)
    
    # 3) Apply color threshold to identify navigable terrain/obstacles/rock samples
    navigable = color_thresh_range(warped, rgb_thresh_low=(160, 160, 160))
    obstacles = (1-navigable) * mask
    gold = color_thresh_range(warped, rgb_thresh_low=(110, 110, 0), rgb_thresh_high=(255, 255, 50))
    
    # 4) Update Rover.vision_image (this will be displayed on left side of screen)
        # Example: Rover.vision_image[:,:,0] = obstacle color-thresholded binary image
        #          Rover.vision_image[:,:,1] = rock_sample color-thresholded binary image
        #          Rover.vision_image[:,:,2] = navigable terrain color-thresholded binary image
    rover.vision_image[:,:,0] = obstacles
    rover.vision_image[:,:,1] = gold
    rover.vision_image[:,:,2] = navigable

    # 5) Convert map image pixel values to rover-centric coords
    x_rover_nav_coords, y_rover_nav_coords = rover_coords(navigable)
    x_rover_ob_coords, y_rover_ob_coords = rover_coords(obstacles)
    
    # 6) Convert rover-centric pixel values to world coordinates
    xpos = rover.pos[0] #- 15
    ypos = rover.pos[1] #+ 15
    yaw = rover.yaw
    world_size = rover.worldmap.shape[0]
    scale = 10 # TODO: Figure out how to obtain this. It was 2 * dst_size 
    x_world_nav_coords, y_world_nav_coords = pix_to_world(x_rover_nav_coords, y_rover_nav_coords, xpos, ypos, yaw, world_size, scale)
    x_world_ob_coords, y_world_ob_coords = pix_to_world(x_rover_ob_coords, y_rover_ob_coords, xpos, ypos, yaw, world_size, scale)
    
    # 7) Update Rover worldmap (to be displayed on right side of screen)
        # Example: Rover.worldmap[obstacle_y_world, obstacle_x_world, 0] += 1
        #          Rover.worldmap[rock_y_world, rock_x_world, 1] += 1
        #          Rover.worldmap[navigable_y_world, navigable_x_world, 2] += 1
    rover.worldmap[y_world_ob_coords, x_world_ob_coords, 0] = 255
    rover.worldmap[y_world_nav_coords, x_world_nav_coords, 2] = 255
    nav_pix = rover.worldmap[:, :, 2] > 0
    rover.worldmap[nav_pix, 0] = 0
    if gold.any():
        x_rover_gold_coords, y_rover_gold_coords = rover_coords(gold)
        x_world_gold_coords, y_world_gold_coords = pix_to_world(x_rover_gold_coords, y_rover_gold_coords, xpos, ypos, yaw, world_size, scale)
        rover.worldmap[y_world_gold_coords, x_world_gold_coords, 1] = 255

    # 8) Convert rover-centric pixel positions to polar coordinates
    # Update Rover pixel distances and angles
        # Rover.nav_dists = rover_centric_pixel_distances
        # Rover.nav_angles = rover_centric_angles
    rover.nav_dists, rover.nav_angles = to_polar_coords(x_rover_nav_coords, y_rover_nav_coords)
#     mean_dir = np.mean(navigable_angles)
    
    return rover