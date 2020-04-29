import requests
import cv2 as cv
import numpy as np
from base_constants.general_constants import CAPTURING_MODE, HAND
from preprocessing.image_preprocessing import smoothing


class FrameCaptor:

    def __init__(self, url='', hand_index=0):
        """
        This class is used to continuosly capture frames from the camera in real time and to prepare and to edit them
        with display messages and the rectangle representing the area of interest, where users are required to put their hand signs
        :param url: url to Android IPWebcam server; if it is a valid one, the application will use the Android phone's camera
        :param hand: 0 for right hand, 1 for left hand
        """
        self._url = url + '/shot.jpg'
        self._capturing_mode = None
        self.hand_index = hand_index

    def set_capture_mode(self):
        # if the url is not empty and is valid then the Android camera will be used
        if self._url != '':
            response = requests.get(self._url)
            # TODO: We need a way to validate the URL before checking if we have a response
            if response.ok:
                self._capturing_mode = 1
                return

        # if the url is not valid, the PC camera will be used by default
        self._capturing_mode = 0
        self._camera = cv.VideoCapture(0)
        self._camera.set(10, 200)
        self._camera.set(3, 1280)

    def read_frame(self, is_background_captured, predicted_letter):
        """
        Reads frame from camera input, applies bilateral filter on it and display responses to the user
        :param is_background_captured: boolean parameter to check if the background has been extracted
        :param predicted_letter: the response of the CNNArchitecture for the currently shown hand sign
        :return: frame with messages
        """
        if CAPTURING_MODE[self._capturing_mode] == 'PC_CAMERA':
            _, frame = self._camera.read()
        else:
            image_response = requests.get(self._url)
            image_array = np.array(bytearray(image_response.content), dtype=np.uint8)
            frame = cv.imdecode(image_array, -1)
            frame = cv.resize(frame, (1280, 720))

        filtered_frame = smoothing(frame)

        # If the user wants to use his/her left hand, the rectangle representing the area of interest will
        # be shown on the upper-left corner
        if HAND[self.hand_index] == 'RIGHT':
            cv.rectangle(filtered_frame, (800, 0), (1280, 480), (0, 255, 0), 2)
        else:
            # otherwise on the upper-right corner
            cv.rectangle(filtered_frame, (0, 0), (480, 480), (0, 255, 0), 2)

        if is_background_captured is False:
            text_first = "Please make sure that your hand and any other moving"
            text_second = "objects are outside the green rectangle."
            text_third = "Press B after you made sure."
            cv.putText(filtered_frame, text_first, (60, 60), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0,255), 2, cv.LINE_AA)
            cv.putText(filtered_frame, text_second, (60, 85), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv.LINE_AA)
            cv.putText(filtered_frame, text_third, (60, 110), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv.LINE_AA)
        else:
            cv.putText(filtered_frame, "Predicted letter: " + str(predicted_letter), (750, 650), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)

        cv.imshow('Hand Recognition Application (HRA)', filtered_frame)
        return filtered_frame