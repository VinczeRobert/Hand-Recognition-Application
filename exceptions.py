from abc import abstractmethod


class BaseHRAException(Exception):
    """
    Base class for all HRA Exceptions
    """

    def __init__(self, message=None, parent_exception=None):
        Exception.__init__(self, message, parent_exception)
        self.message = str(message)

    def __str__(self):
        return self.message

    @abstractmethod
    def get_exception_message(self):
        return None


class InvalidFileException(BaseHRAException):
    def __init__(self, message=None):
        super(InvalidFileException, self).__init__(message)

    def get_exception_message(self):
        return "Chosen path does not exist or it is not a file!"


class IncorrectExtensionException(BaseHRAException):
    def __init__(self, extension, message=None):
        self.extension = extension
        super(IncorrectExtensionException, self).__init__(message)

    def get_exception_message(self):
        return "Chosen file should have {} extensions!".format(self.extension)


class InvalidModeException(BaseHRAException):
    def __init__(self, message=None):
        super(InvalidModeException, self).__init__(message)

    def get_exception_message(self):
        return "Mode should be either TRAINED OR UNTRAINED!"


class ImageNotLoadedException(BaseHRAException):
    def __init__(self, message=None):
        super(ImageNotLoadedException, self).__init__(message)

    def get_exception_message(self):
        return "Image was not read, probably because the path is incorrect or does not refer to an image!"
