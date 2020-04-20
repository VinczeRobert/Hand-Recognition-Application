from background_subtraction.background_subtraction import BackgroundSubtractor
from cnn_architecture.cnn_architecture import CNNArchitecture
import h5py
import timeit
import cv2 as cv
import numpy as np
from skimage import img_as_bool
from skimage.transform import resize
from base_constants.general_constants import CLASSES, NUMBER_OF_IMAGES
from frame_obtaining.frame_obtainer import FrameObtainer
from preprocessing.image_preprocessing import convert_to_binary, extend_binary_to_three_channels
from utils import check_first_command_line_argument, check_second_command_line_argument


if __name__ == '__main__':
    path_to_h5 = check_first_command_line_argument()
    mode = check_second_command_line_argument()

    with h5py.File(path_to_h5, 'r') as hf:
        training_data = hf['training_data'][:]
        training_class_labels = hf['training_class_labels'][:]
        # testing_data = hf['testing_data'][:]
        # testing_class_labels = hf['testing_class_labels'][:]

    # shuffle data
    idx = np.random.permutation(NUMBER_OF_IMAGES)
    training_data = training_data[idx]
    training_class_labels = training_class_labels[idx]

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
        # predictions = cnn_architecture.predict_classes_for_images(testing_data)
        # cnn_architecture.compute_confusion_matrix(testing_class_labels, predictions)

    cap_region_x_begin = 0.5
    cap_region_y_end = 0.5
    frame_obtainer = FrameObtainer(cap_region_x_begin, cap_region_y_end)
    frame_obtainer.create_trackbar()
    background_subtractor = BackgroundSubtractor()
    predicted_label = None

    while True:
        original_image = frame_obtainer.read_frame(background_subtractor.is_background_captured(), predicted_label)

        if background_subtractor.is_background_captured():
            background_subtractor.set_frame(original_image)
            background = background_subtractor.extract_background(show_image=True)
            binary_image = convert_to_binary(background, show_image=True)

            image_for_labeling = np.array(np.zeros(shape=(1, 100, 100, 3)))
            binary_image = extend_binary_to_three_channels(binary_image)
            binary_image = cv.normalize(binary_image, None, alpha=0, beta=1, norm_type=cv.NORM_MINMAX, dtype=cv.CV_32F)
            binary_image = img_as_bool(resize(binary_image, (100, 100)))
            image_for_labeling[0] = binary_image
            predicted_class = cnn_architecture.predict_classes_for_images(image_for_labeling)
            predicted_label = CLASSES[predicted_class[0]]

        k = cv.waitKey(10)

        # Press Esc to Exit Program
        if k == 27:
            cv.destroyAllWindows()
            exit(0)
            break
        # Press B to capture Background
        elif k == ord('b'):
            background_subtractor.set_background_captured(True)
            print('Background Captured!')
        elif k == ord('r'):
            background_subtractor.set_background_captured(False)
            print('Background Reset!')
