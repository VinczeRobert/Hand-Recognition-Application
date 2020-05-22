import cv2 as cv
import numpy as np
from base_constants.general_constants import IMAGE_SIZE_Y, IMAGE_SIZE_X, CLASSES, HAND, WEIGHTS_RIGHT_PATH, \
    WEIGHTS_LEFT_PATH
from model.cnn_architecture import CNNArchitecture
from model.frame_captor import FrameCaptor
from model.frame_displayer import FrameDisplayer
from model.image_preprocessor import ImagePreprocessor


class Controller:
    def __init__(self, camera_init_url='', hand_index=0,
                 var_threshold=50):
        self.frame_captor = FrameCaptor(camera_init_url)
        self.frame_captor.set_capture_mode()
        self.frame_displayer = FrameDisplayer(hand_index)
        self.image_preprocessor = ImagePreprocessor(hand_index, var_threshold)
        self.cnn_architecture = CNNArchitecture()
        self.cnn_architecture.build_model()

        if HAND[hand_index] == 'RIGHT':
            self.cnn_architecture.load_model(WEIGHTS_RIGHT_PATH)
        else:
            self.cnn_architecture.load_model(WEIGHTS_LEFT_PATH)

    def run_hand_prediction(self, is_binary=False, with_cropping=False):
        predicted_letter = None
        is_background_captured = False

        while True:
            image = self.frame_captor.read_frame()
            flipped_image = cv.flip(image, 1)

            if is_background_captured is True:
                preprocessed_image = self.image_preprocessor.prepare_image_for_classification(flipped_image,
                                                                                              is_binary=is_binary,
                                                                                              with_cropping=with_cropping)

                resized_image = cv.resize(preprocessed_image, (IMAGE_SIZE_X, IMAGE_SIZE_Y))
                cnn_input = np.array(np.zeros(shape=(1, IMAGE_SIZE_X, IMAGE_SIZE_Y, 3)))
                normalized_input = cv.normalize(resized_image, None, alpha=0, beta=1, norm_type=cv.NORM_MINMAX,
                                                dtype=cv.CV_32F)
                cnn_input[0] = normalized_input

                predicted_class = self.cnn_architecture.predict_classes_for_images(cnn_input)
                predicted_letter = CLASSES[predicted_class[0]]

            self.frame_displayer.display_frame(flipped_image, predicted_letter)

            k = cv.waitKey(10)

            # Press Esc to Exit Program
            if k == 27:
                cv.destroyAllWindows()
                exit(0)
            # Press B to Capture Background
            elif k == ord('b'):
                self.image_preprocessor.set_background_subtractor()
                is_background_captured = True

            # Press R to eliminate Current Background, then press B to capture it again
            elif k == ord('r'):
                predicted_letter = None
                is_background_captured = False