import numpy as np
from base_constants.general_constants import IMAGE_SIZE_X, IMAGE_SIZE_Y, CLASSES
from preprocessing.image_preprocessing import cropping
import cv2 as cv


def simple_frame_generator(frame_captor):
    while True:
        frame = frame_captor.read_frame(False, None)
        frame = cv.imencode('.png', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')


def predicted_frame_generator(frame_captor, background_subtractor, cnn_architecture):
    predicted_letter = None
    while True:
        frame = frame_captor.read_frame(True, predicted_letter)
        background_subtractor.set_frame(frame)
        captured_image = background_subtractor.extract_background_difference(hand_index=frame_captor.hand_index, show_image=True)
        cropped = cropping(captured_image)
        cropped = cv.resize(cropped, (IMAGE_SIZE_X, IMAGE_SIZE_Y))

        # Normalize the image and feed it to the CNN model to get the predicted class
        next_image = np.array(np.zeros(shape=(1, IMAGE_SIZE_X, IMAGE_SIZE_Y, 3)))
        normalized_image = cv.normalize(cropped, None, alpha=0, beta=1, norm_type=cv.NORM_MINMAX, dtype=cv.CV_32F)
        next_image[0] = normalized_image
        predicted_class = cnn_architecture.predict_classes_for_images(next_image)
        predicted_letter = CLASSES[predicted_class[0]]
        frame = cv.imencode('.png', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')

        cv.waitKey(10)
