import cv2 as cv
from model.settings import HAND


class FrameDisplayer:
    def __init__(self, hand_index=0):
        self._hand_index = hand_index
        self._last_predicted_letter = None
        self._iterations_between_different_predictions = 0
        self._current_predicted_text = ''

    def display_frame(self, frame, predicted_letter):
        # If the user wants to use his/her left hand, the rectangle representing the area of interest will
        # be shown on the upper-left corner
        if self._hand_index == HAND[0]:
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
        text_size = cv.getTextSize(self._current_predicted_text, cv.FONT_HERSHEY_SIMPLEX, 1,cv.LINE_AA)[0]
        line_height = text_size[1] + 5
        y0 = 520
        no_displayable_lines = int((720 - 500) / line_height)
        split_text = self._current_predicted_text.split("\n")
        no_all_lines = len(split_text)

        if no_all_lines > no_displayable_lines:
            split_text = split_text[(no_all_lines - no_displayable_lines):]

        for i, line in enumerate(split_text):
            y = y0 + i * line_height
            cv.putText(frame, line, (0, y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)

        return cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    def get_predicted_text(self, new_predicted_letter):
        if new_predicted_letter != self._last_predicted_letter:
            self._last_predicted_letter = new_predicted_letter
        else:
            self._iterations_between_different_predictions = self._iterations_between_different_predictions + 1

        if self._iterations_between_different_predictions > 40:
            self._iterations_between_different_predictions = 0

            #TODO: This is wonderful with one small issue: there is no way for the user to know when a space or newline was actually succesfull
            if new_predicted_letter == 'Delete':
                self._current_predicted_text = self._current_predicted_text[:-1]
            elif new_predicted_letter == 'Space':
                self._current_predicted_text = self._current_predicted_text + ' '
            elif new_predicted_letter == 'NewLine':
                self._current_predicted_text = self._current_predicted_text + '\n'
            else:
                self._current_predicted_text = self._current_predicted_text + new_predicted_letter

    def set_hand_index(self, hand_index):
        self._hand_index = hand_index




