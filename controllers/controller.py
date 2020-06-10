import sys
import threading
import cv2 as cv
import numpy as np
from PyQt5 import QtWidgets

from base_constants.general_constants import IMAGE_SIZE_Y, IMAGE_SIZE_X, CLASSES, HAND, WEIGHTS_RIGHT_PATH, \
    WEIGHTS_LEFT_PATH
from model.cnn_architecture import CNNArchitecture
from model.frame_captor import FrameCaptor
from model.frame_displayer import FrameDisplayer
from model.image_preprocessor import ImagePreprocessor
from model.text_to_speech_converter import TextToSpeechConverter
from view.hand_gesture_recognition_view import HandGestureRecognitionView


class Controller:
    def __init__(self, camera_init_url='', hand_index=0,
                 var_threshold=50):
        self.frame_captor = FrameCaptor(camera_init_url)
        self.frame_captor.set_capture_mode()
        self.frame_displayer = FrameDisplayer(hand_index)
        self.image_preprocessor = ImagePreprocessor(hand_index, var_threshold)
        self.cnn_architecture = CNNArchitecture()
        self.cnn_architecture.build_model()
        self.text_to_speech_converter = TextToSpeechConverter()

        if HAND[hand_index] == 'RIGHT':
            self.cnn_architecture.load_model(WEIGHTS_RIGHT_PATH)
        else:
            self.cnn_architecture.load_model(WEIGHTS_LEFT_PATH)

        app = QtWidgets.QApplication(sys.argv)
        self.main_view = HandGestureRecognitionView()
        self.main_view.prediction_button.clicked.connect(self.run_hand_prediction)
        self.main_view.main_window.show()

        sys.exit(app.exec_())

    def run_hand_prediction(self, is_binary=False, with_cropping=False):
        new_predicted_letter = None
        last_predicted_letter = None
        iterations_between_different_predictions = 0
        predicted_text = ''
        is_background_captured = False

        while True:
            image = self.frame_captor.read_frame()
            flipped_image = cv.flip(image, 1)


            if is_background_captured is True:
                preprocessed_image, status = self.image_preprocessor.prepare_image_for_classification(flipped_image,
                                                                                              is_binary=is_binary,
                                                                                              with_cropping=with_cropping)
                if status == -1:
                    new_predicted_letter = -1
                else:
                    resized_image = cv.resize(preprocessed_image, (IMAGE_SIZE_X, IMAGE_SIZE_Y))
                    cnn_input = np.array(np.zeros(shape=(1, IMAGE_SIZE_X, IMAGE_SIZE_Y, 3)))
                    normalized_input = cv.normalize(resized_image, None, alpha=0, beta=1, norm_type=cv.NORM_MINMAX,
                                                    dtype=cv.CV_32F)
                    cnn_input[0] = normalized_input

                    predicted_class = self.cnn_architecture.predict_classes_for_images(cnn_input)
                    new_predicted_letter = CLASSES[predicted_class[0]]

                    if new_predicted_letter != last_predicted_letter:
                        last_predicted_letter = new_predicted_letter
                    else:
                        iterations_between_different_predictions = iterations_between_different_predictions + 1

                    if iterations_between_different_predictions > 40:
                        iterations_between_different_predictions = 0
                        predicted_text = predicted_text + last_predicted_letter

            voice_thread = threading.Thread(target=self.text_to_speech_converter.convert_text_to_speech,
                                            kwargs={'text': new_predicted_letter})
            voice_thread.start()
            image = self.frame_displayer.display_frame(flipped_image, new_predicted_letter, predicted_text)
            self.main_view.update_frame(image)

            k = cv.waitKey(10)

            # TODO: Simplify this somehow, there are too many ifs + we need to add for saving and loading
            # Press Esc to Exit Program
            if k == ord('q'):
                cv.destroyAllWindows()
                exit(0)
            # Press B to Capture Background
            elif k == ord('b'):
                self.image_preprocessor.set_background_subtractor()
                is_background_captured = True
            elif k == ord('d'):
                predicted_text = predicted_text[:-1]
            elif k == ord('s'):
                predicted_text = predicted_text + ' '
            elif k == ord('n'):
                predicted_text = predicted_text + '\n'
            elif k in [ord('.'), ord(','), ord('?'), ord('!'), ord("'"), ord('"')]:
                predicted_text = predicted_text + ('%c' % k)
            elif k == ord('c'):
                predicted_text = ''

            # Press R to eliminate Current Background, then press B to capture it again
            elif k == ord('r'):
                new_predicted_letter = None
                is_background_captured = False
