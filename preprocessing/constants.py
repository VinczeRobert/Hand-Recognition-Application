import cv2 as cv


THRESHOLD = 60
BLUR_VALUE = 17
BACKGROUND_SUB_THRESHOLD = 50
ETA = 0
RESIZE_DIMENSION = 200
ERODE_ITERATIONS = 5
MASK_SIZE = 5
SAMPLING_STEP = 5

APPROXIMATION_METHOD =cv.CHAIN_APPROX_SIMPLE
CONTOUR_RETRIEVAL_MODE = cv.RETR_LIST

FOLDER_CONVERSIONS = {
    'BINARY': 0,
    'GRAYSCALE': 1,
    'CONTOUR': 2
}

SCALING_FACTOR_LOWER_LIMIT = 0.5
SCALING_FACTOR_UPPER_LIMIT = 1.5
ROTATION_ANGLE_LOWER_LIMIT = -30
ROTATION_ANGLE_UPPER_LIMIT = 30
