import cv2 as cv
from model.frame_captor import FrameCaptor
from model.frame_displayer import FrameDisplayer
from model.image_preprocessor import ImagePreprocessor
from model.predictor import Predictor
from model.settings import Settings
from view.main_view import MainView


class HandGestureRecognitionController:
    def __init__(self):
        self.settings = Settings.get_instance()
        self.frame_captor = FrameCaptor.get_instance(self.settings.android_server_url)
        self.frame_captor.set_capture_mode()
        self.frame_displayer = FrameDisplayer(self.settings.hand)
        self.image_preprocessor = ImagePreprocessor(self.settings.hand)

        self.predictor = Predictor('data/weights/weights_binary_left.ckpt', self.settings.classes)

        main_view = MainView.get_instance()
        self.hand_gesture_recognition_view = main_view.hand_gesture_recognition_view

        main_view.central_widget.currentChanged.connect(lambda: self.start_video(
            main_view.central_widget.currentWidget().__class__))

        self.hand_gesture_recognition_view.save_background_button.clicked.connect(
            lambda: self.image_preprocessor.set_background_subtractor()
        )
        self.hand_gesture_recognition_view.keyPressed.connect(self.button_events)

    def start_video(self, widget_class):
        self.hand_gesture_recognition_view.graphics_view.setFocus()
        self.frame_captor.pause_and_restart_camera(True)

        if isinstance(self.hand_gesture_recognition_view, widget_class):
            self.frame_displayer.hand_index = self.settings.hand
            self.image_preprocessor.hand_index = self.settings.hand

            self.run_hand_prediction(self.settings.image_type)
        else:
            cv.destroyAllWindows()
            self.frame_captor.pause_and_restart_camera(False)

    def run_hand_prediction(self, image_type):
        new_predicted_letter = None

        while self.frame_captor.is_running():
            image = self.frame_captor.read_frame()

            if self.image_preprocessor.background_subtractor is not None:
                preprocessed_image, status = self.image_preprocessor.prepare_image_for_classification(image, image_type)
                if status == -1:
                    new_predicted_letter = -1
                else:
                    new_predicted_letter = self.predictor.predict_hand_gesture(preprocessed_image, False)
                    self.frame_displayer.get_predicted_text(new_predicted_letter)

            image = self.frame_displayer.display_frame(image, new_predicted_letter)
            self.hand_gesture_recognition_view.update_frame(image)

            cv.waitKey(10)

    def button_events(self, key):
        if key == 66:
            self.image_preprocessor.set_background_subtractor()
