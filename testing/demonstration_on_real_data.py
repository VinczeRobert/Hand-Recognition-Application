"""
Run this file to load one test image for each class and display the images with their
predicted classes and actual classes.
"""

import os
import cv2 as cv
import numpy as np
from cnn_architecture.cnn_architecture import CNNArchitecture
from constants.general_constants import OWN_DATA_PATH
from exceptions import ImageNotLoadedException
from visualization.image_viewer import ImageViewer


if __name__ == '__main__':
    path = OWN_DATA_PATH
    # Initializing numpy arrays
    testing_data = np.zeros(shape=(29, 64, 64, 3), dtype='float32')
    class_labels = np.zeros(shape=29, dtype='uint8')

    # Reading, resizing and normalizing images
    counter = 0
    for image in os.listdir(path):
        try:
            image_array = cv.imread(os.path.join(path, image), cv.IMREAD_COLOR)
            if image_array.size == 0:
                raise ImageNotLoadedException

            resized_array = cv.resize(image_array, (64, 64))
            testing_data[counter] = cv.normalize(resized_array, None, alpha=0, beta=1, norm_type=cv.NORM_MINMAX, dtype=cv.CV_32F)
            class_labels[counter] = counter
            counter = counter + 1
        except ImageNotLoadedException as e:
            print(e.get_exception_message())

    # Creating the model, loading the weights and getting the predictions
    cnn_architecture = CNNArchitecture()
    cnn_architecture.build_model()
    cnn_architecture.model.load_weights('../data/weights/weights.ckpt')
    predicted_classes = cnn_architecture.predict_classes_for_images(testing_data)

    image_viewer = ImageViewer()

    # Iterating through images, adding them to a plot and displaying them
    row = 5
    col = 6
    for idx in range(1, 30):
        index = idx - 1
        image_viewer.plot_image(testing_data[index], predicted_classes[index], class_labels[index], row, col, idx)
    image_viewer.show_plot()
