import cv2 as cv
import numpy as np

from base_constants.general_constants import HAND


class HandDetector:
    def __init__(self, accum_weight=0.5):
        self.accum_weight = accum_weight
        self.background = None

    @staticmethod
    def smooth_image(image):
        filtered_image = cv.bilateralFilter(image, 5, 50, 100)
        filtered_image = cv.flip(filtered_image, 1)
        return filtered_image

    def update_background(self, image):
        if self.background is None:
            self.background = image.copy().astype("float")
            return

        cv.accumulateWeighted(image, self.background, self.accum_weight)

    def extract_background_difference(self, image, hand_index):
        difference = cv.absdiff(self.background.astype("uint8"), image)
        kernel = np.ones((3, 3), np.uint8)
        opening = cv.erode(difference, kernel, iterations=5)
        opening = cv.dilate(difference, kernel, iterations=5)

        if HAND[hand_index] == 'RIGHT':
            extracted_image = opening[0:480, 800:1280]
        else:
            extracted_image = opening[0:480, 0:480]

        return extracted_image

    @staticmethod
    def cropping(self):
        largest_area = finding


