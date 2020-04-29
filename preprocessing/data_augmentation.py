import os
import cv2 as cv
from base_constants.general_constants import CLASSES
from exceptions import ImageNotLoadedException
from preprocessing.constants import ROTATION_ANGLE_LOWER_LIMIT, SCALING_FACTOR_LOWER_LIMIT, ROTATION_ANGLE_UPPER_LIMIT, \
    SCALING_FACTOR_UPPER_LIMIT
from preprocessing.image_preprocessing import scaling_with_padding, rotating_with_cropping, rotating


def data_augmentation(path_to_folder, new_folder_name):
    path_to_new_base_folder = os.path.join(os.path.dirname(path_to_folder), new_folder_name)
    # TODO: First check if path exists and then delete it, otherwise it will fail
    # os.rmdir(path_to_new_base_folder)
    os.mkdir(path_to_new_base_folder)

    for category in CLASSES:
        path_to_class_folder = os.path.join(path_to_folder, category)
        path_to_new_sub_folder = os.path.join(path_to_new_base_folder, category)
        os.mkdir(path_to_new_sub_folder)
        for image in os.listdir(path_to_class_folder):
            try:
                path_to_image = os.path.join(path_to_class_folder, image)
                image_base_name = os.path.basename(path_to_image)
                read_image = cv.imread(path_to_image, cv.IMREAD_UNCHANGED)

                if read_image.size == 0:
                    raise ImageNotLoadedException

                scaling_factor = SCALING_FACTOR_LOWER_LIMIT

                while scaling_factor <= SCALING_FACTOR_UPPER_LIMIT:
                    rotating_angle = ROTATION_ANGLE_LOWER_LIMIT
                    while rotating_angle <= ROTATION_ANGLE_UPPER_LIMIT:
                        rotated_image = rotating_with_cropping(read_image, rotating_angle)
                        scaled_and_rotated_image = scaling_with_padding(rotated_image, scaling_factor)

                        image_new_name = os.path.splitext(image_base_name)[0] + '_S' + str(scaling_factor) \
                                         + '_R' + str(rotating_angle) + '.png'
                        path_to_new_image = os.path.join(path_to_new_sub_folder, image_new_name)
                        cv.imwrite(path_to_new_image, scaled_and_rotated_image)

                        rotating_angle = rotating_angle + 5
                    scaling_factor = scaling_factor + 0.25
            except ImageNotLoadedException as e:
                print(e.get_exception_message())
    print('Data Augmentation is Complete...')
