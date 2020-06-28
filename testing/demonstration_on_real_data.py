import cv2 as cv
from model.frame_captor import FrameCaptor
from model.frame_displayer import FrameDisplayer
from model.image_preprocessor import ImagePreprocessor
from model.predictor import Predictor
from model.settings import Settings, HAND, IMAGE_TYPE


def real_time_test_for_one_class(class_name, hand_index, image_type):
    settings = Settings.get_instance()
    frame_captor = FrameCaptor.get_instance(settings.get_android_server_url())
    frame_captor.set_capture_mode()
    image_preprocessor = ImagePreprocessor(hand_index=hand_index)
    frame_displayer = FrameDisplayer(hand_index=hand_index)
    predictor = Predictor('../data/weights/weights_left_binary.ckpt', settings.get_classes())

    correct_predictions = 0
    total_predictions = 0
    start = False

    while True:
        image = frame_captor.read_frame()

        if image_preprocessor.get_background_subtractor() is not None:
            preprocessed_image = image_preprocessor.prepare_image_for_classification(image, image_type,
                                                                                     settings.get_intermediary_steps())[0]
            cv.imshow('Preprocessed Image', preprocessed_image)
            if start:
                new_predicted_sign = predictor.predict_hand_gesture(preprocessed_image, False)

                if new_predicted_sign == class_name:
                    correct_predictions = correct_predictions + 1
                total_predictions = total_predictions + 1

                if total_predictions > 200:
                    break

        display_image = frame_displayer.display_frame(image, total_predictions)
        cv.imshow('Testing Module', display_image)

        k = cv.waitKey(10)

        if k == ord('b'):
            image_preprocessor.set_background_subtractor()
        if k == ord('s'):
            if image_preprocessor.get_background_subtractor() is not None:
                start = True

    print('Real Time Accuracy for class {} is {}%.'.format(
        class_name, float(correct_predictions/total_predictions * 100)))


if __name__ == '__main__':
    real_time_test_for_one_class('Delete', HAND[1], IMAGE_TYPE[1])

