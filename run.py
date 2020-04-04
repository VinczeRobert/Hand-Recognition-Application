from cnn_architecture.cnn_architecture import CNNArchitecture
import h5py
import timeit
from utils import check_first_command_line_argument, check_second_command_line_argument


if __name__ == '__main__':
    path_to_h5 = check_first_command_line_argument()
    mode = check_second_command_line_argument()

    with h5py.File(path_to_h5, 'r') as hf:
        training_data = hf['training_data'][:]
        training_class_labels = hf['training_class_labels'][:]
        testing_data = hf['testing_data'][:]
        testing_class_labels = hf['testing_class_labels'][:]

    cnn_architecture = CNNArchitecture()
    cnn_architecture.build_model()
    if mode == "UNTRAINED":
        # If the model hasn't been trained, we train it and we are curious to know the time it takes
        start = timeit.default_timer()
        cnn_architecture.train_model(training_data, training_class_labels)
        stop = timeit.default_timer()
        print('Total Run Time for Training: {}'.format(stop - start))
    else:
        # If model has been already trained and you have the weights file, you don't need to train the model again
        cnn_architecture.model.load_weights('data/weights/weights.ckpt')
    cnn_architecture.evaluate_model(testing_data, testing_class_labels)
