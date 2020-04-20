import cv2 as cv
import os
import numpy as np
from base_constants.general_constants import CLASSES
from preprocessing.constants import BLUR_VALUE, THRESHOLD


def convert_to_binary(color_image, show_image=False):
    gray_image =cv.cvtColor(color_image, cv.COLOR_BGR2GRAY)
    blurred_image = cv.GaussianBlur(gray_image, (BLUR_VALUE, BLUR_VALUE), 0)
    _, binary_image = cv.threshold(blurred_image, THRESHOLD, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    if show_image:
        cv.imshow('Binary Image', binary_image)
    return binary_image


def convert_folder_to_binary(path_to_folder):
    path_to_new_base_folder = os.path.join(os.path.dirname(path_to_folder), 'Only_Letters_Binary')
    os.mkdir(path_to_new_base_folder)
    for category in CLASSES:
        path = os.path.join(path_to_folder, category)
        path_to_new_sub_folder = os.path.join(path_to_new_base_folder, category)
        os.mkdir(path_to_new_sub_folder)
        for image in os.listdir(path):
            try:
                path_to_image = os.path.join(path, image)
                color_image = cv.imread(path_to_image, cv.IMREAD_COLOR)
                binary_image = convert_to_binary(color_image)
                image_base_name = os.path.basename(path_to_image)
                path_to_new_image = os.path.join(path_to_new_sub_folder, image_base_name)
                cv.imwrite(path_to_new_image, binary_image)
            except Exception as e:
                pass


def smoothing(image):
    filtered_image = cv.bilateralFilter(image, 5, 50, 100)
    filtered_image = cv.flip(filtered_image, 1)
    return filtered_image


def extend_binary_to_three_channels(image):
    three_channel_binary = np.zeros(shape=(image.shape[0], image.shape[1], 3))
    three_channel_binary[:,:,0] = image
    three_channel_binary[:,:,1] = image
    three_channel_binary[:,:,2] = image

    return three_channel_binary
