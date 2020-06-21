import requests
import cv2 as cv
import numpy as np
from requests.exceptions import ConnectionError, Timeout

class FrameCaptor:
    _instance = None

    def __init__(self, init_url=''):
        """
        This class is used to continuosly capture frames from the camera in real time and to prepare and to edit them
        with display messages and the rectangle representing the area of interest, where users are required to put their hand signs
        :param url: url to Android IPWebcam server; if it is a valid one, the application will use the Android phone's camera
        :param hand: 0 for right hand, 1 for left hand
        """
        # self._init_url = 'http://192.168.1.104:8080/shot.jpg'
        self._init_url = '/shot.jpg'
        self._is_android_server = False
        self._camera = None
        self._is_running = False

    @staticmethod
    def get_instance(android_server_url=''):
        if FrameCaptor._instance is None:
            FrameCaptor._instance = FrameCaptor(android_server_url)
        return FrameCaptor._instance

    def set_capture_mode(self):
        # if the url is not empty and is valid then the Android camera will be used
        if self._init_url != '/shot.jpg':
            try:
                requests.get(self._init_url, timeout=5)
                self._is_android_server = True
                return
            except (ConnectionError, Timeout) as e:
                print(e)
                print('Invalid URL or the server is taking too much time. The built-in camera will be used instead')

        # if the url is not valid, the PC camera will be used by default
        self._camera = cv.VideoCapture(0)
        self._camera.set(10, 200)
        self._camera.set(3, 1280)
        self._camera.set(cv.CAP_PROP_SETTINGS, 1)

    def read_frame(self):
        """
        Reads frame from camera input, applies bilateral filter on it and display responses to the user
        :param is_background_captured: boolean parameter to check if the background has been extracted
        :param predicted_letter: the response of the CNNArchitecture for the currently shown hand sign
        :return: frame with messages
        """
        if self._is_android_server is False:
            _, frame = self._camera.read()
        else:
            image_response = requests.get(self._init_url)
            image_array = np.array(bytearray(image_response.content), dtype=np.uint8)
            frame = cv.imdecode(image_array, -1)
            frame = cv.resize(frame, (1280, 720))

        frame = cv.flip(frame, 1)
        return frame

    def is_camera_opened(self):
        if self._camera is not None:
            return self._camera.isOpened()
        return False

    def pause_and_restart_camera(self, is_running):
        self._is_running = is_running

    def is_running(self):
        return self._is_running

    def close_camera(self):
        self._camera.release()
