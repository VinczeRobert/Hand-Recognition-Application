import cv2 as cv
from model.frame_captor import FrameCaptor
from model.frame_displayer import FrameDisplayer
from model.image_preprocessor import ImagePreprocessor
from model.predictor import Predictor
from model.settings import Settings
from view.main_view import MainView


class HandGestureRecognitionController:
    """
    Controller class responsible for handling user input related hand gesture recognition
    """
    def __init__(self):
        self.settings = Settings.get_instance()
        self.frame_captor = FrameCaptor.get_instance(self.settings.get_android_server_url())
        self.frame_captor.set_capture_mode()
        self.frame_displayer = FrameDisplayer(self.settings.get_hand())
        self.image_preprocessor = ImagePreprocessor(self.settings.get_hand())
        self.currently_predicted_text = ''

        self.predictor = Predictor('data/weights/augmented_weights2.ckpt', self.settings.get_classes())

        main_view = MainView.get_instance()
        self.hand_gesture_recognition_view = main_view.hand_gesture_recognition_view

        main_view.central_widget.currentChanged.connect(lambda: self.start_video(
            main_view.central_widget.currentWidget().__class__))

        self.hand_gesture_recognition_view.save_background_button.clicked.connect(
            lambda: self.image_preprocessor.set_background_subtractor()
        )

        self.hand_gesture_recognition_view.load_text_button.clicked.connect(lambda: self.load_text())
        self.hand_gesture_recognition_view.save_text_button.clicked.connect(lambda: self.save_text())

        self.hand_gesture_recognition_view.keyPressed.connect(self.button_events)

    def load_text(self):
        """
        Saving currently predicted text.
        """
        text_file_path = self.hand_gesture_recognition_view.choose_text_file_to_load()
        self.currently_predicted_text = self.frame_displayer.load_text(text_file_path)

    def save_text(self):
        """
        Loading currently predicted text.
        """
        text_file_path = self.hand_gesture_recognition_view.choose_text_file_to_save()
        self.frame_displayer.save_text(text_file_path)

    def start_video(self, widget_class):
        """
        This method starts recording if the current widget is AddNewSignView, otherwise it stops
        recording and the whole saving process
        :param widget_class: Current UI View chosen from the main menu
        """
        self.hand_gesture_recognition_view.graphics_view.setFocus()
        self.frame_captor.pause_and_restart_camera(True)

        if isinstance(self.hand_gesture_recognition_view, widget_class):
            self.frame_displayer.set_hand_index(self.settings.get_hand())
            self.image_preprocessor.set_hand_index(self.settings.get_hand())

            self.run_hand_prediction(self.settings.get_image_type(), self.settings.get_intermediary_steps())

        else:
            cv.destroyAllWindows()
            self.image_preprocessor.reset_background_subtractor()
            self.frame_captor.pause_and_restart_camera(False)

    def run_hand_prediction(self, image_type, intermediary_steps):
        """
        "This method takes image_type and intermediary_steps from Settings
         and starts recording and gives predictions for gestures
        """
        new_predicted_letter = None

        while self.frame_captor.is_running():
            image = self.frame_captor.read_frame()

            if self.image_preprocessor.get_background_subtractor() is not None:
                # Gets preprocessed image
                preprocessed_image, status = self.image_preprocessor.prepare_image_for_classification(
                    image, image_type, intermediary_steps)
                if status == -1:
                    new_predicted_letter = -1
                else:
                    # Controller only asks for prediction if status is not -1 (See ImagePreprocessor)
                    new_predicted_letter = self.predictor.predict_hand_gesture(
                        preprocessed_image, self.hand_gesture_recognition_view.vocal_mode_checkbox.isChecked())
                    # Update currently predicted text
                    self.currently_predicted_text = \
                        self.frame_displayer.get_predicted_text(new_predicted_letter, self.currently_predicted_text)

            # Display result with prediction
            image = self.frame_displayer.display_frame(image, new_predicted_letter, self.currently_predicted_text)
            self.hand_gesture_recognition_view.update_frame(image)

            cv.waitKey(10)

    def button_events(self, key):
        if key == 66: # Button B
            self.image_preprocessor.set_background_subtractor()
