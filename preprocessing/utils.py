import os
import cv2 as cv
from base_constants.general_constants import CLASSES
from exceptions import ImageNotLoadedException
from preprocessing.image_preprocessing import scaling, convert_to_binary


def convert_folder_to_binary(path_to_folder, resize=False, scaling_factor=1.0):
    """
    Converts a folder of RGB images to binary images
    :param path_to_folder: the path has to lead to a folder, which is supposed to have sub-folders for each class and
    the images belonging to those classes should all be in their respective sub-folders
    :param resize: Optionally resizing the images
    :param scaling_factor: Factors which sets the new dimension of the resized images
    :return: void
    """
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
                if color_image.size == 0:
                    raise ImageNotLoadedException
                if resize:
                    color_image = scaling(image, scaling_factor)
                binary_image = convert_to_binary(color_image)
                image_base_name = os.path.basename(path_to_image)
                path_to_new_image = os.path.join(path_to_new_sub_folder, image_base_name)
                cv.imwrite(path_to_new_image, binary_image)
            except ImageNotLoadedException as e:
                print(e.get_exception_message())
