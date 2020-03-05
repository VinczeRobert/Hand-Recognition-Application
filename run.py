from data_collecting.training_data_reader import TrainingDataReader
import pickle
import sys

if __name__ == '__main__':
    training_data_reader = TrainingDataReader()

    if sys.argv[2] == 'NORMAL_READ':
        training_data_reader.read_training_data()
        with open('training_data_pickle', 'wb') as f:
            pickle.dump(training_data_reader.training_data, f)
    elif sys.argv[2] == 'PICKLE_READ':
        with open('training_data_pickle', 'rb') as f:
            training_data_reader.training_data = pickle.load(f)
    else:
        print('Invalid second argument!')