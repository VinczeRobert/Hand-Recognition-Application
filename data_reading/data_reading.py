import os
import cv2 as cv
import h5py
import numpy as np
from sklearn.model_selection import train_test_split

from base_constants.general_constants import NUMBER_OF_CLASSES, SPLIT_RATIO, NUMBER_OF_IMAGES, CLASSES, OWN_DATA_PATH, \
    IMAGE_SIZE_X, IMAGE_SIZE_Y
from exceptions import ImageNotLoadedException


class TrainingDataReader:

    def __init__(self):
        """
        attributes:
        training_data: contains data that we will use to train our model
        training_class_labels: actual classes that each training sample belongs to
        testing_data: contains data that we will use to test the accuracy of our trained model
        testing_class_labels: actual classes that each testing sample belongs to
        """
        self.training_data = np.zeros(shape=(NUMBER_OF_IMAGES, IMAGE_SIZE_X, IMAGE_SIZE_Y, 3), dtype='float32')
        self.training_class_labels = np.zeros(shape=NUMBER_OF_IMAGES, dtype='uint8')
        self.testing_data = None
        self.testing_class_labels = None
        self.counter = 0

    def read_training_data(self):
        """
        Obtains folder with data from the next class and calls 'read_data_for_one_class' to actually read the data
        """
        for category in CLASSES:
            path = os.path.join(OWN_DATA_PATH, category)
            class_num = CLASSES.index(category)
            self.read_data_for_one_class(path, class_num)

    def read_data_for_one_class(self, path, class_num):
        """
        Main method of this first part of the project.
        This method gets the path to a folder belonging to one class, iterates through the photos, reads them,
        normalizes them and adds them to the training data, as well as the corresponding class labels.
        """
        print('Currently reading data for class number {}...'.format(class_num))
        for image in os.listdir(path):
            try:
                image_array = cv.imread(os.path.join(path, image), cv.IMREAD_COLOR)

                if image_array.size == 0:
                    raise ImageNotLoadedException

                new_array = cv.resize(image_array, (IMAGE_SIZE_X, IMAGE_SIZE_Y))
                self.training_data[self.counter] = cv.normalize(new_array, None, alpha=0, beta=1,
                                                                norm_type=cv.NORM_MINMAX, dtype=cv.CV_32F)
                self.training_class_labels[self.counter] = class_num
                self.counter = self.counter + 1
            except ImageNotLoadedException as e:
                print(e.get_exception_message())

    def split_data(self):
        """
        Initially the data is only read into the training_data and training_class_labels attributes.
        In this function, it is divided into training and testing data.
        """
        self.training_data, self.testing_data, self.training_class_labels, self.testing_class_labels = \
            train_test_split(self.training_data, self.training_class_labels, test_size = SPLIT_RATIO)

    def save_to_h5(self, file_path):
        """
        Store the numpy image arrays to an H5 file.
        :param file_path: the path where the H5 file will be saved.
        """
        with h5py.File(file_path, 'w') as hf:
            hf.create_dataset("training_data", data=self.training_data)
            hf.create_dataset("training_class_labels", data=self.training_class_labels)
            hf.create_dataset("testing_data", data=self.testing_data)
            hf.create_dataset("testing_class_labels", data=self.testing_class_labels)

    def load_from_h5(self, file_path):
        """
        Load the numpy image arrays from an H5 file.
        :param file_path: the path of the H5 file that data will be loaded from
        """
        with h5py.File(file_path, 'r') as hf:
            self.training_data = hf['training_data'][:]
            self.training_class_labels = hf['training_class_labels'][:]
            self.testing_data = hf['testing_data'][:]
            self.testing_class_labels = hf['testing_class_labels'][:]
