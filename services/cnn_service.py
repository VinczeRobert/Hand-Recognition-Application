from base_constants.general_constants import CLASSES
from model.cnn_architecture import CNNArchitecture


class CNNService:
    def __init__(self):
        self.cnn_architecture = CNNArchitecture()
        self.cnn_architecture.build_model()
        self.cnn_architecture.load_weights()

    def predict_class(self, cnn_input):
        predicted_class = self.cnn_architecture.predict_classes_for_images(cnn_input)
        return CLASSES[predicted_class[0]]

