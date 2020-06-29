import threading
import os
import timeit
from model.cnn_architecture import CNNArchitecture
from model.data_reading import TrainingDataReader
from model.settings import Settings
from view.dialogs import show_error_message
from view.main_view import MainView


class TrainNeuralNetworkController:
    """
    Controller class responsible for handling user input related to training the neural network
    """
    def __init__(self):
        self.training_data_reader = TrainingDataReader()
        self.cnn_architecture = CNNArchitecture.get_instance()
        self._dataset_folder = None

        main_view = MainView.get_instance()
        self.train_neural_network_view = main_view.train_neural_network_view

        self.train_neural_network_view.load_dataset_button.clicked.connect(lambda: self.set_dataset_folder())
        self.train_neural_network_view.start_training_button.clicked.connect(lambda: self.launch_reading_and_training())

    def set_dataset_folder(self):
        self._dataset_folder = self.train_neural_network_view.choose_dataset_folder()

    def launch_reading_and_training(self):
        """
        This method is responsible for validating the dataset path and asynchronously start the data
        reading and neural network training on a different thread.
        """

        if self._dataset_folder is None:
            show_error_message('Choose a dataset folder before you start!')
            return

        classes = self.training_data_reader.init_reading(self._dataset_folder)

        if len(classes) < 3:
            show_error_message('You have chosen a dataset which has 0 or 1 classes! Please choose a dataset with at '
                               'least 2 classes!')
            return

        thread = threading.Thread(target=self.asynchronously_train_network, kwargs={'classes': classes})
        thread.start()

    def asynchronously_train_network(self, classes):
        """
        Method which reads data for each class and then trains the network.
        This method is supposed to be called started in a different thread.
        :param classes: list of identified class folders
        """
        start = timeit.default_timer()
        for category in classes:
            path = os.path.join(self._dataset_folder, category)
            class_num = classes.index(category)

            # Displayer message to interface about the curent class that is being read
            self.train_neural_network_view.appendText('Currently reading data for class {}...\n'.format(
                classes[class_num]))
            # Read data for one class
            status = self.training_data_reader.read_data_for_one_class(path, class_num)

            if status == -1:
                # In case a non-image file has been found or image can't be read, show error message
                # and stop training
                show_error_message(
                    'A non-image file has been found in the dataset path! Please choose a path that only '
                    'contains images.')
                return
        stop = timeit.default_timer()
        print('Total Run Time for Training: {}'.format(stop - start))
        self.train_neural_network_view.appendText('Data has been succesfully read! \n\n'
                                                  'Training the network... Please wait.')
        # After data is read, train the CNN
        self.cnn_architecture.train_model(self.training_data_reader.get_training_data(),
                                          self.training_data_reader.get_training_class_labels())
        self.train_neural_network_view.appendText('The network has been succesfully trained!')

        # Save classes so the new one can be added
        Settings.get_instance().set_classes(classes)
