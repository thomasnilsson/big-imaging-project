import numpy as np
import matplotlib.pyplot as plt
from skimage.util import montage as montage2d
montage3d = lambda x, **k: montage2d(np.stack([montage2d(y, **k) for y in x], 0))


def plot_patient_slices_3d(patient_slices, title=False, figsize=(20, 20)):
    '''Plots a 2D image per slice in series (3D in total)'''
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    image = montage2d(patient_slices)
    if title: ax.set_title(title)
    ax.imshow(image, cmap='bone')


def plot_patient_data_4d(patient_data, all_slices=False, num_slices=[0], figsize=(20, 20)):
    '''Plots a 3D image per time step in patient data (4D in total)'''
    if all_slices:
        # Number of slices is equal to the first dimension of the patient image array
        num_slices = range(patient_data.images.shape[0])
    for i in num_slices:
        plot_patient_slices_3d(patient_data.images[i],
                               title=('Showing slice %i' % i))