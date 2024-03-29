import pydicom as dicom
import re
import os
import numpy as np



class Patient(object):
    def __init__(self, directory, subdir):
        # deal with any intervening directories
        while True:
            subdirs = next(os.walk(directory))[1]
            if len(subdirs) == 1:
                directory = os.path.join(directory, subdirs[0])
            else:
                break

        slices = []
        for s in subdirs:
            m = re.match("sax_(\d+)", s)
            if m is not None:
                slices.append(int(m.group(1)))

        slices_map = {}
        first = True
        times = []
        for s in slices:
            files = next(os.walk(os.path.join(directory, "sax_%d" % s)))[2]
            offset = None

            for f in files:
                m = re.match("IM-(\d{4,})-(\d{4})\.dcm", f)
                if m is not None:
                    if first:
                        times.append(int(m.group(2)))
                    if offset is None:
                        offset = int(m.group(1))

            first = False
            slices_map[s] = offset

        self.directory = directory
        self.time = sorted(times)
        self.slices = sorted(slices)
        self.slices_map = slices_map
        self.name = subdir

    def _filename(self, s, t):
        fname = os.path.join(self.directory,
                                 "sax_%d" % s, 
                                 "IM-%04d-%04d.dcm" % (self.slices_map[s], t))
        return fname

    def _read_dicom_image(self, filename):
        d = dicom.read_file(filename)
        img = d.pixel_array
        return np.array(img)

    def _read_all_dicom_images(self):
        f1 = self._filename(self.slices[0], self.time[0])
        f2 = self._filename(self.slices[1], self.time[0])
        
        d1 = dicom.read_file(f1)
        d2 = dicom.read_file(f2)
        
        (x, y) = d1.PixelSpacing
        (x, y) = (float(x), float(y))
        self.col_scaling = x
        self.row_scaling = y
        
        # try a couple of things to measure distance between slices
        try:
            dist = np.abs(d2.SliceLocation - d1.SliceLocation)
        except AttributeError:
            try:
                dist = d1.SliceThickness
            except AttributeError:
                dist = 8  # better than nothing...

        self.images = np.array([[self._read_dicom_image(self._filename(d, i))
                                 for i in self.time]
                                for d in self.slices])
        self.dist = dist
        self.area_multiplier = x * y

    def load(self):
        self._read_all_dicom_images()
        
def load_patient(patient_id, root_dir=None):
    if not root_dir: 
        root_dir =  os.path.join('..', 'input', 'train', 'train')
    patient_id = str(patient_id)
    base_path = os.path.join(root_dir, patient_id)
    try:
        tdata = Patient(base_path, patient_id)
        tdata.load()
        # If data does not contain 4 dimensions, throw it away
        if len(tdata.images.shape) == 4:
            return tdata
    except (ValueError, TypeError, IndexError, AttributeError, FileNotFoundError):
        print('Patient %s could not be loaded.' % patient_id)
        return None