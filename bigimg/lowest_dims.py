import numpy as np
from bigimg.load_data import *


def find_min_dims(patients):
    '''
    Finds the lowest dimensions (height, width) of images among the patients
    '''
    min_width, min_height = np.infty, np.infty
    for p in patients:
        min_height = min(min_height, p.images.shape[2])
        min_width = min(min_width, p.images.shape[3])
    print("Lowest dims: ", min_height, ",", min_width)
    return min_height, min_width


def batch_min_dims(batch_size=10, all_ids=range(1, 501)):
    batch_results = np.zeros((batch_size, 2))
    id_batches = np.array_split(all_ids, batch_size)

    for i, ids in enumerate(id_batches):
        print('Processing batch %i / %i...' % ((i + 1), batch_size))
        patient_batch = load_multiple_patients(patient_ids=ids)
        batch_results[i] = find_min_dims(patient_batch)
        # Delete batch to avoid RAM hogging
        del patient_batch

    # Return min height & width for all batches
    return batch_results.min(axis=0)