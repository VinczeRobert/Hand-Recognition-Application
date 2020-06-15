import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from base_constants.constants import CLASSES, NUMBER_OF_CLASSES


class ConfusionMatrixViewer:
    """
    Class used to visualize the confusion matrix applied on testing data in a
    heat-map friendly style using seaborn.
    """
    def __init__(self, confusion_matrix):
        self.confusion_matrix = confusion_matrix

    def plot_confusion_matrix(self):
        df = pd.DataFrame(self.confusion_matrix, index=[i for i in CLASSES],
                          columns=[i for i in CLASSES])
        plt.figure(figsize=(NUMBER_OF_CLASSES, NUMBER_OF_CLASSES))
        sn.heatmap(df, annot=True)
