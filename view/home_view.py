import os

from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QPen
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGroupBox, QHBoxLayout, QScrollArea, QVBoxLayout, QSlider, \
    QStyle, QMainWindow

from view.style_sheets.main_view_stylesheet import FIRST_LETTER_LABEL_STYLE_SHEET, REST_LETTERS_LABEL_STYLE_SHEET, \
    BUTTON_STYLE_SHEET


# noinspection PyArgumentList
class HomeView(QWidget):

    def __init__(self, parent=None):
        super(HomeView, self).__init__(parent)

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
        self.videos_view = None
        self.show_gestures_button.clicked.connect(lambda: self.set_tutorial_view())
        self.show_videos_button.clicked.connect(lambda: self.set_videos_view())

        self.setup_view()

    def set_tutorial_view(self):
        self.tutorial_view = TutorialView(os.listdir('data/gestures'))

    def set_videos_view(self):
        self.videos_view = VideoView(path_to_video='C:/Users/robi997/Desktop/Vortex_Tutorials/Vortex1_0304/Vortex1_03.avi')

    def setup_view(self):
        self.horizontal_group_box.setGeometry(QtCore.QRect(200, 600, 600, 150))
        # self.horizontal_group_box.setSizePolicy(self.size_policy)
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
        self.h_picture.setPixmap(QPixmap("D:/Hand Gesture Datasets/Training/Only_Letters/Only_Letters/H/H.png"))

        self.r_picture.setGeometry(QtCore.QRect(754, 10, 242, 500))
        self.r_picture.setPixmap(QPixmap(
            "D:/Hand Gesture Datasets/Training/Only_Letters/Only_Letters/R/hand1_r_bot_seg_2_cropped.png"))

        self.a_picture.setGeometry(QtCore.QRect(1160, 130, 282, 370))
        self.a_picture.setPixmap(QPixmap("D:/Hand Gesture Datasets/Training/Only_Letters/Only_Letters/A/A.png"))

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


class TutorialView(QScrollArea):

    def __init__(self, gesture_path_list, parent=None):
        QScrollArea.__init__(self, parent)
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        layout.setSpacing(75)
        for index in range(len(gesture_path_list)):
            label = QLabel()
            pixmap = QPixmap('data/gestures/' + gesture_path_list[index])
            painter = QPainter(self)
            painter.drawPixmap(self.rect(), pixmap)
            pen = QPen(QtCore.Qt.darkYellow, 3)
            painter.setPen(pen)
            painter.drawLine(10, 10, self.rect().width() - 10, 50)
            label.setPixmap(pixmap)
            layout.addWidget(label)

        new_label = QLabel("Gigike Gigike Gigike Gigike")
        new_label.setWordWrap(True)
        layout.addWidget(new_label)
        self.setWidget(widget)
        self.setWidgetResizable(True)
        # self.setStyleSheet('background: black;')
        self.resize(800, 600)
        self.show()

class VideoView(QMainWindow):
    def __init__(self, path_to_video, parent=None):
        QWidget.__init__(self, parent)

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()

        self.play_button = QPushButton()
        self.position_slider = QSlider(QtCore.Qt.Horizontal)

        self.content_widget = QWidget(self)
        self.content_layout = QHBoxLayout()
        self.vertical_layout = QVBoxLayout()

        self.play_button.clicked.connect(self.play_video)
        self.position_slider.sliderMoved.connect(self.set_position)

        self.media_player.stateChanged.connect(self.media_state_changed)
        self.media_player.positionChanged.connect(self.position_changed)

        self.setup_view(path_to_video)

    def setup_view(self, path_to_video):
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.position_slider.setRange(0, 0)

        self.setCentralWidget(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.addWidget(self.play_button)
        self.content_layout.addWidget(self.position_slider)

        self.vertical_layout.addWidget(self.video_widget)
        self.vertical_layout.addLayout(self.content_layout)
        self.content_widget.setLayout(self.vertical_layout)

        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(path_to_video)))

        self.resize(640, 480)
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

    def position_changed(self, position):
        self.position_slider.setValue(position)



