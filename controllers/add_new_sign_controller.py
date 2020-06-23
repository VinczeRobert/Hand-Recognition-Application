import os
import cv2 as cv
from model.frame_captor import FrameCaptor
from model.frame_displayer import FrameDisplayer
from model.image_preprocessor import ImagePreprocessor
from model.settings import Settings
from view.main_view import MainView


class AddNewSignController:
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
        self._start_saving = False

        self.add_new_sign_view = main_view.add_new_sign_view
        self.add_new_sign_view.load_text_button.clicked.connect(lambda: self._set_download_folder())
        self.add_new_sign_view.start_saving_button.clicked.connect(lambda: self._set_start())
        self.add_new_sign_view.save_background_button.clicked.connect(
            lambda: self.image_preprocessor.set_background_subtractor())
        self.add_new_sign_view.keyPressed.connect(self.button_events)

    def _set_download_folder(self):
        self.upload_path = self.add_new_sign_view.choose_folder()

    def _set_start(self):
        if self.image_preprocessor.get_background_subtractor() is not None:
            self._start_saving = True

    def start_video(self, widget_class):
        self.add_new_sign_view.graphics_view.setFocus()

        if isinstance(self.add_new_sign_view, widget_class):
            self.frame_captor.pause_and_restart_camera(True)
            self.frame_displayer.set_hand_index(self.settings.get_hand())
            self.image_preprocessor.set_hand_index(self.settings.get_hand())

            if self._upload_path is None:
                self._upload_path = self.add_new_sign_view.choose_folder()

            self.preview_for_param_preparing(self.settings.get_image_type(), self.settings.get_intermediary_steps())
        else:
            cv.destroyAllWindows()
            self.image_preprocessor.reset_background_subtractor()
            self.frame_captor.pause_and_restart_camera(False)

    def preview_for_param_preparing(self, image_type, intermediary_steps):
        while self.frame_captor.is_running():
            image = self.frame_captor.read_frame()

            if self.image_preprocessor.get_background_subtractor():
                _, _ = self.image_preprocessor.prepare_image_for_classification(image, image_type, intermediary_steps)

            if self._start_saving:
                cv.destroyAllWindows()
                break
            else:
                image = self.frame_displayer.display_frame(image, 0)
                self.add_new_sign_view.update_frame(image)

            cv.waitKey(10)

        class_name, start_count, end_count = self.add_new_sign_view.set_parameters_before_start()
        self.create_data_for_class(self._upload_path, class_name, start_count, end_count, image_type, intermediary_steps)

    def create_data_for_class(self, path_to_folder, class_name, start_count, end_count, image_type, intermediary_steps):

        image_path = os.path.join(path_to_folder, class_name)

        if not os.path.exists(image_path):
            os.mkdir(image_path)

        while self.frame_captor.is_running():
            image = self.frame_captor.read_frame()

            preprocessed_image, status = self.image_preprocessor.prepare_image_for_classification(
                image, image_type, intermediary_steps)

            save_path = os.path.join(image_path, class_name + '_{}.jpg'.format(start_count))

            image = self.frame_displayer.display_frame(image, start_count)
            self.add_new_sign_view.update_frame(image)

            if status != -1:
                cv.imwrite(save_path, preprocessed_image)
                start_count = start_count + 1

            if start_count > end_count:
                break

            cv.waitKey(10)

    # TODO: Add key listener to interrupt image saving
    def button_events(self, key):
        if key == 66:
            self.image_preprocessor.set_background_subtractor()
        elif key == 81:
            print('We should quit...')
