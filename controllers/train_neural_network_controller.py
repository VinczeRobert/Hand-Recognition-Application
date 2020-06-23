from model.cnn_architecture import CNNArchitecture
from model.data_reading import TrainingDataReader
from model.settings import Settings
from view.main_view import MainView


class TrainNeuralNetworkController:
    def __init__(self):
        self.settings = Settings.get_instance()
        self.training_data_reader = TrainingDataReader()
        self.cnn_architecture = CNNArchitecture.get_instance()
        self.dataset_folder = None

        main_view = MainView.get_instance()
        self.train_neural_network_view = main_view.train_neural_network_view

        self.train_neural_network_view.load_dataset_button.clicked.connect(lambda: self.set_dataset_folder())
        self.train_neural_network_view.start_training_button.clicked.connect(lambda: self.train_network())

    def set_dataset_folder(self):
        self.dataset_folder = self.train_neural_network_view.choose_dataset_folder()

    def train_network(self):
        self.training_data_reader.read_training_data(self.dataset_folder)
        self.cnn_architecture.train_model(self.training_data_reader.get_training_data(),
                                          self.training_data_reader.get_training_class_labels())


