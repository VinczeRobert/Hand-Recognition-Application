import cv2 as cv
import os
import numpy as np
from base_constants.general_constants import CLASSES
from preprocessing.constants import BLUR_VALUE, THRESHOLD, CONTOUR_RETRIEVAL_MODE, APPROXIMATION_METHOD


def convert_to_binary(color_image, show_image=False):
    gray_image =cv.cvtColor(color_image, cv.COLOR_BGR2GRAY)
    blurred_image = cv.GaussianBlur(gray_image, (BLUR_VALUE, BLUR_VALUE), 0)
    _, binary_image = cv.threshold(blurred_image, THRESHOLD, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    if show_image:
        cv.imshow('Binary Image', binary_image)
    return binary_image


def convert_folder_to_binary(path_to_folder, resize=False, scaling_factor=1.0):
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
                if resize:
                    color_image = scaling(image, scaling_factor)
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


def scaling(image, scaling_factor, show=False):
    image = cv.resize(image, (int(image.shape[1] * scaling_factor), int(image.shape[0] * scaling_factor)), interpolation=cv.INTER_AREA)
    if show:
        cv.imshow("Resized Image with scaling_factor of {}".format(scaling_factor), image)
    return image


def rotating(image, rotation_angle, show=False):
    height, width = image.shape[:2]
    center = (width / 2, height / 2)

    rotation_matrix = cv.getRotationMatrix2D(center, rotation_angle, 1.0)

    abs_cos = abs(rotation_matrix[0, 0])
    abs_sin = abs(rotation_matrix[0, 1])

    new_width = int(height * abs_sin + width * abs_cos)
    new_height = int(height * abs_cos + width * abs_sin)

    rotation_matrix[0, 2] += new_width/2 - center[0]
    rotation_matrix[1, 2] += new_height/2 - center[1]

    image = cv.warpAffine(image, rotation_matrix, (new_width, new_height))
    if show:
        cv.imshow("Rotated Image with an angle of {}".format(rotation_angle), image)
    return image


def padding(image, new_size, scaling_factor, show=False):
    x_padding = int((new_size[1] - image.shape[1]) / 2)
    y_padding = int((new_size[0] - image.shape[0]) / 2)

    padded_image = np.zeros(shape=new_size, dtype=np.uint8)
    for i in range(y_padding, new_size[0] - y_padding-1):
        for j in range(x_padding, new_size[1] - x_padding-1):
            padded_image[i][j] = image[i-y_padding][j-x_padding]
    if show:
        cv.imshow('Resized Image with Padding', padded_image)
    return padded_image


def scaling_with_padding(image, scaling_factor, show=False):
    new_size = image.shape
    scaled_image = scaling(image, scaling_factor, show)
    padded_image = padding(scaled_image, new_size, scaling_factor, show)
    return padded_image


def finding_contour(binary_image, show=False):
    contours, _ = cv.findContours(binary_image, CONTOUR_RETRIEVAL_MODE, APPROXIMATION_METHOD)
    contoured_image = np.zeros(shape=binary_image.shape, dtype=np.uint8)
    largest_areas = sorted(contours, key=cv.contourArea)
    contoured_image = cv.drawContours(contoured_image, [largest_areas[-1]], 0, (255, 255, 255), 2)
    if show:
        cv.imshow('Contoured Image', contoured_image)
    return contoured_image


def finding_bounding_box(binary_image, show=False):
    contours, _ = cv.findContours(binary_image, CONTOUR_RETRIEVAL_MODE, APPROXIMATION_METHOD)
    largest_area = sorted(contours, key=cv.contourArea)[-1]
    x, y, w, h = cv.boundingRect(largest_area)
    bounding_boxed = binary_image[y:y+h, x:x+w]
    if show:
        cv.imshow('Bounding Boxed Image', bounding_boxed)
    return bounding_boxed


path = 'C:/Users/robi997/Downloads/Hand_Gesture_Dataset/Training/Only_Letters_Binary/G/hand1_g_bot_seg_2_cropped.png'
image = cv.imread(path, cv.IMREAD_UNCHANGED)
cv.imshow("Original", image)
rotated = rotating(image, 30, True)
finding_bounding_box(rotated, True)
# scaling(image, 1.5, True)
# rotating(image, 30, True)
cv.waitKey(0)



