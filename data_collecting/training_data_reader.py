from hyper_parameters.constants import TRAINING_DATA_FOLDER
from hyper_parameters.hyper_parameters import NUMBER_OF_CLASSES, CLASSES
import sys
import os
import cv2 as cv
import numpy

class TrainingDataReader:

    def __init__(self):
        self.number_of_classes = NUMBER_OF_CLASSES
        self.training_data = []

    def read_training_data(self):
        for category in CLASSES:
            path = os.path.join(sys.argv[1], TRAINING_DATA_FOLDER, TRAINING_DATA_FOLDER, category)
            class_num = CLASSES.index(category)
            self.read_data_for_one_class(path, class_num)

        # self.inputs = numpy.array(self.inputs)
        # self.class_labels = numpy.array(self.class_labels)

    def read_data_for_one_class(self, path, class_num):
            print('Currently reading data for class number {}...'.format(class_num))
            for image in os.listdir(path):
                try:
                    image_array = cv.imread(os.path.join(path, image), cv.IMREAD_COLOR)
                    new_array = cv.resize(image_array, (64, 64))
                    self.training_data.append([new_array, class_num])
                except Exception as e:
                    pass

