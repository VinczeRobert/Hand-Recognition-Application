from model.settings import HAND
from view.dialogs import show_error_message
import shutil


def validate_integer(integer_as_string):
    """
    :param integer_as_string: string taken from UI
    :return: result if integer_as_string is represent an int less than 1 000 000, else None
    """
    try:
        result = int(integer_as_string)

        # Not letting start_index or end_index pass one million
        if 0 < result < 1000000:
            return result
        return None

    except ValueError:
        return None

def validate_integer_difference(start_index, end_index):
    """
    The maximum number of frames that can be recorded at once is 3000
    :param start_index: index of first frame
    :param end_index: index of last frame
    :return: result of validation as a boolean
    """
    difference = end_index - start_index

    if 0 < difference <= 3000:
        return True

    return False

def validate_string_characters(text):
    """
    This function makes sure that there are no forbidden characters in a directory or file name
    :param text: path to file/directory
    :return: result of validation as a boolean
    """
    return any(i in text for i in '\\/:*?"<>|')

def check_if_enough_disk_space(upload_path, number_of_images, image_type):
    """
    This function checks if there is enough space on the drive to store the required number of images.
    The maximum required size of one image is set experimentally.
    :param upload_path: path to directory
    :param number_of_images: number of images to be saved
    :param image_type: type of the image (RGB or Binary)
    :return: result of validation as a boolean
    """

    free_space = shutil.disk_usage(upload_path).free

    if image_type == HAND[0]:
        required_space = number_of_images * 40
    else:
        required_space = number_of_images * 20

    return required_space < free_space

def validate_add_new_sign(upload_path, class_name, start_index, end_index, image_type):
    """
    Main validation function for adding a new sign which uses the functions above
    (See the functions above for parameters)
    """
    if upload_path is None:
        show_error_message('Choose a dataset folder before you start!')
        return False

    if class_name == '':
        show_error_message('Please choose a name for your new gesture!')
        return False
    elif len(class_name) > 50:
        show_error_message('Please choose a gesture name with less than 50 characters!')
        return False
    elif validate_string_characters(class_name):
        show_error_message('Class name can not contain any of the following characters: \\/:*?"<>|')
        return False

    start_index = validate_integer(start_index)
    if start_index is None:
        show_error_message('Start Index has to be a positive integer less than 1 000 000!')
        return False

    end_index = validate_integer(end_index)
    if end_index is None:
        show_error_message('End Index has to be a positive integer less than 1 000 000!')
        return False

    index_difference = end_index - start_index
    if validate_integer_difference(start_index, end_index) is False:
        show_error_message('End Index must be bigger than Start Index and the difference between the two has '
                           'to be at most 3000!')
        return False

    if not (check_if_enough_disk_space(upload_path, index_difference, image_type)):
        show_error_message('There is no enough disk space to store the required image number! Please try to clean up '
                           'some space, use a different disk or choose a lower number of images!')
    return True
