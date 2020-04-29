import matplotlib.pyplot as plt


class AccuracyLossViewer:
    """
    Class used to visualize the two most important results of the training process: accuracy and loss.
    """
    def __init__(self, history):
        self.history = history

    def plot_accuracy(self):
        plt.plot(self.history.history['accuracy'])
        plt.plot(self.history.history['val_accuracy'])
        plt.legend(['train', 'validation'], loc='lower right')
        plt.title('Train VS. Validation Accuracy')
        plt.xlabel('epoch')
        plt.ylabel('accuracy')
        plt.show()

    def plot_loss(self):
        plt.plot(self.history.history['loss'])
        plt.plot(self.history.history['val_loss'])
        plt.legend(['train', 'validation'], loc='upper right')
        plt.title('Train VS. Validation Loss')
        plt.xlabel('epoch')
        plt.ylabel('loss')
        plt.show()
