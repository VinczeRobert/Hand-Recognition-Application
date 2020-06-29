import os
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGroupBox, QHBoxLayout, QScrollArea, QVBoxLayout, QSlider, \
    QStyle, QComboBox
from view.style_sheets.main_view_stylesheet import FIRST_LETTER_LABEL_STYLE_SHEET, REST_LETTERS_LABEL_STYLE_SHEET, \
    BUTTON_STYLE_SHEET, BACKGROUND_COLOR


# noinspection PyArgumentList
class HomeView(QWidget):
    """
    View class containg the title of the application and options for viewing the gestures of each letter of the
    american sign language and for viewing some demonstrating videos of the application.
    This View is what the user first sees when the application is launched.
    """

    def __init__(self, icon, parent=None):
        super(HomeView, self).__init__(parent)

        self.icon = icon

        self.h_picture = QLabel(self)
        self.r_picture = QLabel(self)
        self.a_picture = QLabel(self)

        self.h_first = QLabel("H", self)
        self.h_rest = QLabel("and", self)
        self.r_first = QLabel("R", self)
        self.r_rest = QLabel("ecognition", self)
        self.a_first = QLabel("A", self)
        self.a_rest = QLabel("pplication", self)

        self.horizontal_group_box = QGroupBox(self)
        self.horizontal_layout = QHBoxLayout(self.horizontal_group_box)

        self.show_gestures_button = QPushButton("See Hand Gestures")
        self.help_icon = QIcon()
        self.show_videos_button = QPushButton("See Videos")
        self.videos_icon = QIcon()

        self.tutorial_view = None
        self.video_view = None
        self.show_gestures_button.clicked.connect(lambda: self.set_tutorial_view())
        self.show_videos_button.clicked.connect(lambda: self.set_videos_view())

        self.setup_view()

    def set_tutorial_view(self):
        self.tutorial_view = GestureView(self.icon, os.listdir('data/gestures'))

    def set_videos_view(self):
        self.video = VideoView(self.icon, 'data/videos/romanian_app_text.avi')

    def setup_view(self):
        self.horizontal_group_box.setGeometry(QtCore.QRect(200, 600, 600, 150))
        self.horizontal_group_box.setSizeIncrement(QtCore.QSize(40, 1))
        self.horizontal_group_box.setFlat(False)
        self.horizontal_group_box.setStyleSheet("border: none;")
        self.horizontal_layout.setSpacing(40)

        self.h_first.setGeometry(QtCore.QRect(310, 520, 51, 61))
        self.h_first.setStyleSheet(FIRST_LETTER_LABEL_STYLE_SHEET)
        self.h_rest.setGeometry(QtCore.QRect(360, 520, 121, 61))
        self.h_rest.setStyleSheet(REST_LETTERS_LABEL_STYLE_SHEET)

        self.r_first.setGeometry(QtCore.QRect(700, 520, 51, 61))
        self.r_first.setStyleSheet(FIRST_LETTER_LABEL_STYLE_SHEET)
        self.r_rest.setGeometry(QtCore.QRect(740, 510, 351, 81))
        self.r_rest.setStyleSheet(REST_LETTERS_LABEL_STYLE_SHEET)

        self.a_first.setGeometry(QtCore.QRect(1130, 520, 51, 61))
        self.a_first.setStyleSheet(FIRST_LETTER_LABEL_STYLE_SHEET)
        self.a_rest.setGeometry(QtCore.QRect(1170, 500, 351, 91))
        self.a_rest.setStyleSheet(REST_LETTERS_LABEL_STYLE_SHEET)

        self.h_picture.setGeometry(QtCore.QRect(161, 280, 432, 230))
        self.h_picture.setPixmap(QPixmap('data/icons/h_letter.png'))

        self.r_picture.setGeometry(QtCore.QRect(754, 10, 242, 500))
        self.r_picture.setPixmap(QPixmap('data/icons/r_letter.png'))

        self.a_picture.setGeometry(QtCore.QRect(1160, 130, 282, 370))
        self.a_picture.setPixmap(QPixmap('data/icons/a_letter.png'))

        self.help_icon.addPixmap(QPixmap("data/icons/help_icon"), QIcon.Normal, QIcon.Off)
        self.show_gestures_button.setIcon(self.help_icon)
        self.show_gestures_button.setIconSize(QtCore.QSize(50, 50))
        self.show_gestures_button.setStyleSheet(BUTTON_STYLE_SHEET)
        self.horizontal_layout.addWidget(self.show_gestures_button)

        self.videos_icon.addPixmap(QPixmap("data/icons/video_icon"), QIcon.Normal, QIcon.Off)
        self.show_videos_button.setIcon(self.videos_icon)
        self.show_videos_button.setIconSize(QtCore.QSize(50, 50))
        self.show_videos_button.setStyleSheet(BUTTON_STYLE_SHEET)
        self.horizontal_layout.addWidget(self.show_videos_button)


class GestureView(QScrollArea):
    """
    Scrollable View class which showes all gestures of the american sign language in a vertical layout form
    """

    def __init__(self, icon, gesture_path_list, parent=None):
        QScrollArea.__init__(self, parent)
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        layout.setSpacing(75)

        for index in range(len(gesture_path_list)):
            label = QLabel()
            pixmap = QPixmap('data/gestures/' + gesture_path_list[index])
            label.setPixmap(pixmap)
            layout.addWidget(label)

        self.setWidget(widget)
        self.setStyleSheet(BACKGROUND_COLOR)
        self.setWidgetResizable(True)
        self.setWindowTitle('Gestures')
        self.setWindowIcon(QIcon(icon))
        self.resize(800, 600)
        self.show()


# noinspection PyArgumentList
class VideoView(QWidget):
    """
    View class which lets users watch a few videos demonstrating the hand gesture recognition use case.
    """
    def __init__(self, icon, path_to_video, parent=None):
        QWidget.__init__(self, parent)

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()

        self.play_button = QPushButton()
        self.position_slider = QSlider(QtCore.Qt.Horizontal)
        self.combo_box = QComboBox()

        self.content_widget = QWidget(self)
        self.content_layout = QHBoxLayout()
        self.vertical_layout = QVBoxLayout()

        self.play_button.clicked.connect(self.play_video)
        self.position_slider.sliderMoved.connect(self.set_position)

        self.media_player.stateChanged.connect(self.media_state_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)

        self.setup_view(icon, path_to_video)

    def setup_view(self, icon, path_to_video):
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.position_slider.setRange(0, 0)
        self.combo_box.addItems(['ABC', 'Romanian Tutorial', 'Text 1', 'Text 2', 'Text 3'])

        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.addWidget(self.play_button)
        self.content_layout.addWidget(self.position_slider)
        self.content_layout.addWidget(self.combo_box)

        self.vertical_layout.addWidget(self.video_widget)
        self.vertical_layout.addLayout(self.content_layout)
        self.setLayout(self.vertical_layout)

        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(path_to_video)))
        self.media_player.play()
        self.media_player.pause()

        self.resize(800, 600)
        self.setWindowTitle('Videos')
        self.setWindowIcon(QIcon(icon))
        self.show()

    def play_video(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def set_position(self, position):
        self.media_player.setPosition(position)

    def media_state_changed(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )
        else:
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
            )

    def duration_changed(self, duration):
        self.position_slider.setRange(0, duration)

    def position_changed(self, position):
        self.position_slider.setValue(position)
