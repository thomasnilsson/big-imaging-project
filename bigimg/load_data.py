import os
import numpy as np
from pandas.compat import FileNotFoundError
from bigimg.patient import Patient


def load_patient(patient_id, root_dir=None):
    """
    Loads one [Patient] object
    :param patient_id: id of the patient [integer]
    :param root_dir: name of root dir, defaults to Kaggle root directory [string]
    :return:
    """
    if not root_dir:
        root_dir = os.path.join('..', 'input', 'train', 'train')
    patient_id = str(patient_id)
    base_path = os.path.join(root_dir, patient_id)
    try:
        patient_data = Patient(base_path, patient_id)
        patient_data.load()
        # If data does not contain 4 dimensions, throw it away
        if len(patient_data.images.shape) == 4:
            return patient_data
    except (ValueError, TypeError, IndexError, AttributeError, FileNotFoundError):
        print('Patient %s could not be loaded.' % patient_id)
        return None


def load_multiple_patients(patient_ids=False, root_dir=None, verbose=False):
    """
    :param patient_ids: ids of patients to load [list of integers]
    :param root_dir: name of root dir, defaults to Kaggle root directory [string]
    :param verbose: Whether to print every patient id when loading [boolean]
    :return: list of [Patient] objects
    """
    # If no ids are specified load all from 1-500
    if not patient_ids:
        patient_ids = range(1, 501)
    patient_list = []
    for pid in patient_ids:
        if verbose:
            print('Loading patient %i...' % pid)
        p_data = load_patient(pid, root_dir=root_dir)
        if p_data:
            patient_list.append(p_data)
    return patient_list


def find_min_dims(patients):
    """
    Finds the lowest dimensions (height, width) of images among the patients
    :param patients: Array of type Patient
    :return: min_height, min_width (int, int)
    """
    min_width, min_height = np.infty, np.infty
    for p in patients:
        min_height = min(p.images.shape[2], min_height)
        min_width = min(p.images.shape[3], min_width)
    print("Lowest dims: ", min_height, ",", min_width)
    return min_height, min_width
