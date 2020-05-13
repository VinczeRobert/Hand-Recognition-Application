import os
import cv2 as cv
from base_constants.general_constants import CLASSES
from exceptions import ImageNotLoadedException
from model.frame_captor import FrameCaptor
from preprocessing.constants import FOLDER_CONVERSIONS
from preprocessing.image_preprocessing import scaling, convert_to_binary, drawing_contour


def convert_folder(path_to_folder, new_folder_name, conversion_mode=FOLDER_CONVERSIONS['BINARY'],
                   resize=False, scaling_factor=1.0):
    """
    Converts a folder of RGB images to binary, grayscale or contour images. Binary is default.
    :param path_to_folder: the path has to lead to a folder, which is supposed to have sub-folders for each class and
    the images belonging to those classes should all be in their respective sub-folders
    :param new_folder_name: name of new folder
    :param resize: Optionally resizing the images
    :param conversion_mode: 0 = Binary, 1 = Grayscale, 2 = Contour
    :param scaling_factor: Factors which sets the new dimension of the resized images
    :return: void
    """

    path_to_new_base_folder = os.path.join(os.path.dirname(path_to_folder), new_folder_name)

    if os.path.exists(path_to_new_base_folder):
        os.rmdir(path_to_new_base_folder)

    os.mkdir(path_to_new_base_folder)
    for category in CLASSES:
        path = os.path.join(path_to_folder, category)
        path_to_new_sub_folder = os.path.join(path_to_new_base_folder, category)
        os.mkdir(path_to_new_sub_folder)
        for image in os.listdir(path):
            try:
                path_to_image = os.path.join(path, image)
                image_base_name = os.path.basename(path_to_image)
                color_image = cv.imread(path_to_image, cv.IMREAD_COLOR)

                if color_image.size == 0:
                    raise ImageNotLoadedException

                if resize:
                    color_image = scaling(image, scaling_factor)

                if conversion_mode == FOLDER_CONVERSIONS['BINARY']:
                    new_image = convert_to_binary(color_image)
                elif conversion_mode == FOLDER_CONVERSIONS['GRAYSCALE']:
                    new_image = cv.cvtColor(color_image, cv.COLOR_BGR2GRAY)
                else:
                    binary_image = convert_to_binary(color_image)
                    new_image = drawing_contour(binary_image)

                path_to_new_image = os.path.join(path_to_new_sub_folder, image_base_name)
                cv.imwrite(path_to_new_image, new_image)
            except ImageNotLoadedException as e:
                print(e.get_exception_message())
    print('Folder Conversion is Complete...')
