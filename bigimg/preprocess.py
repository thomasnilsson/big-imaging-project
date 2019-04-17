import numpy as np


# def preprocess_patient(patient_data, min_height, min_width):
#     num_slices, time, height, width = patient_data.images.shape
#     new_img_data = np.zeros((num_slices, time, min_height, min_width))
#     for i in range(num_slices):
#         for j in range(time):
#             img_2d = patient_data.images[i, j]
#             new_img_data[i,j] = crop_roi(img_2d, min_height, min_width)
#     return new_img_data


def crop_roi(img, dim_y, dim_x, cy, cx):
    """
    Crops an image from the given coords (cy, cx), such that the resulting img is of
    dimensions [dim_y, dim_x], i.e. height and width.
    Resulting image is filled out from top-left corner, and remaining pixels are left black.
    """
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