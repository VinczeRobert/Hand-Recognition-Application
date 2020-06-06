from base_constants.general_constants import HAND
import cv2 as cv


class FrameDisplayer:
    def __init__(self, hand_index=0):
        self.hand_index = hand_index

    def display_frame(self, frame, predicted_letter, predicted_text):
        # If the user wants to use his/her left hand, the rectangle representing the area of interest will
        # be shown on the upper-left corner
        if HAND[self.hand_index] == 'RIGHT':
            cv.rectangle(frame, (800, 0), (1280, 480), (0, 255, 0), 2)
        else:
            # otherwise on the upper-right corner
            cv.rectangle(frame, (0, 0), (480, 480), (0, 255, 0), 2)

        # If predicted letter is None, it means predictions have not been started yet
        if predicted_letter is None:
            text_first = "Please make sure that your hand and any other moving"
            text_second = "objects are outside the green rectangle."
            text_third = "Press B after you made sure."
            cv.putText(frame, text_first, (60, 60), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0,255), 2, cv.LINE_AA)
            cv.putText(frame, text_second, (60, 85), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv.LINE_AA)
            cv.putText(frame, text_third, (60, 110), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv.LINE_AA)
        # If predicted letter is -1, if means detection has started but there is no detected object in the area
        elif predicted_letter == -1:
            cv.putText(frame, "No hand detected.", (750, 650), cv.FONT_HERSHEY_SIMPLEX,
                       1, (0, 0, 255), 2, cv.LINE_AA)
        # If predicted letter is any other integer, it means we are in dataset building mode
        elif isinstance(predicted_letter, int):
            cv.putText(frame, "Currently saving image number {}".format(predicted_letter), (650, 650),
                       cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)
        # Any other value means a predicted letter, which must be displayed
        else:
            cv.putText(frame, "Predicted letter: " + str(predicted_letter), (750, 650), cv.FONT_HERSHEY_SIMPLEX,
                       1, (0, 0, 255), 2, cv.LINE_AA)

        cv.putText(frame, predicted_text, (0, 500), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)
        cv.imshow('Hand Recognition Application', frame)
