import numpy as np
import cv2

def rescale_patient_4d_imgs(patient):
    img_4d = patient.images
    if len(img_4d.shape) < 4: raise Exception("Patient images are not 4D!")
    num_slices, time, height, width = img_4d.shape
    col, row = patient.col_scaling, patient.row_scaling
    scaled_height = int(height * row)
    scaled_width = int(width * col)
    scaled_imgs = np.zeros((num_slices, time, scaled_height, scaled_width))
    
    for i in range(num_slices):
        for j in range(time):
            scaled_imgs[i,j] = cv2.resize(src=img_4d[i,j], dsize=None, fx=col, fy=row)
    
    return scaled_imgs

def crop_roi(img, dim_y, dim_x, cy, cx):
    """
    Crops an image from the given coords (cy, cx), such that the resulting img is of
    dimensions [dim_y, dim_x], i.e. height and width.
    Resulting image is filled out from top-left corner, and remaining pixels are left black.
    """
    cy, cx = int(round(cy)), int(round(cx))
    h, w = img.shape
    if dim_x > w or dim_y > h: raise ValueError('Crop dimensions larger than image dimension!')
    new_img = np.zeros((dim_y, dim_x))
    dx, dy = int(dim_x / 2), int(dim_y / 2)
    dx_odd, dy_odd = int(dim_x % 2 == 1), int(dim_y % 2 == 1)

    # Find boundaries for cropping [original img]
    dx_left = max(0, cx - dx)
    dx_right = min(w, cx + dx + dx_odd)
    dy_up = max(0, cy - dy)
    dy_down = min(h, cy + dy + dy_odd)

    # Find how many pixels to fill out in new image
    range_x = dx_right - dx_left
    range_y = dy_down - dy_up
    

    # Fill out new image from top left corner
    # Leave pixels outside range as 0's (black)
    new_img[0:range_y, 0:range_x] = img[dy_up:dy_down, dx_left:dx_right]
    return new_img