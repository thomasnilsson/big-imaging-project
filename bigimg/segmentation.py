import cv2
import numpy as np
from skimage.morphology import binary_dilation, binary_erosion, binary_opening, binary_closing, disk

from skimage.morphology import binary_dilation, binary_erosion, binary_opening, binary_closing, disk
import numpy as np
import cv2

def K_means(patient_img):
    """Returns matrix
    Segmententation of patient_img with k-means
    """
    Z = np.float32(np.ravel(patient_img))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness, labels, centers = cv2.kmeans(Z, 2, None, criteria, 10, flags)
    center = np.uint8(centers)
    return labels.reshape(patient_img.shape)

def pat_K_means(patient_img):
    """Returns list
    List of segmented slices with k_means()
    """
    num_slices, height, width = patient_img.shape
    segmented_slices = np.zeros((num_slices, height, width))

    for i in range(num_slices):
        seg_slice = K_means(patient_img[i])
        if seg_slice.sum() > seg_slice.size * 0.5:
            seg_slice = 1 - seg_slice
        segmented_slices[i] = seg_slice

    return segmented_slices


from skimage.morphology import binary_dilation, binary_erosion, binary_opening, binary_closing, disk


def roi_mean_yx(patient_img):
    """Returns mean(y) and mean(x) [double]
    Mean coordinates in segmented patients slices.
    This function performs erosion to get a better result.
    Original: See https://nbviewer.jupyter.org/github/kmader/Quantitative-Big-Imaging-2019/blob/master/Lectures/06-ShapeAnalysis.ipynb
    """
    seg_slices = pat_K_means(patient_img)
    num_slices = seg_slices.shape[0]
    y_all, x_all = np.zeros(num_slices), np.zeros(num_slices)
    neighborhood = disk(2)

    for i, seg_slice in enumerate(seg_slices):
        # Perform erosion to get rid of wrongly segmented small parts
        seg_slices_eroded = binary_erosion(seg_slice, neighborhood)

        # Filter out background of slice, after erosion [background=0, foreground=1]
        y_coord, x_coord = seg_slices_eroded.nonzero()

        # Save mean coordinates of foreground
        y_all[i], x_all[i] = np.mean(y_coord), np.mean(x_coord)

    # Return mean of mean foregrounds - this gives an estimate of ROI coords.
    return np.mean(y_all), np.mean(x_all)