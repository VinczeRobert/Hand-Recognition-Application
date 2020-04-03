from cnn_architecture.cnn_architecture import CNNArchitecture
import h5py
import timeit


if __name__ == '__main__':

    start = timeit.default_timer()

    cnn_architecture = CNNArchitecture()

    with h5py.File('data/hra_training_data.h5', 'r') as hf:
            training_data = hf['training_data'][:]
            training_class_labels = hf['training_class_labels'][:]
            testing_data = hf['testing_data'][:]
            testing_class_labels = hf['testing_class_labels'][:]

    cnn_architecture.build_model()
    cnn_architecture.train_model(training_data, training_class_labels)

    cnn_architecture.evaluate_model(testing_data, testing_class_labels)

    stop = timeit.default_timer()
    print('Total Run Time for Loading, Training and Testing: {}'.format(stop-start))