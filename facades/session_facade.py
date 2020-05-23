import numpy as np

from base_constants.general_constants import IMAGE_SIZE_X, IMAGE_SIZE_Y
from services.cnn_service import CNNService
from services.image_processing_service import ImageProcessingService


class SessionFacade:
    def __init__(self):
        self.cnn_service = CNNService()
        self.image_processing_service = ImageProcessingService()

    def start_prediction(self):
        self.image_processing_service.start_prediction()

    def get_prediction_for_image(self, image, is_binary=False, with_cropping=False):
        normalized_image = self.image_processing_service.preprocess_image(image, is_binary, with_cropping)
        cnn_input = np.array(np.zeros(shape=(1, IMAGE_SIZE_X, IMAGE_SIZE_Y, 3)))
        cnn_input[0] = normalized_image

        predicted_letter = self.cnn_service.predict_class(cnn_input)
        return predicted_letter






