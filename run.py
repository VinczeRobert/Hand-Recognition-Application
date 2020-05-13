from model.background_subtraction import BackgroundSubtractor
from model.cnn_architecture import CNNArchitecture
import timeit
import os
import cv2 as cv
import numpy as np
from base_constants.general_constants import CLASSES, H5_PATH, IMAGE_SIZE_X, IMAGE_SIZE_Y, \
    WEIGHTS_LEFT_PATH, WEIGHTS_RIGHT_PATH
from data_reading.data_reading import TrainingDataReader
from model.frame_captor import FrameCaptor
from preprocessing.image_preprocessing import cropping
from utils import check_first_command_line_argument
from visualization.accuracy_and_loss_viewer import AccuracyLossViewer

if __name__ == '__main__':
    mode = check_first_command_line_argument()

    cnn_architecture = CNNArchitecture()
    cnn_architecture.build_model()

    if mode == "DEVELOPER_MODE":
        training_data_reader = TrainingDataReader()
        if not os.path.isfile(H5_PATH):
            training_data_reader.read_training_data()
            training_data_reader.split_data()
            training_data_reader.save_to_h5(H5_PATH)
        else:
            training_data_reader.load_from_h5(H5_PATH)

        # In developer mode, the model is trained and the total time for training is calculated
        start = timeit.default_timer()
        cnn_architecture.train_model(training_data_reader.training_data, training_data_reader.training_class_labels)
        stop = timeit.default_timer()
        print('Total Run Time for Training: {}'.format(stop - start))

        # After the training is done, the model is tested with the testing data with total time
        # calculated just like before
        start = timeit.default_timer()
        cnn_architecture.evaluate_model(training_data_reader.testing_data, training_data_reader.testing_class_labels)
        stop = timeit.default_timer()
        print('Total Time for Testing: {}'.format(stop - start))

        # Developers are also interested on seeing the plot of the validation accuracy,
        # the validation_loss and the confusion matrix on testing data
        acc_loss_viewer = AccuracyLossViewer(cnn_architecture.history)
        acc_loss_viewer.plot_accuracy()
        acc_loss_viewer.plot_loss()

        predicted_classes = cnn_architecture.predict_classes_for_images(training_data_reader.testing_data)
        cnn_architecture.compute_confusion_matrix(training_data_reader.testing_class_labels, predicted_classes)

    else:
        # In client mode the CNN model is already trained and the file with the weights should exist at WEIGHTS_PATH
        hand_index = 1
        if hand_index == 0:
            weights_path = WEIGHTS_RIGHT_PATH
        else:
            weights_path = WEIGHTS_LEFT_PATH

        cnn_architecture.model.load_weights(weights_path)

        frame_captor = FrameCaptor(hand_index=hand_index)
        frame_captor.set_capture_mode()
        background_subtractor = BackgroundSubtractor()
        predicted_letter = None

        while True:
            original_image = frame_captor.read_frame(background_subtractor.is_background_captured(), predicted_letter)

            if background_subtractor.is_background_captured():
                # Extract the difference, eliminate the unnecessary background parts via cropping and we resize it
                # to the dimension that the CNN Architecture expects
                background_subtractor.set_frame(original_image)
                captured_image = background_subtractor.extract_background_difference(hand_index=frame_captor.hand_index, show_image=True)
                cropped = cropping(captured_image)
                cropped = cv.resize(cropped, (IMAGE_SIZE_X, IMAGE_SIZE_Y))

                # Normalize the image and feed it to the CNN model to get the predicted class
                next_image = np.array(np.zeros(shape=(1, IMAGE_SIZE_X, IMAGE_SIZE_Y, 3)))
                normalized_image = cv.normalize(cropped, None, alpha=0, beta=1, norm_type=cv.NORM_MINMAX, dtype=cv.CV_32F)
                next_image[0] = normalized_image
                predicted_class = cnn_architecture.predict_classes_for_images(next_image)
                predicted_letter = CLASSES[predicted_class[0]]

            k = cv.waitKey(10)

            # Press Esc to Exit Program
            if k == 27:
                cv.destroyAllWindows()
                exit(0)
            # Press B to capture Background
            elif k == ord('b'):
                background_subtractor.set_background_captured(True)
                print('Background Captured!')
            # Press R to eliminate current Background, then press B again to capture it again
            elif k == ord('r'):
                background_subtractor.set_background_captured(False)
                background_subtractor.reset_background()
                print('Background Reset!')

