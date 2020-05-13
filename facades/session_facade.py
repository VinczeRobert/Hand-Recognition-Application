from services.cnn_service import CNNService
from services.image_processing_service import ImageProcessingService


class SessionFacade:
    def __init__(self):
        self.cnn_service = CNNService()
        self.image_processing_service = ImageProcessingService()

    def get_prediction_for_image(self, image):
        self.image_processing_service.set_current_image(image)
        self.image_processing_service.convert_to_numpy_image()






