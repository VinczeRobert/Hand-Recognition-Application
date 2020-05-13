import cv2 as cv
import numpy as np
from base_constants.general_constants import HAND




class BackgroundSubtractor:

    HISTORY = 0
    VAR_THRESHOLD = 50

    def __init__(self):
        self._frame = None
        self._background_model = cv.createBackgroundSubtractorMOG2(self.HISTORY, varThreshold=self.VAR_THRESHOLD)
        self._background_captured = False

    def extract_background_difference(self, hand_index=0, show_image=False):
        mask = self._background_model.apply(self._frame, learningRate=0)
        kernel = np.ones((3, 3), np.uint8)
        mask = cv.erode(mask, kernel, iterations=5)
        mask = cv.dilate(mask, kernel, iterations=5)

        # get the background by checking the difference
        difference = cv.bitwise_and(self._frame, self._frame, mask=mask)
        if HAND[hand_index] == 'RIGHT':
            difference = difference[0:480, 800:1280]
        else:
            difference = difference[0:480, 0:480]

        if show_image:
            cv.imshow('Extracted Hand', difference)
        return difference

    def set_frame(self, frame):
        self._frame = frame

    def is_background_captured(self):
        return self._background_captured

    def set_background_captured(self, background_captured):
        self._background_captured = background_captured

    def reset_background(self):
        self._background_model = cv.createBackgroundSubtractorMOG2(self.HISTORY, varThreshold=self.VAR_THRESHOLD)
