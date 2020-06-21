from keras import models, layers, losses, regularizers, callbacks
import numpy as np
from sklearn import metrics


class CNNArchitecture:

    MODEL_PATH = 'data/cnn/hra_model'
    _instance = None

    # Declaring hra_model hyper (non-trainable) parameters for training
    INPUT_SHAPE = (64, 64, 3)
    DROPOUT_RATE = 0.5
    DENSE_UNITS = 512

    # String constants
    ACTIVATION_FUNCTION = 'relu'
    SECOND_ACTIVATION_FUNCTION = 'softmax'

    # Used regularizer to avoid over-fitting
    KERNEL_REGULARIZER = regularizers.l2(0.001)

    # Hyper parameters for training
    EPOCHS = 5
    BATCH_SIZE = 256
    VALIDATION_SPLIT = 0.2

    def __init__(self):
        self.model = models.Sequential()
        self.history = None

    @staticmethod
    def get_instance():
        if CNNArchitecture._instance is None:
            CNNArchitecture._instance = CNNArchitecture()
        return CNNArchitecture._instance

    def build_model(self, classes=29):
        """
        Method used to build the hra_model what will be used for training.
        """
        self.model.add(layers.Conv2D(filters=32, kernel_size=2,
                                     strides=(1, 1), padding="same", activation=self.ACTIVATION_FUNCTION,
                                     input_shape=self.INPUT_SHAPE))
        self.model.add(layers.Conv2D(filters=64, kernel_size=3,
                                     strides=(1, 1), padding="same", activation=self.ACTIVATION_FUNCTION))
        self.model.add(layers.MaxPooling2D(pool_size=2))

        self.model.add(layers.Conv2D(filters=64, kernel_size=3,
                                     strides=(1, 1), padding="same", activation=self.ACTIVATION_FUNCTION,
                                     input_shape=self.INPUT_SHAPE))
        self.model.add(layers.Conv2D(filters=64, kernel_size=3,
                                     strides=(1, 1), padding="same", activation=self.ACTIVATION_FUNCTION))
        self.model.add(layers.MaxPooling2D(pool_size=3))

        self.model.add(layers.Conv2D(filters=128, kernel_size=5,
                                     strides=(1, 1), padding="same", activation=self.ACTIVATION_FUNCTION))
        self.model.add(layers.Conv2D(filters=256, kernel_size=3,
                                     strides=(1, 1), padding="same", activation=self.ACTIVATION_FUNCTION))
        self.model.add(layers.MaxPooling2D(pool_size=5))

        self.model.add(layers.BatchNormalization())
        self.model.add(layers.Flatten())
        self.model.add(layers.Dropout(rate=self.DROPOUT_RATE))

        self.model.add(
            layers.Dense(self.DENSE_UNITS, activation=self.ACTIVATION_FUNCTION, kernel_regularizer=self.KERNEL_REGULARIZER))
        self.model.add(layers.Dense(classes, activation=self.SECOND_ACTIVATION_FUNCTION))

        print(self.model.summary())

        self.model.compile(optimizer='adam',
                           loss=losses.sparse_categorical_crossentropy,
                           metrics=['accuracy'])

    def train_model(self, train_images, class_labels):
        """
        Method used to train the built hra_model.
        :param train_images: images that the hra_model will be trained on
        :param class_labels: classes that the training images belong to
        """
        save_weights_callback = self.use_callback_for_saving_model()
        early_stopping_callback = self.use_callback_for_early_stopping()
        self.history = self.model.fit(train_images, class_labels, epochs=self.EPOCHS, batch_size=self.BATCH_SIZE, shuffle=True,
                                      validation_split=self.VALIDATION_SPLIT, callbacks=[save_weights_callback, early_stopping_callback])

        self.model.save(self.MODEL_PATH)

    def evaluate_model(self, test_images, class_labels):
        """
        Method used to test the built hra_model.
        :param test_images: images that the hra_model will be evaluated on
        :param class_labels: classes that the testing images belong to
        """
        evaluate_metrics = self.model.evaluate(test_images, class_labels)
        print("\nEvaluation Accuracy = ", "{:.2f}%".format(evaluate_metrics[1] * 100), "\nEvaluation loss = ",
              "{:.6f}".format(evaluate_metrics[0]))

    def load_model(self, path):
        self.model.load_weights(path)

    @staticmethod
    def use_callback_for_saving_model():
        """
        Create a Callback that saves the hra_model's weights.
        """
        save_weights_callback = callbacks.ModelCheckpoint(filepath='data/weights/new_weights.ckpt', save_weights_only=True, verbose=1)
        return save_weights_callback

    @staticmethod
    def use_callback_for_early_stopping():
      """
      Create a Callback that stops the hra_model earlier if no improvements are made.
      We use this as an attempt to block potential overfitting.
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
      """
      Computes the confusion matrix of the hra_model based on testing data.
      :param true_labels: classes that the testing images actually belong to
      :param predicted_labels: classes that where predicted for each testing image
      """
      confusion_matrix = metrics.confusion_matrix(true_labels, predicted_labels)
      return confusion_matrix