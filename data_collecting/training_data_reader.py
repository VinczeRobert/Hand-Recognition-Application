from hyper_parameters.constants import TRAINING_DATA_FOLDER
from hyper_parameters.hyper_parameters import NUMBER_OF_CLASSES, CLASSES
import sys
import os
import numpy as np
import cv2 as cv


class TrainingDataReader:

    def __init__(self):
        self.number_of_classes = NUMBER_OF_CLASSES
        self.training_data = np.zeros(shape=(87000, 64, 64, 3), dtype='float32')
        self.class_labels = np.zeros(shape=87000, dtype='uint8')

    def read_training_data(self):
        for category in CLASSES:
            path = os.path.join(sys.argv[1], TRAINING_DATA_FOLDER, TRAINING_DATA_FOLDER, category)
            class_num = CLASSES.index(category)
            self.read_data_for_one_class(path, class_num)

    def read_data_for_one_class(self, path, class_num):
            print('Currently reading data for class number {}...'.format(class_num))
            counter = class_num * 3000
            for image in os.listdir(path):
                try:
                    image_array = cv.imread(os.path.join(path, image), cv.IMREAD_COLOR)
                    new_array = cv.resize(image_array, (64, 64))
                    self.training_data[counter] = cv.normalize(new_array, None, alpha=0, beta=1, norm_type=cv.NORM_MINMAX, dtype=cv.CV_32F)
                    self.class_labels[counter] = class_num
                    counter = counter + 1
                except Exception as e:
                    pass

