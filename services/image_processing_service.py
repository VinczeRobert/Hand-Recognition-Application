from PIL import Image
import numpy as np

from model.hand_detector.hand_detector import HandDetector


class ImageProcessingService:
    def __init__(self, frame_count=32):
        self._frame_count = frame_count
        self._total_frames = 0
        self._current_image = 0
        self._hand_detector = HandDetector(accum_weight=0.1)

    def set_current_image(self, new_image):
        self._current_image = new_image

    def get_current_image(self):
        return self._current_image

    def detect_hand(self, hand_index=0):
        image_object = Image.open(self._current_image)
        self._current_image = np.asarray(image_object)
        self._current_image = self._hand_detector.smooth_image(self._current_image)

        if self._total_frames > self._frame_count:
            background_difference = self._hand_detector.extract_background_difference(self._current_image, hand_index)





    def resize_image(self):


