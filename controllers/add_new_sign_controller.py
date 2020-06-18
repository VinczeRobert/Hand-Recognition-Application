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
        self.upload_path = None
        self.start_saving = False
        self.frame_captor = FrameCaptor(self.settings.android_server_url)
        self.frame_captor.set_capture_mode()
        self.image_preprocessor = ImagePreprocessor()
        self.frame_displayer = FrameDisplayer(self.settings.hand)

        self.main_view = MainView.get_instance()
        self.add_new_sign_view = self.main_view.add_new_sign_view
        self.main_view.central_widget.currentChanged.connect(lambda: self.start_video(
            self.main_view.central_widget.currentWidget().__class__.__name__
        ))

        self.add_new_sign_view.load_text_button.clicked.connect(lambda: self.set_download_folder())
        self.add_new_sign_view.start_saving_button.clicked.connect(lambda: self.set_start())
        self.add_new_sign_view.keyPressed.connect(self.button_events)

    def set_download_folder(self):
        self.upload_path = self.add_new_sign_view.choose_folder()

    def set_start(self):
        if self.image_preprocessor.background_subtractor is not None:
            self.start_saving = True

    def start_video(self, widget_class):
        if widget_class == 'AddNewSignView':
            self.frame_displayer.hand_index = self.settings.hand
            self.image_preprocessor.hand_index = self.settings.hand

            if self.upload_path is None:
                self.upload_path = self.add_new_sign_view.choose_folder()

            self.preview_for_param_preparing()

    def preview_for_param_preparing(self):
        while True:
            image = self.frame_captor.read_frame()

            if self.image_preprocessor.background_subtractor is not None:
                preprocessed_image, status = self.image_preprocessor.prepare_image_for_classification(
                    image, is_binary=self.settings.image_type)

            if self.start_saving:
                start_count = 1
                end_count = 2000

                if self.add_new_sign_view.start_index_line_edit.text().isdigit():
                    start_count = int(self.add_new_sign_view.start_index_line_edit.text())
                if self.add_new_sign_view.end_index_line_edit.text().isdigit():
                    end_count = int(self.add_new_sign_view.end_index_line_edit.text())

                self.create_data_for_class(self.upload_path, self.add_new_sign_view.class_name_line_edit.text(),
                                           start_count, end_count)
                break
            else:
                image = self.frame_displayer.display_frame(image, 0)
                self.add_new_sign_view.update_frame(image)

            cv.waitKey(10)

    def create_data_for_class(self, path_to_folder, class_name, start_count, end_count):

        image_path = os.path.join(path_to_folder, class_name)

        if not os.path.exists(image_path):
            os.mkdir(image_path)

        for count in range(start_count, end_count+1):
            image = self.frame_captor.read_frame()

            preprocessed_image, status = self.image_preprocessor.prepare_image_for_classification(
                image, is_binary=self.settings.image_type)

            save_path = os.path.join(image_path, class_name + '_{}.jpg'.format(count))

            if status != -1:
                cv.imwrite(save_path, preprocessed_image)

            image = self.frame_displayer.display_frame(image, count)
            self.add_new_sign_view.update_frame(image)

            if self.main_view.central_widget.currentWidget().__class__.__name__ != 'AddNewSignView':
                cv.destroyAllWindows()
                break

            cv.waitKey(10)

    #TODO: Add key listener to interrupt image saving
    def button_events(self, key):
        if key == 66:
            self.image_preprocessor.set_background_subtractor()
        elif key == 81:
            print('We should quit...')
