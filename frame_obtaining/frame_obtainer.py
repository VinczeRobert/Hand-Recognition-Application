import requests
import cv2 as cv
import numpy as np
from preprocessing.constants import THRESHOLD
from preprocessing.image_preprocessing import smoothing

trackbar_name = 'Hand Recognition Application'
URL = "http://192.168.1.103:8080/shot.jpg"

class FrameObtainer:
    def __init__(self, cap_region_x_begin, cap_region_y_end):
        self._cap_region_x_begin = cap_region_x_begin
        self._cap_region_y_end = cap_region_y_end

    @staticmethod
    def print_threshold(thr):
        print("Changed threshold to " + str(thr))

    def create_trackbar(self):
        cv.namedWindow(trackbar_name)
        cv.createTrackbar('thr', trackbar_name, THRESHOLD, 100, self.print_threshold)

    def read_frame(self, is_background_captured, predicted_label):
        image_response = requests.get(URL)
        image_array = np.array(bytearray(image_response.content), dtype=np.uint8)
        frame = cv.imdecode(image_array, -1)
        frame = cv.resize(frame, (1536, 864))
        filtered_frame = smoothing(frame)
        cv.rectangle(filtered_frame, (960, 0), (1920, 540), (0, 255, 0), 2)
        if is_background_captured is False:
            text_first = "Please make sure that your hand and any other moving"
            text_second = "objects are outside the green rectangle."
            text_third = "Press B after you made sure."
            cv.putText(filtered_frame, text_first, (60, 60), cv.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2, cv.LINE_AA)
            cv.putText(filtered_frame, text_second, (60, 85), cv.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2, cv.LINE_AA)
            cv.putText(filtered_frame, text_third, (60, 110), cv.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2, cv.LINE_AA)
        else:
            cv.putText(filtered_frame, "Predicted label: " + str(predicted_label), (750, 650), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)

        cv.imshow('Original Image', filtered_frame)
        return filtered_frame

