import cv2 as cv
import numpy as np
from base_constants.general_constants import HAND


class ImagePreprocessor:
    def __init__(self, hand_index=0, var_threshold=50):
        self.background_subtractor = None
        self.hand_index = hand_index
        self.var_threshold = var_threshold

    def prepare_rgb_image_for_classification(self, image):
        # STEP 1: Remove noise
        filtered_image = cv.bilateralFilter(image, 9, 75, 75)

        # STEP 2: Get background mask
        mask = self.background_subtractor.apply(filtered_image, learningRate=0)

        # STEP 3: Perform opening on mask
        kernel = np.ones((3, 3), np.uint8)
        eroded_mask = cv.erode(mask, kernel, iterations=3)
        opened_mask = cv.dilate(eroded_mask, kernel, iterations=3)

        # STEP 4: Get difference between background and current image
        difference = cv.bitwise_and(filtered_image, filtered_image, mask=opened_mask)

        # STEP 5: Extract the hand from the difference
        if HAND[self.hand_index] == 'RIGHT':
            extracted_hand = difference[0:480, 800:1280]
        else:
            extracted_hand = difference[0:480, 0:480]

        cv.imshow('Extracted Hand', extracted_hand)
        return extracted_hand

    def prepare_binary_image_for_classification(self, image):
        # STEP 1: Convert to grayscale
        grayscale_image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

        # STEP 2: Remove noise
        filtered_image = cv.bilateralFilter(grayscale_image, 9, 75, 75)

        # STEP 3: Convert image to binary
        binary_image = cv.threshold(filtered_image, 60, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

        # STEP 4: Get background mask
        mask = self.background_subtractor.apply(filtered_image, learningRate=0)

        # STEP 5: Get difference  between background and current image
        difference = cv.bitwise_and(filtered_image, filtered_image, mask)

        # STEP 6: Extract the hand from the difference
        if HAND[self.hand_index] == 'RIGHT':
            extracted_Hand = difference[0:480, 800:1280]
        else:
            extracted_Hand = difference[0:480, 0:480]

        # STEP 7: Perform opening on extracted hand
        kernel = np.ones((3, 3), np.uint8)
        eroded_hand = cv.erode(extracted_Hand, kernel, iterations=3)
        opened_hand = cv.erode(eroded_hand, kernel, iterations=3)

        # STEP 8: Find the contours of the image
        contours = cv.findContours(opened_hand, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]

        # STEP 9: If the image has at least one contour, keep only the biggest one, otherwise exit
        if len(contours) == 0:
            return opened_hand
        else:
            largest_contour = sorted(contours, key=cv.contourArea)[-1]
            final_image = np.zeros(shape=opened_hand.shape, dtype=np.uint8)
            return cv.drawContours(final_image, largest_contour, 0, (255, 255, 255), 2)

    def set_background_subtractor(self):
        self.background_subtractor = cv.createBackgroundSubtractorMOG2(0, self.var_threshold)