import cv2 as cv
import numpy as np
from preprocessing.constants import BLUR_VALUE, THRESHOLD, CONTOUR_RETRIEVAL_MODE, APPROXIMATION_METHOD


def smoothing(captured_frame):
    """
    Applies bilateral filter to a frame extracted from the real-time video captures and flips it around the y-axis
    :param captured_frame: captured frame
    :return: smoothed and flipped image
    """
    filtered_image = cv.bilateralFilter(captured_frame, 9, 75, 75)
    filtered_image = cv.flip(filtered_image, 1)
    return filtered_image


def convert_to_binary(color_image, show_image=False):
    """
    Converts an image to binary
    :param color_image: input image
    :param show_image: optionally show the binary image
    :return: binary representation of the input image
    """
    gray_image = cv.cvtColor(color_image, cv.COLOR_BGR2GRAY)
    blurred_image = cv.GaussianBlur(gray_image, (BLUR_VALUE, BLUR_VALUE), 0)
    _, binary_image = cv.threshold(blurred_image, THRESHOLD, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    if show_image:
        cv.imshow('Binary Image', binary_image)
    return binary_image


def scaling(original_image, scaling_factor, show=False):
    """
    Scales an image along both axes with the same scaling_factor resulting in a resized images,
    which will have its size equal to the old size multiplied by the scaling_factor
    :param original_image: input image
    :param scaling_factor: parameter which will determine the size of the scaled image
    :param show: optionally show the scaled image
    :return: scaled image
    """
    scaled_image = cv.resize(original_image, (int(original_image.shape[1] * scaling_factor),
                                              int(original_image.shape[0] * scaling_factor)),
                             interpolation=cv.INTER_AREA)
    if show:
        cv.imshow("Resized Image with scaling_factor of {}".format(scaling_factor), scaled_image)
    return scaled_image


def padding(resized_image, old_size, show=False):
    """
    This function is used because we don't want to resize the whole image, we want just the hand part.
    Thus, this function takes out the image of the resized hand and puts it back in the original one.
    :param resized_image: resized image from which we have to extract the hand
    :param old_size: size of the original image
    :param show: optionally show the image
    :return: padded image
    """
    x_padding = int((old_size[1] - resized_image.shape[1]) / 2)
    y_padding = int((old_size[0] - resized_image.shape[0]) / 2)

    padded_image = np.zeros(shape=old_size, dtype=np.uint8)

    if x_padding > 0:
        # When the resized image is smaller than the original one
        for i in range(y_padding, old_size[0] - y_padding - 1):
            for j in range(x_padding, old_size[1] - x_padding - 1):
                padded_image[i][j] = resized_image[i - y_padding][j - x_padding]
    else:
        # When the resized image is bigger than the original one
        x_padding = abs(x_padding)
        y_padding = abs(y_padding)
        for i in range(old_size[0] - 1):
            for j in range(old_size[1] - 1):
                padded_image[i][j] = resized_image[i+y_padding][j+x_padding]
    if show:
        cv.imshow('Resized Image with Padding', padded_image)
    return padded_image


def scaling_with_padding(original_image, scaling_factor, show=False):
    """
    Scales only the hand part of the image
    :param original_image: input image
    :param scaling_factor: parameter which will determine the size of the scaled image
    :param show: optionally show the new image where only the hand is resized
    :return: return the new image where only the hand is resized
    """
    new_size = original_image.shape
    scaled_image = scaling(original_image, scaling_factor, show)
    padded_image = padding(scaled_image, new_size, show)
    return padded_image


def rotating(original_image, rotation_angle, show=False):
    """
    Rotates an image without cropping it
    :param original_image: input image
    :param rotation_angle: angle of rotation (if bigger than 0, the image is rotated counter-clockwise,
     otherwise clockwise)
    :param show: optionally show the rotated image
    :return: rotated image
    """
    height, width = original_image.shape[:2]
    center = (width / 2, height / 2)

    rotation_matrix = cv.getRotationMatrix2D(center, rotation_angle, 1.0)

    abs_cos = abs(rotation_matrix[0, 0])
    abs_sin = abs(rotation_matrix[0, 1])

    new_width = int(height * abs_sin + width * abs_cos)
    new_height = int(height * abs_cos + width * abs_sin)

    rotation_matrix[0, 2] += new_width / 2 - center[0]
    rotation_matrix[1, 2] += new_height / 2 - center[1]

    rotated_image = cv.warpAffine(original_image, rotation_matrix, (new_width, new_height))
    if show:
        cv.imshow("Rotated Image with an angle of {}".format(rotation_angle), rotated_image)
    return rotated_image


def finding_largest_contour(original_image):
    """
    Takes a binary image and returns the contour of the biggest object
    :param original_image: input image
    :return: largest contour
    """
    if len(original_image.shape) > 2:
        original_image = convert_to_binary(original_image)
    contours, _ = cv.findContours(original_image, CONTOUR_RETRIEVAL_MODE, APPROXIMATION_METHOD)

    if len(contours) == 0:
        return []

    largest_contour = sorted(contours, key=cv.contourArea)[-1]
    return largest_contour


def drawing_contour(binary_image, show=False):
    """
    Draws the contour of the biggest object from a binary image
    :param binary_image: input image
    :param show: optionally show the contour
    :return: contoured_image
    """
    largest_area = finding_largest_contour(binary_image)
    contoured_image = np.zeros(shape=binary_image.shape, dtype=np.uint8)
    contoured_image = cv.drawContours(contoured_image, [largest_area], 0, (255, 255, 255), 2)
    if show:
        cv.imshow('Contoured Image', contoured_image)
    return contoured_image


def rotating_with_cropping(original_image, rotation_angle, show=False):
    """
    Rotating a binary image and cropping out only the region of interest by using a bounding box
    :param original_image: input image
    :param rotation_angle: angle of rotation (if bigger than 0, the image is rotated counter-clockwise,
     otherwise clockwise)
    :param show: optionally showing the rotated and cropped image
    :return: rotated and cropped image
    """
    rotated_image = rotating(original_image, rotation_angle, show)
    cropped_image = cropping(rotated_image, show)
    return cropped_image


def thresholding_rgb_images(original_image, show=False):
    grayscale = cv.cvtColor(original_image, cv.COLOR_RGB2GRAY)
    blurred = cv.GaussianBlur(grayscale, (BLUR_VALUE, BLUR_VALUE), 0)
    _, thresholded = cv.threshold(blurred, 100, 255, cv.THRESH_TOZERO)

    for i in range(thresholded.shape[1]):
        for j in range(thresholded.shape[0]):
            if thresholded[j][i] == 0:
                original_image[j][i] = [0, 0, 0]

    if show:
        cv.imshow('Thresholded RGB Image', original_image)
        cv.imshow('Blurred RGB Image', blurred)
    return original_image
