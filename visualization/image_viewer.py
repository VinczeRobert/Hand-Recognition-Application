import matplotlib.pyplot as plt
import cv2 as cv


class ImageViewer:
    """
    Class used for displaying images with their actual and predicted classes.
    """
    def __init__(self):
        self.pred_figure = plt.figure(figsize=(20, 20))

    def plot_image(self, image, predicted_class, actual_class, row, col, index):
        """
        :param image: image to displayed
        :param predicted_class: class predicted by our model
        :param actual_class: class that the image actually belongs to
        :param row: row of the plot that this image will be displayed to
        :param col: column of the plot that this image will be displayed to
        :param index:  index of this image on the plot
        """
        self.pred_figure.add_subplot(row, col, index)
        plt.axis('off')
        plt.imshow(image)
        title = 'prediction: [{}] \n actual: [{}]'.format(predicted_class, actual_class)
        plot_title = plt.title(title)
        plt.setp(plot_title, color='r')

    @staticmethod
    def show_plot():
        plt.show()

