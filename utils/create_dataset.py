import os
import cv2 as cv
import timeit
from model.frame_captor import FrameCaptor
from model.frame_displayer import FrameDisplayer
from model.image_preprocessor import ImagePreprocessor


def create_data_for_class(path_to_folder, class_name, is_binary=False, start_count=1, end_count=1000,
                          camera_init_url='', hand_index=0, var_threshold=50):
    # Creating folders if they are not existing
    if not os.path.exists(path_to_folder):
        os.mkdir(path_to_folder)

    image_path = os.path.join(path_to_folder, class_name)

    if not os.path.exists(image_path):
        os.mkdir(image_path)

    # Initializing
    frame_captor = FrameCaptor(camera_init_url)
    frame_captor.set_capture_mode()
    image_preprocessor = ImagePreprocessor(hand_index, var_threshold)
    frame_display = FrameDisplayer(hand_index)
    start = False
    background_captured = False

    while True:
        image = frame_captor.read_frame()
        start_time = timeit.default_timer()
        flipped_image = cv.flip(image, 1)

        if background_captured is True:
            preprocessed_image, status = image_preprocessor.prepare_image_for_classification(flipped_image,
                                                                                         is_binary=is_binary)


            if start:
                save_path = os.path.join(image_path, class_name + '_{}.jpg'.format(start_count))

                # while True:

                    #difference = stop_time - start_time

                    # if difference > 0.25:
                if status != -1:
                    cv.imwrite(save_path, preprocessed_image)
                    start_count = start_count + 1
                        # break

            if start_count > end_count:
                break

        frame_display.display_frame(flipped_image, start_count, '')

        key = cv.waitKey(10)

        if key == ord('s') and background_captured:
            start = True
        elif key == ord('b'):
            background_captured = True
            image_preprocessor.set_background_subtractor()
        elif key == ord('q'):
            cv.destroyAllWindows()
            exit(0)

    cv.destroyAllWindows()
    exit(0)


if __name__ == '__main__':
    path_to_folder = 'D:/Hand Gesture Datasets/Self_Made_ASL_Dataset'
    class_name = 'I'
    create_data_for_class(path_to_folder, class_name, hand_index=1)

