import cv2 as cv
import numpy as np

from preprocessing.constants import ETA, ERODE_ITERATIONS, BACKGROUND_SUB_THRESHOLD


class BackgroundSubtractor:

    def __init__(self):
        self._frame = None
        self._background_model = cv.createBackgroundSubtractorMOG2(0, BACKGROUND_SUB_THRESHOLD)
        self._background_captured = False

    def extract_background(self, show_image=False):
        mask = self._background_model.apply(self._frame, learningRate=ETA)
        kernel = np.ones((3,3), np.uint8)
        mask = cv.erode(mask, kernel, iterations=ERODE_ITERATIONS)
        mask = cv.dilate(mask, kernel, iterations=ERODE_ITERATIONS)

        # get the background by checking the difference
        img = cv.bitwise_and(self._frame, self._frame, mask=mask)
        img = img[0:540, 960:1920]

        if show_image:
            cv.imshow('Extracted Hand', img)
        return img

    def set_frame(self, frame):
        self._frame = frame

    def is_background_captured(self):
        return self._background_captured

    def set_background_captured(self, background_captured):
        self._background_captured = background_captured
