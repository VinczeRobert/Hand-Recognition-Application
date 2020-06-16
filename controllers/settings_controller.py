from model.settings import Settings
from view.main_view import MainView


class SettingsController:
    def __init__(self):
        self.settings = Settings.get_instance()
        main_view = MainView.get_instance()
        self.settings_view = main_view.settings_view
        self.settings_view.vocal_mode_checkbox.stateChanged.connect(lambda: self.settings.switch_vocal_mode())
        self.settings_view.rgb_images_radio_button.toggled.connect(lambda: self.settings.switch_image_type())
        self.settings_view.left_hand_radio_button.toggled.connect(lambda: self.settings.switch_hand())
        self.settings_view.android_server_url_line_edit.textChanged.connect(lambda: self.settings.set_android_server_url(
            self.settings_view.android_server_url_line_edit.text()
        ))
        self.settings_view.h5_path_line_edit.textChanged.connect(lambda: self.settings.set_h5_path(
            self.settings_view.h5_path_line_edit.text()
        ))

        for checkbox in self.settings_view.vertical_group_box.children()[1:]:
            checkbox.stateChanged.connect(lambda state, checkbox=checkbox: self.settings.set_intermediary_step(checkbox))


