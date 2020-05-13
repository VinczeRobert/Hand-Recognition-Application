from model.cnn_architecture import CNNArchitecture


class CNNService:
    def __init__(self):
        self.cnn_architecture = CNNArchitecture()
        self.cnn_architecture.build_model()
        self.cnn_architecture.load_weights()

