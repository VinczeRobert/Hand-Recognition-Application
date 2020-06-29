import cv2 as cv
from model.settings import HAND


class FrameDisplayer:
    """
    Class responsible for displaying the frames with texts in the UI.
    """

    # Constants that will be used throughout this class
    USED_FONT = cv.FONT_HERSHEY_SIMPLEX
    USED_FONT_SCALE = 0.75
    USED_COLOR = (255, 0, 0)
    USED_THICKNESS = 2
    USED_LINE_TYPE = cv.LINE_AA
    CHARACTERS_PER_LINE = 60

    def __init__(self, hand_index=0):
        self._hand_index = hand_index
        self._last_predicted_letter = None
        self._iterations_between_different_predictions = 0
        self._frame_count = 0
        self._predicted_text_copy = ''

    def display_frame(self, frame, predicted_letter, current_predicted_text):
        """

        :param frame: Current frame to be displayed
        :param predicted_letter: Currently predicted letter
        :param current_predicted_text: Current text made of predicted letters
        :return: BGR frame with all needed texts and rectangle added
        """

        self._frame_count = self._frame_count + 1
        self._draw_rectangle(frame)

        # If predicted letter is None, it means predictions have not been started yet
        if predicted_letter is None:
            text_first = "Please make sure that your hand"
            text_second = "and any other moving objects are"
            text_third = "outside the green rectangle."
            text_forth = "Press B after you have made sure."
            cv.putText(frame, text_first, (30, 60), self.USED_FONT, self.USED_FONT_SCALE, self.USED_COLOR,
                       self.USED_THICKNESS, self.USED_LINE_TYPE)
            cv.putText(frame, text_second, (30, 85), self.USED_FONT, self.USED_FONT_SCALE, self.USED_COLOR,
                       self.USED_THICKNESS, self.USED_LINE_TYPE)
            cv.putText(frame, text_third, (30, 110), self.USED_FONT, self.USED_FONT_SCALE, self.USED_COLOR,
                       self.USED_THICKNESS, self.USED_LINE_TYPE)
            cv.putText(frame, text_forth, (30, 160), self.USED_FONT, self.USED_FONT_SCALE, self.USED_COLOR,
                       self.USED_THICKNESS, self.USED_LINE_TYPE)
        # If predicted letter is -1, if means detection has started but there is no detected object in the area
        elif predicted_letter == -1:
            cv.putText(frame, "No hand detected.", (100, 650), self.USED_FONT, self.USED_FONT_SCALE, self.USED_COLOR,
                       self.USED_THICKNESS, self.USED_LINE_TYPE)
        # Any other value means a predicted letter, which must be displayed
        else:
            cv.putText(frame, "Predicted letter: " + str(predicted_letter), (100, 650), self.USED_FONT,
                       self.USED_FONT_SCALE, self.USED_COLOR, self.USED_THICKNESS, self.USED_LINE_TYPE)

        split_text, line_height = self.format_predicted_text(current_predicted_text)
        y0 = 20

        # Toggle the cursor
        if self._frame_count % 2 == 0:
            split_text[-1] = split_text[-1] + '|'

        # Adds predicted text to the frame line by line
        for i, line in enumerate(split_text):
            y = y0 + i * line_height
            cv.putText(frame, line, (500, y), self.USED_FONT, self.USED_FONT_SCALE, self.USED_COLOR,
                       self.USED_THICKNESS, self.USED_LINE_TYPE)

        # The UI expects BGR images so a conversion is needed
        return cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    def display_frame_in_building_mode(self, frame, frame_index):
        """
        This method is only used when adding frames of a new gesture
        :param frame: new frame to be saved
        :param frame_index: index of the new frame
        :return: BGR representation of the new frame
        """
        self._draw_rectangle(frame)
        cv.putText(frame, "Currently saving image number {}".format(frame_index), (100, 650),
                   self.USED_FONT, 1, self.USED_COLOR, 2, self.USED_LINE_TYPE)
        return cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    def _draw_rectangle(self, frame):
        """
        Draws rectangle in the upper left or right corner based on which hand is being used
        """
        if self._hand_index == HAND[0]:
            cv.rectangle(frame, (800, 0), (1280, 480), (0, 255, 0), 2)
        else:
            # otherwise on the upper-right corner
            cv.rectangle(frame, (0, 0), (480, 480), (0, 255, 0), 2)

    def get_predicted_text(self, new_predicted_letter, predicted_text):
        """
        This method contains the logic of adding the last predicted letter to the text
        """
        if new_predicted_letter != self._last_predicted_letter:
            self._last_predicted_letter = new_predicted_letter
        else:
            self._iterations_between_different_predictions = self._iterations_between_different_predictions + 1

        # A prediction has to be constant for 30 consecutive frames in order to be added
        if self._iterations_between_different_predictions > 30:
            self._iterations_between_different_predictions = 0

            # Handling special characters
            if new_predicted_letter == 'Delete':
                predicted_text = predicted_text[:-1]
                self._predicted_text_copy = self._predicted_text_copy[:-1]
            elif new_predicted_letter == 'Space':
                predicted_text = predicted_text + ' '
                self._predicted_text_copy = self._predicted_text_copy[:-1]
            elif new_predicted_letter == 'NewLine':
                predicted_text = predicted_text + '\n'
                self._predicted_text_copy = self._predicted_text_copy + '\n'
            else:
                predicted_text = predicted_text + new_predicted_letter
                self._predicted_text_copy = self._predicted_text_copy + new_predicted_letter

        return predicted_text

    def format_predicted_text(self, predicted_text):
        """
        Divide the text into line so it fits in the UI
        """
        text_size = cv.getTextSize(predicted_text, self.USED_FONT, 1, self.USED_LINE_TYPE)[0]
        no_displayable_lines = int(720 / text_size[1])
        split_text = predicted_text.split("\n")
        no_all_lines = len(split_text)

        # If the text is too long, only the most recent number of lines will be displayed
        if no_all_lines > no_displayable_lines:
            split_text = split_text[(no_all_lines - no_displayable_lines):]

        return split_text, text_size[1]

    def set_hand_index(self, hand_index):
        self._hand_index = hand_index

    def load_text(self, text_file_path):
        if text_file_path != '':
            text_file = open(text_file_path, 'r')
            predicted_text = text_file.read()
            self._predicted_text_copy = predicted_text

            # Add new lines to loaded text so it fits in UI
            predicted_text = '\n'.join(predicted_text[i:i + self.CHARACTERS_PER_LINE]
                                       for i in range(0, len(predicted_text), self.CHARACTERS_PER_LINE))
            text_file.close()
            return predicted_text
        return ''

    def save_text(self, text_file_path):
        if text_file_path != '':
            text_file = open(text_file_path, 'w')
            text_file.write(self._predicted_text_copy)
            text_file.close()
