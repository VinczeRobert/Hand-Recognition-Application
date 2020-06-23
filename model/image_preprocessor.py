import cv2 as cv
import numpy as np
from model.settings import HAND, IMAGE_TYPE


class ImagePreprocessor:
    def __init__(self, hand_index=0):
        self._background_subtractor = None
        self._hand_index = hand_index

    def prepare_image_for_classification(self, image, image_type, intermediary_steps):
        # STEP 1: Remove noise
        filtered_image = cv.bilateralFilter(image, 9, 75, 75)
        self.show_intermediary_step(filtered_image, intermediary_steps, 'Filtered Image')

        # STEP 2: Get the difference between current frame and background
        background_mask = self._background_subtractor.apply(filtered_image, learningRate=0)
        self.show_intermediary_step(background_mask, intermediary_steps, 'Background Difference Image')

        # STEP 3: Extract only the hand part from the difference
        if self._hand_index == HAND[0]:
            binary_mask = background_mask[0:480, 800:1280]
            extracted_image = image[0:480, 800:1280]
        else:
            binary_mask = background_mask[0:480, 0:480]
            extracted_image = image[0:480, 0:480]

        self.show_intermediary_step(binary_mask, intermediary_steps, 'Extracted Binary Hand Image')

        # STEP 4: Perform opening on extracted hand to remove noise
        kernel = np.ones((3, 3), np.uint8)
        eroded_hand = cv.erode(binary_mask, kernel, iterations=2)
        opened_hand = cv.erode(eroded_hand, kernel, iterations=2)
        self.show_intermediary_step(opened_hand, intermediary_steps, 'Opened Hand Image')

        # STEP 5: Find the contours of the image
        contours = cv.findContours(opened_hand, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]

        # STEP 6: If the image has at least one contour, keep only the biggest one, otherwise exit
        if len(contours) == 0:
            three_channels_opened_hand = cv.cvtColor(opened_hand, cv.COLOR_GRAY2RGB)
            self.show_intermediary_step(three_channels_opened_hand, intermediary_steps, 'Final Image')
            return three_channels_opened_hand, -1
        else:
            largest_contour = sorted(contours, key=cv.contourArea)[-1]
            contour_area = cv.contourArea(largest_contour)

            # If largest area does not cover at least 30% of the image, it is considered that no handsign was shown
            if contour_area < (0.15 * opened_hand.shape[0] * opened_hand.shape[1]):
                three_channels_opened_hand = cv.cvtColor(opened_hand, cv.COLOR_GRAY2RGB)
                self.show_intermediary_step(three_channels_opened_hand, intermediary_steps, 'Final Image')
                return three_channels_opened_hand, - 1

            final_image = np.zeros(shape=opened_hand.shape, dtype=np.uint8)
            contoured_image = cv.drawContours(final_image, [largest_contour], 0, (255, 255, 255), -2)
            self.show_intermediary_step(contoured_image, intermediary_steps, 'Contoured Image')

            if image_type == IMAGE_TYPE[0]:
                # STEP 7 (IF RGB): keep only pixels from contoured image
                extracted_hand = cv.bitwise_and(extracted_image, extracted_image, mask=contoured_image)
            else:
                # STEP 7 (IF BINARY): extend the one-channeled binary image to three channels
                extracted_hand = cv.cvtColor(contoured_image,cv.COLOR_GRAY2RGB)

            self.show_intermediary_step(extracted_hand, intermediary_steps, 'Final Image')
            return extracted_hand, 0

    def set_background_subtractor(self):
        self._background_subtractor = cv.createBackgroundSubtractorMOG2(0, 50, detectShadows=False)

    def reset_background_subtractor(self):
        self._background_subtractor = None

    def  get_background_subtractor(self):
        return self._background_subtractor

    def set_hand_index(self, hand_index):
        self._hand_index = hand_index

    @staticmethod
    def show_intermediary_step(image, intermediary_steps, step):
        if intermediary_steps[step]:
            cv.imshow(step, image)


