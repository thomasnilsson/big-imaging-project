import numpy as np


# Based on https://gist.github.com/ajsander/fb2350535c737443c4e0#file-tutorial-md
def fourier_time_transform_slice(image_3d):
    '''
    3D array -> 2D array
    [slice, height, width] -> [height, width]
    Returns (width, height) matrix
    Fourier transform for 3d data (time,height,weight)
    '''
    # Apply FFT to the selected slice
    fft_img_2d = np.fft.fftn(image_3d)[1, :, :]
    return np.abs(np.fft.ifftn(fft_img_2d))


def fourier_time_transform(patient_images):
    '''
    4D array -> 3D array (compresses time dimension)
    Concretely, [slice, time, height, width] -> [slice, height, width]
    Description: Fourier transform for analyzing movement over time.
    '''

    ftt_image = np.array([
        fourier_time_transform_slice(patient_slice)
        for patient_slice in patient_images
    ])
    return ftt_image