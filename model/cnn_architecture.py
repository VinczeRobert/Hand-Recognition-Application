from keras import models, layers, losses, regularizers, callbacks
import numpy as np
from model.data_reading import IMAGE_RESIZE_X, IMAGE_RESIZE_Y


class CNNArchitecture:
    MODEL_PATH = 'data/cnn/hra_model'
    _instance = None
    ACTIVATION_FUNCTION = 'relu'

    def __init__(self):
        self._model = models.Sequential()

    @staticmethod
    def get_instance():
        if CNNArchitecture._instance is None:
            CNNArchitecture._instance = CNNArchitecture()
        return CNNArchitecture._instance

    def build_model(self, classes=29):
        """
        Method used to build the hra_model what will be used for training.
        """
        self._model.add(layers.Conv2D(filters=32, kernel_size=2,
                                      strides=(1, 1), padding="same", activation=self.ACTIVATION_FUNCTION,
                                      input_shape=(IMAGE_RESIZE_X, IMAGE_RESIZE_Y, 3)))
        self._model.add(layers.Conv2D(filters=64, kernel_size=3,
                                      strides=(1, 1), padding="same", activation=self.ACTIVATION_FUNCTION))
        self._model.add(layers.MaxPooling2D(pool_size=2))

        self._model.add(layers.Conv2D(filters=64, kernel_size=3,
                                      strides=(1, 1), padding="same", activation=self.ACTIVATION_FUNCTION))
        self._model.add(layers.Conv2D(filters=64, kernel_size=3,
                                      strides=(1, 1), padding="same", activation=self.ACTIVATION_FUNCTION))
        self._model.add(layers.MaxPooling2D(pool_size=3))

        self._model.add(layers.Conv2D(filters=128, kernel_size=5,
                                      strides=(1, 1), padding="same", activation=self.ACTIVATION_FUNCTION))
        self._model.add(layers.Conv2D(filters=256, kernel_size=3,
                                      strides=(1, 1), padding="same", activation=self.ACTIVATION_FUNCTION))
        self._model.add(layers.MaxPooling2D(pool_size=5))

        self._model.add(layers.BatchNormalization())
        self._model.add(layers.Flatten())
        self._model.add(layers.Dropout(rate=0.5))

        self._model.add(
            layers.Dense(512, activation=self.ACTIVATION_FUNCTION,
                         kernel_regularizer=regularizers.l2(0.001)))
        self._model.add(layers.Dense(classes, activation='softmax'))

        print(self._model.summary())

        self._model.compile(optimizer='adam',
                            loss=losses.sparse_categorical_crossentropy,
                            metrics=['accuracy'])

    def train_model(self, train_images, class_labels):
        """
        Method used to train the built hra_model.
        :param train_images: images that the hra_model will be trained on
        :param class_labels: classes that the training images belong to
        """
        save_weights_callback = self._use_callback_for_saving_model()
        early_stopping_callback = self._use_callback_for_early_stopping()
        self._model.fit(train_images, class_labels, epochs=5, batch_size=256,
                        shuffle=True, validation_split=0.2,
                        callbacks=[save_weights_callback, early_stopping_callback])

        self._model.save(self.MODEL_PATH)

    def load_model(self, path):
        self._model.load_weights(path)

    @staticmethod
    def _use_callback_for_saving_model():
        """
        Create a Callback that saves the hra_model's weights.
        """
        save_weights_callback = callbacks.ModelCheckpoint(filepath='data/weights/new_weights.ckpt',
                                                          save_weights_only=True, verbose=1)
        return save_weights_callback

    @staticmethod
    def _use_callback_for_early_stopping():
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
        predictions = self._model.predict(images)
        max_predictions = []

        for idx in range(len(predictions)):
            max_predictions.append(np.argmax(predictions[idx]))

        return max_predictions

    def compute_confidence_scores_for_images(self, images):
        return self._model.predict(images)
