import sys
import os
from base_constants.general_constants import DATA_EXTENSION, RUN_MODES
from exceptions import InvalidFileException, IncorrectExtensionException, InvalidModeException


def check_first_command_line_argument():
    """
    This function checks if the first command line argument is one of the valid modes: CLIENT_MODE or DEVELOPER_MODE.
    :return: the mode that the application will run in
    """
    try:
        mode = sys.argv[1]

        if not (mode in RUN_MODES):
            raise InvalidModeException
        return mode
    except InvalidModeException as e:
        print(e.get_exception_message())
    except IndexError:
        print("First command line argument is missing!")
        sys.exit(1)


def check_second_command_line_argument():
    """
    This function checks if the second command line argument is a path to an existing .h5 file
    :return: the path to the .h5 file with the separated numpy arrays and class labels for training and testing
    """
    try:
        path_to_h5 = sys.argv[2]

        if not os.path.isfile(path_to_h5):
            raise InvalidFileException
        if not path_to_h5.endswith(DATA_EXTENSION):
            raise IncorrectExtensionException(DATA_EXTENSION)

        return path_to_h5
    except InvalidFileException as e:
        print(e.get_exception_message())
        return None
    except IncorrectExtensionException as e:
        print(e.get_exception_message())
        return None
    except IndexError:
        return None
