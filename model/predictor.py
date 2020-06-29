import threading
import cv2 as cv
import numpy as np
from model.cnn_architecture import CNNArchitecture
from model.data_reading import IMAGE_RESIZE_X, IMAGE_RESIZE_Y
from model.text_to_speech_converter import TextToSpeechConverter

class Predictor:
    """
    Class responsible for getting the predictions in written mode and
    (optionally) in vocal mode.
    """
    def __init__(self, weights_path, classes):
        self._classes = classes
        self.cnn_architecture = CNNArchitecture.get_instance()
        self.cnn_architecture.build_model(len(classes))
        self.cnn_architecture.load_model(weights_path)

        self.text_to_speech_converter = TextToSpeechConverter()

    def predict_hand_gesture(self, image, vocal_mode):
        """
        Gets prediction for an image.
        :param image: to be predicted
        :param vocal_mode: boolean value which determines if the text has to be also considered to speech
        :return:
        """
        resized_image = cv.resize(image, (IMAGE_RESIZE_X, IMAGE_RESIZE_Y))
        cnn_input = np.array(np.zeros(shape=(1, IMAGE_RESIZE_X, IMAGE_RESIZE_Y, 3)))

        # Frames have to be normalized before sending the mto the CNN
        normalized_input = cv.normalize(resized_image, None, alpha=0, beta=1, norm_type=cv.NORM_MINMAX, dtype=cv.CV_32F)
        cnn_input[0] = normalized_input

        # Directly send frame to CNN and get the prediction
        predicted_class = self.cnn_architecture.predict_classes_for_images(cnn_input)[0]
        new_predicted_letter = self._classes[predicted_class]

        if vocal_mode:
            # Vocal prediction has to be done on a different thread (see TextToSpeechConverter)
            voice_thread = threading.Thread(target=self.text_to_speech_converter.convert_text_to_speech,
                                            kwargs={'text': new_predicted_letter})
            voice_thread.start()

        return new_predicted_letter
