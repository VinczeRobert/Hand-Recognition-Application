import sys
import threading
import cv2 as cv
import numpy as np
from base_constants.constants import IMAGE_SIZE_Y, IMAGE_SIZE_X, CLASSES
from model.frame_captor import FrameCaptor
from model.frame_displayer import FrameDisplayer
from model.image_preprocessor import ImagePreprocessor
from model.predictor import Predictor
from model.settings import Settings
from view.main_view import MainView


class HandGestureRecognitionController:
    def __init__(self):
        self.settings = Settings.get_instance()
        self.frame_captor = FrameCaptor(self.settings.android_server_url)
        self.frame_captor.set_capture_mode()

        self.frame_displayer = FrameDisplayer(self.settings.hand)
        self.image_preprocessor = ImagePreprocessor(self.settings.hand)

        self.predictor = Predictor('data/weights/left_hand_rgb_29.ckpt')

        self.main_view = MainView.get_instance()
        self.hand_gesture_recognition_view = self.main_view.hand_gesture_recognition_view
        self.hand_gesture_recognition_view.keyPressed.connect(self.button_events)

        self.main_view.central_widget.currentChanged.connect(lambda: self.start_video(
            self.main_view.central_widget.currentWidget().__class__.__name__
        ))

    def start_video(self, widget_class):
        if widget_class == 'HandGestureRecognitionView':
            self.frame_displayer.hand_index = self.settings.hand
            self.image_preprocessor.hand_index = self.settings.hand
            self.run_hand_prediction()

    def run_hand_prediction(self, is_binary=False):
        new_predicted_letter = None
        last_predicted_letter = None
        iterations_between_different_predictions = 0
        predicted_text = ''

        while True:
            image = self.frame_captor.read_frame()
            flipped_image = cv.flip(image, 1)

            if self.image_preprocessor.background_subtractor is not None:
                preprocessed_image, status = self.image_preprocessor.prepare_image_for_classification(flipped_image,
                                                                                              is_binary=is_binary)
                if status == -1:
                    new_predicted_letter = -1
                else:
                    new_predicted_letter = self.predictor.predict_hand_gesture(preprocessed_image)

                    if new_predicted_letter != last_predicted_letter:
                        last_predicted_letter = new_predicted_letter
                    else:
                        iterations_between_different_predictions = iterations_between_different_predictions + 1

                    if iterations_between_different_predictions > 40:
                        iterations_between_different_predictions = 0
                        predicted_text = predicted_text + last_predicted_letter

            image = self.frame_displayer.display_frame(flipped_image, new_predicted_letter, predicted_text)
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            self.hand_gesture_recognition_view.update_frame(image)

            if self.main_view.central_widget.currentWidget().__class__.__name__ != 'HandGestureRecognitionView':
                cv.destroyAllWindows()
                break

            cv.waitKey(10)

    def button_events(self, key):
        if key == 66:
            self.image_preprocessor.set_background_subtractor()