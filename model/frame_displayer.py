from base_constants.general_constants import HAND
import cv2 as cv


class FrameDisplayer:
    def __init__(self, hand_index=0):
        self.hand_index = hand_index

    def display_frame(self, frame, predicted_letter):
        # If the user wants to use his/her left hand, the rectangle representing the area of interest will
        # be shown on the upper-left corner
        if HAND[self.hand_index] == 'RIGHT':
            cv.rectangle(frame, (800, 0), (1280, 480), (0, 255, 0), 2)
        else:
            # otherwise on the upper-right corner
            cv.rectangle(frame, (0, 0), (480, 480), (0, 255, 0), 2)

        # If predicted letter is None, it means detection has not started yet
        if predicted_letter is None:
            text_first = "Please make sure that your hand and any other moving"
            text_second = "objects are outside the green rectangle."
            text_third = "Press B after you made sure."
            cv.putText(frame, text_first, (60, 60), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0,255), 2, cv.LINE_AA)
            cv.putText(frame, text_second, (60, 85), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv.LINE_AA)
            cv.putText(frame, text_third, (60, 110), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv.LINE_AA)
        else:
            cv.putText(frame, "Predicted letter: " + str(predicted_letter), (750, 650), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)

        cv.imshow('Hand Recognition Application', frame)