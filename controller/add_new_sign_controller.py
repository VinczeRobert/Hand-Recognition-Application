import os
import cv2 as cv
from controller.validation import validate_add_new_sign
from model.frame_captor import FrameCaptor
from model.frame_displayer import FrameDisplayer
from model.image_preprocessor import ImagePreprocessor
from model.settings import Settings
from view.main_view import MainView
from view.dialogs import show_error_message


class AddNewSignController:
    """
    Controller class responsible for handling user input related to adding a new gesture
    """
    def __init__(self):
        self.settings = Settings.get_instance()
        self.frame_captor = FrameCaptor.get_instance(self.settings.get_android_server_url())
        self.image_preprocessor = ImagePreprocessor()
        self.frame_displayer = FrameDisplayer(self.settings.get_hand())

        main_view = MainView.get_instance()
        main_view.central_widget.currentChanged.connect(lambda: self.start_video(
            main_view.central_widget.currentWidget().__class__
        ))

        self._upload_path = None
        self._saving = False

        self.add_new_sign_view = main_view.add_new_sign_view
        self.add_new_sign_view.load_text_button.clicked.connect(lambda: self._set_download_folder())
        self.add_new_sign_view.start_saving_button.clicked.connect(lambda: self._set_start())
        self.add_new_sign_view.save_background_button.clicked.connect(
            lambda: self.image_preprocessor.set_background_subtractor())
        self.add_new_sign_view.keyPressed.connect(self.button_events)

    def _set_download_folder(self):
        self._upload_path = self.add_new_sign_view.choose_new_gesture_folder()

    def _set_start(self):
        if self.image_preprocessor.get_background_subtractor() is not None:

            # Starting the saving of frames of a new gesture is only possible if the entered data is correct
            if (validate_add_new_sign(self._upload_path, self.add_new_sign_view.class_name_line_edit.text(),
                                      self.add_new_sign_view.start_index_line_edit.text(),
                                      self.add_new_sign_view.end_index_line_edit.text(),
                                      self.settings.get_image_type())):
                self._saving = True
        else:
            # Background has to be saved before starting
            show_error_message('Please save the background before starting!')

    def start_video(self, widget_class):
        """
        This method starts recording if the current widget is AddNewSignView, otherwise it stops
        recording and the whole saving process
        :param widget_class: Current UI View chosen from the main menu
        """
        self.add_new_sign_view.graphics_view.setFocus()

        if isinstance(self.add_new_sign_view, widget_class):
            self.frame_captor.pause_and_restart_camera(True)
            self.frame_displayer.set_hand_index(self.settings.get_hand())
            self.image_preprocessor.set_hand_index(self.settings.get_hand())

            if self._upload_path is None:
                self._set_download_folder()

            self.preview_for_param_preparing(self.settings.get_image_type(), self.settings.get_intermediary_steps())
        else:
            cv.destroyAllWindows()
            self.image_preprocessor.reset_background_subtractor()
            self.frame_captor.pause_and_restart_camera(False)
            self._saving = False

    def preview_for_param_preparing(self, image_type, intermediary_steps):
        """
        "This method takes image_type and intermediary_steps from Settings
         and starts recording but it doesn't save images yet.
        """
        while self.frame_captor.is_running():
            image = self.frame_captor.read_frame()

            if self.image_preprocessor.get_background_subtractor():
                # Image processing here is only done to save the background
                # and show intermediary steps, but the input is not used
                _, _ = self.image_preprocessor.prepare_image_for_classification(image, image_type, intermediary_steps)

            if self._saving:
                cv.destroyAllWindows()
                break
            else:
                image = self.frame_displayer.display_frame_in_building_mode(image, 0)
                self.add_new_sign_view.update_frame(image)

            cv.waitKey(10)

        if self.frame_captor.is_running():
            # This function is called after validation of fields was correct, background was set and
            # start button was pressed.
            self.create_data_for_class(self._upload_path, self.add_new_sign_view.class_name_line_edit.text(),
                                       int(self.add_new_sign_view.start_index_line_edit.text()),
                                       int(self.add_new_sign_view.end_index_line_edit.text()), image_type,
                                       intermediary_steps)

    def create_data_for_class(self, path_to_folder, class_name, start_count, end_count, image_type, intermediary_steps):

        image_path = os.path.join(path_to_folder, class_name)

        if not os.path.exists(image_path):
            os.mkdir(image_path)

        while self.frame_captor.is_running():
            # Get new frame
            image = self.frame_captor.read_frame()

            # Send the current frame through the image processing algorithms
            preprocessed_image, status = self.image_preprocessor.prepare_image_for_classification(
                image, image_type, intermediary_steps)

            save_path = os.path.join(image_path, class_name + '_{}.jpg'.format(start_count))

            # Update current frame in the UI
            image = self.frame_displayer.display_frame_in_building_mode(image, start_count)
            self.add_new_sign_view.update_frame(image)

            if status != -1:
                # Images are only saved if status is not -1 (see ImagePreprocessor)
                cv.imwrite(save_path, preprocessed_image)
                start_count = start_count + 1

            if start_count > end_count:
                break

            cv.waitKey(10)

    # TODO: Add key listener to interrupt image saving
    def button_events(self, key):
        if key == 66:   # Button B
            self.image_preprocessor.set_background_subtractor()
        elif key == 81: # Button Q
            # Q doesn't quit the saving of images, but it pauses it
            if self._saving:
                self._saving = False
