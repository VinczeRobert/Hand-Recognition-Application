from keras import models, layers, losses, regularizers, callbacks
from sklearn import metrics
from base_constants.general_constants import NUMBER_OF_CLASSES, WEIGHTS_PATH, IMAGE_DIMENSION_X, IMAGE_DIMENSION_Y
import numpy as np


class CNNArchitecture:
    # Declaring model hyper (non-trainable) parameters for training
    INPUT_SHAPE = (IMAGE_DIMENSION_X, IMAGE_DIMENSION_Y, 3)
    NUMBER_OF_FILTERS_1 = 32
    NUMBER_OF_FILTERS_2 = 64
    NUMBER_OF_FILTERS_3 = 128
    NUMBER_OF_FILTERS_4 = 256
    KERNEL_SIZE = 3
    STRIDES = (1, 1)
    POOL_SIZE = 3
    DROPOUT_RATE = 0.5
    DENSE_UNITS = 512

    # String constants
    PADDING = "same"
    ACTIVATION_FUNCTION = 'relu'
    SECOND_ACTIVATION_FUNCTION = 'softmax'

    # Used regularizer to avoid over-fitting
    KERNEL_REGULARIZER = regularizers.l2(0.001)

    # Hyper parameters for training
    EPOCHS = 5
    BATCH_SIZE = 64
    VALIDATION_SPLIT = 0.1

    def __init__(self):
        self.model = models.Sequential()
        self.history = None

    def build_model(self):
        """
        Method used to build the model what will be used for training.
        Override this method with your own implementation and subclass for trying out a different model.
        """
        self.model.add(layers.Conv2D(filters=self.NUMBER_OF_FILTERS_2, kernel_size=self.KERNEL_SIZE,
                                     strides=self.STRIDES, padding=self.PADDING, activation=self.ACTIVATION_FUNCTION,
                                     input_shape=self.INPUT_SHAPE))
        self.model.add(layers.Conv2D(filters=self.NUMBER_OF_FILTERS_2, kernel_size=self.KERNEL_SIZE,
                                     strides=self.STRIDES, padding=self.PADDING, activation=self.ACTIVATION_FUNCTION))
        self.model.add(layers.MaxPooling2D(pool_size=self.POOL_SIZE))

        self.model.add(layers.Conv2D(filters=self.NUMBER_OF_FILTERS_2, kernel_size=self.KERNEL_SIZE,
                                     strides=self.STRIDES, padding=self.PADDING, activation=self.ACTIVATION_FUNCTION))
        self.model.add(layers.Conv2D(filters=self.NUMBER_OF_FILTERS_3, kernel_size=self.KERNEL_SIZE,
                                     strides=self.STRIDES, padding=self.PADDING, activation=self.ACTIVATION_FUNCTION))
        self.model.add(layers.MaxPooling2D(pool_size=self.POOL_SIZE))

        self.model.add(layers.Conv2D(filters=self.NUMBER_OF_FILTERS_3, kernel_size=self.KERNEL_SIZE,
                                     strides=self.STRIDES, padding=self.PADDING, activation=self.ACTIVATION_FUNCTION))
        self.model.add(layers.Conv2D(filters=self.NUMBER_OF_FILTERS_4, kernel_size=self.KERNEL_SIZE,
                                     strides=self.STRIDES, padding=self.PADDING, activation=self.ACTIVATION_FUNCTION))
        self.model.add(layers.MaxPooling2D(pool_size=self.POOL_SIZE))

        self.model.add(layers.BatchNormalization())
        self.model.add(layers.Flatten())
        self.model.add(layers.Dropout(rate=self.DROPOUT_RATE))

        self.model.add(
            layers.Dense(self.DENSE_UNITS, activation=self.ACTIVATION_FUNCTION,
                         kernel_regularizer=self.KERNEL_REGULARIZER))
        self.model.add(layers.Dense(NUMBER_OF_CLASSES, activation=self.SECOND_ACTIVATION_FUNCTION))

        print(self.model.summary())

        self.model.compile(optimizer='adam',
                           loss=losses.sparse_categorical_crossentropy,
                           metrics=['accuracy'])

    def train_model(self, train_images, class_labels):
        """
        Method used to train the built model.
        :param train_images: images that the training will be done on
        :param class_labels: classes that the images belong to
        """
        save_weights_callback = self.use_callback_for_saving_model()
        early_stopping_callback = self.use_callback_for_early_stopping()
        self.history = self.model.fit(train_images, class_labels, epochs=self.EPOCHS, batch_size=self.BATCH_SIZE,
                                      validation_split=self.VALIDATION_SPLIT, callbacks=[save_weights_callback,
                                                                                         early_stopping_callback])

        print("Model has been created.")
        self.model.summary()

    def evaluate_model(self, test_images, class_labels):
        """
        Method used to test the built model.
        :param test_images: images that the model will be evaluated on
        :param class_labels: classes that the images belong to
        """
        evaluate_metrics = self.model.evaluate(test_images, class_labels)
        print("\nEvaluation Accuracy = ", "{:.2f}%".format(evaluate_metrics[1] * 100), "\nEvaluation loss = ",
              "{:.6f}".format(evaluate_metrics[0]))

    @staticmethod
    def use_callback_for_saving_model():
        """
        Create a Callback that saves the model's weights.
        """
        save_weights_callback = callbacks.ModelCheckpoint(filepath=WEIGHTS_PATH, save_weights_only=True, verbose=1)
        return save_weights_callback

    @staticmethod
    def use_callback_for_early_stopping():
        """
        Create a Callback that stops the model earlier if no improvements are made, thus avoid overfitting.
        """
        early_stopping_callback = callbacks.EarlyStopping(monitor='val_accuracy', min_delta=0.001, patience=1)
        return early_stopping_callback

    def predict_classes_for_images(self, images):
        """
        Takes an array of images as argument and for each image predicts the class with maximum probability.
        :param images: input images which we need prediction for
        :return: array of predictions for each input image
        """
        predictions = self.model.predict(images)
        max_predictions = []

        for idx in range(len(predictions)):
            max_predictions.append(np.argmax(predictions[idx]))

        return max_predictions

    @staticmethod
    def compute_confusion_matrix(true_labels, predicted_labels):
        confusion_matrix = metrics.confusion_matrix(true_labels, predicted_labels)
        return confusion_matrix
