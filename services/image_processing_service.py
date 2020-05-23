from PIL import Image
import numpy as np
import cv2 as cv
from base_constants.general_constants import IMAGE_SIZE_X, IMAGE_SIZE_Y
from model.image_preprocessor import ImagePreprocessor


class ImageProcessingService:
    def __init__(self, hand_index=0, var_threshold=50):
        self.image_preprocessor = ImagePreprocessor(hand_index=hand_index, var_threshold=var_threshold)

    def start_prediction(self):
        self.image_preprocessor.set_background_subtractor()

    def preprocess_image(self, pil_image, is_binary, with_cropping):
        numpy_image = np.asarray(Image.open(pil_image))
        flipped_image = cv.flip(numpy_image, 1)

        preprocessed_image = self.image_preprocessor.prepare_image_for_classification(flipped_image,
                                                                                      is_binary, with_cropping)
        resized_image = cv.resize(preprocessed_image, (IMAGE_SIZE_X, IMAGE_SIZE_Y))
        normalized_image = cv.normalize(resized_image, None, alpha=0, beta=1, norm_type=cv.NORM_MINMAX,
                                        dtype=cv.CV_32F)
        return normalized_image
