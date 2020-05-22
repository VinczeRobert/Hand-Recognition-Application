import cv2 as cv
import numpy as np
from base_constants.general_constants import HAND


class ImagePreprocessor:
    def __init__(self, hand_index=0, var_threshold=50):
        self.background_subtractor = None
        self.hand_index = hand_index
        self.var_threshold = var_threshold

    def prepare_image_for_classification(self, image, is_binary, with_cropping):
        # STEP 1: Remove noise
        filtered_image = cv.bilateralFilter(image, 9, 75, 75)

        # STEP 2: Get the difference between current frame and background
        binary_image = self.background_subtractor.apply(filtered_image, learningRate=0)

        # STEP 3: Perform opening on extracted hand
        kernel = np.ones((3, 3), np.uint8)
        eroded_hand = cv.erode(binary_image, kernel, iterations=2)
        opened_hand = cv.erode(eroded_hand, kernel, iterations=2)

        # STEP 4: Find the contours of the image
        contours = cv.findContours(opened_hand, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]

        # STEP 5: If the image has at least one contour, keep only the biggest one, otherwise exit
        if len(contours) == 0:
            return -1
        else:
            largest_contour = sorted(contours, key=cv.contourArea)[-1]

            final_image = np.zeros(shape=opened_hand.shape, dtype=np.uint8)
            contoured_image = cv.drawContours(final_image, [largest_contour], 0, (255, 255, 255), -2)

            if with_cropping:
                # STEP 6 (OPTIONAL): Crop the image around the hand
                x, y, w, h = cv.boundingRect(largest_contour)
                contoured_image = contoured_image[y:y + h, x:x + w]

            if is_binary is False:
                # STEP 7 (OPTIONAL): For RGB Images, keep only pixels from contoured image
                contoured_image = cv.bitwise_and(image, image, mask=contoured_image)
            else:
                contoured_image = self.extend_binary_to_three_channels(contoured_image)

            # STEP 7: Extract the hand from the difference
            if HAND[self.hand_index] == 'RIGHT':
                extracted_hand = contoured_image[0:480, 800:1280]
            else:
                extracted_hand = contoured_image[0:480, 0:480]

            cv.imshow('Extracted Hand', extracted_hand)
            return extracted_hand

    def set_background_subtractor(self):
        self.background_subtractor = cv.createBackgroundSubtractorMOG2(0, self.var_threshold, detectShadows=False)

    # TODO: Find out if we actually need this, would be better if we could just feed classic binary images to the model
    @staticmethod
    def extend_binary_to_three_channels(one_channel_binary):
        """
        Extends a classic one-channel binary image to have three channels in order to feed it to the convolutional neural
        network model
        :param one_channel_binary:
        :return: binary image with three channels
        """
        three_channel_binary = np.zeros(shape=(one_channel_binary.shape[0], one_channel_binary.shape[1], 3))
        three_channel_binary[:, :, 0] = one_channel_binary
        three_channel_binary[:, :, 1] = one_channel_binary
        three_channel_binary[:, :, 2] = one_channel_binary
        return three_channel_binary
