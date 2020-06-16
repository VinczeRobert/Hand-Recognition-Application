from base_constants.constants import HAND
import cv2 as cv


class FrameDisplayer:
    def __init__(self, hand_index=0):
        self.hand_index = hand_index

    def display_frame(self, frame, predicted_letter, predicted_text):
        # If the user wants to use his/her left hand, the rectangle representing the area of interest will
        # be shown on the upper-left corner
        if self.hand_index == HAND[0]:
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

        # Display text
        text_size = cv.getTextSize(predicted_text, cv.FONT_HERSHEY_SIMPLEX, 1,cv.LINE_AA)[0]
        line_height = text_size[1] + 5
        y0 = 520
        no_displayable_lines = int((720 - 500) / line_height)
        split_text = predicted_text.split("\n")
        no_all_lines = len(split_text)

        if no_all_lines > no_displayable_lines:
            split_text = split_text[(no_all_lines - no_displayable_lines):]

        for i, line in enumerate(split_text):
            y = y0 + i * line_height
            cv.putText(frame, line, (0, y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)
        # cv.imshow('Hand Recognition Application', frame)
        return frame
