from cnn_architecture.cnn_architecture import CNNArchitecture
from data_collecting.training_data_reader import TrainingDataReader
import h5py
import sys
import timeit


if __name__ == '__main__':

    start = timeit.default_timer()

    training_data_reader = TrainingDataReader()
    cnn_architecture = CNNArchitecture()

    if sys.argv[2] == 'LONG_READ':
        training_data_reader.read_training_data()
        with h5py.File('hra_training_data.h5', 'w') as hf:
            hf.create_dataset("training_data", data=training_data_reader.training_data)
            hf.create_dataset("class_labels", data=training_data_reader.class_labels)

    elif sys.argv[2] == 'H5_READ':
        with h5py.File('hra_training_data.h5', 'r') as hf:
            training_data_reader.training_data = hf['training_data'][:]
            training_data_reader.class_labels = hf['class_labels'][:]
    else:
        print('Invalid second argument!')

    cnn_architecture.build_model()
    cnn_architecture.train_model(training_data_reader.training_data, training_data_reader.class_labels)

    stop = timeit.default_timer()

    print('Total Run Time: {}'.format(stop-start))