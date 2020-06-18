import threading

import cv2 as cv
import numpy as np
from base_constants.constants import IMAGE_SIZE_X, IMAGE_SIZE_Y, CLASSES
from model.cnn_architecture import CNNArchitecture
from model.text_to_speech_converter import TextToSpeechConverter


class Predictor:

    def __init__(self, weights_path):
        self.cnn_architecture = CNNArchitecture()
        self.cnn_architecture.build_model()
        self.cnn_architecture.load_model(weights_path)

        self.text_to_speech_converter = TextToSpeechConverter()

    def predict_hand_gesture(self, image, vocal_mode):
        resized_image = cv.resize(image, (IMAGE_SIZE_X, IMAGE_SIZE_Y))
        cnn_input = np.array(np.zeros(shape=(1, IMAGE_SIZE_X, IMAGE_SIZE_Y, 3)))
        normalized_input = cv.normalize(resized_image, None, alpha=0, beta=1, norm_type=cv.NORM_MINMAX,
                                                    dtype=cv.CV_32F)
        cnn_input[0] = normalized_input

        predicted_class = self.cnn_architecture.predict_classes_for_images(cnn_input)[0]
        new_predicted_letter = CLASSES[predicted_class]

        if vocal_mode:
            voice_thread = threading.Thread(target=self.text_to_speech_converter.convert_text_to_speech,
                                        kwargs={'text': new_predicted_letter})
            voice_thread.start()

        return new_predicted_letter

