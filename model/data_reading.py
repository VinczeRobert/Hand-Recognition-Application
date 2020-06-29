import os
import cv2 as cv
import numpy as np
from exceptions import ImageNotLoadedException
IMAGE_RESIZE_X = 64
IMAGE_RESIZE_Y = 64


class TrainingDataReader:
    """
    Class used for loading the images into numpy arrays.
    """
    def __init__(self):
        """
        training_data: contains data that we will use to train the model
        training_class_labels: actual classes that each training sample belongs to
        """
        self._training_data = None
        self._training_class_labels = None
        self._counter = 0

    def init_reading(self, dataset_path):
        """
        This method gets the classes and the number of images of the dataset
        and initializes the numpy arrays for the training images and labels.
        :param dataset_path: path to the used dataset
        :return: classes of the dataset
        """

        number_of_images = 0

        for _, _, files in os.walk(dataset_path):
            number_of_images += len(files)

        self._training_data = np.zeros(shape=(number_of_images, IMAGE_RESIZE_X, IMAGE_RESIZE_Y, 3), dtype='float32')
        self._training_class_labels = np.zeros(shape=number_of_images, dtype='uint8')

        classes = next(os.walk(dataset_path))[1]
        return classes

    def read_data_for_one_class(self, path, class_num):
        """
        This method gets the path to a folder belonging to one class, iterates through the pctures, reads them,
        normalizes them and adds them to the training data, as well as the corresponding class labels.
        """
        print('Currently reading data for class number {}...'.format(class_num))
        for image in os.listdir(path):
            try:
                image_array = cv.imread(os.path.join(path, image), cv.IMREAD_COLOR)

                if image_array is None or image_array.size == 0:
                    raise ImageNotLoadedException

                new_array = cv.resize(image_array, (IMAGE_RESIZE_X, IMAGE_RESIZE_Y))
                self._training_data[self._counter] = cv.normalize(new_array, None, alpha=0, beta=1,
                                                                  norm_type=cv.NORM_MINMAX, dtype=cv.CV_32F)
                self._training_class_labels[self._counter] = class_num
                self._counter = self._counter + 1
            except ImageNotLoadedException as e:
                return -1

    def get_training_data(self):
        return self._training_data

    def get_training_class_labels(self):
        return self._training_class_labels
