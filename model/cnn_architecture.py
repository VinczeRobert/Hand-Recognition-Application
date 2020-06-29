from keras import models, layers, losses, regularizers, callbacks
from keras_preprocessing.image import ImageDataGenerator
import numpy as np
import copy
from model.data_reading import IMAGE_RESIZE_X, IMAGE_RESIZE_Y


class CNNArchitecture:
    """
    Class of the Convolutional Neural Network (CNN) and all methos related to building and training the model.
    This class has been built using the Singleton Design Pattern.
    """
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
        Method used to build the model what will be used for training.
        :param classes: number of classes required for the last layer
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

        # Call compile to prepare the model for training.
        # This model uses Adam Optimizer and Sparse Categorial Crossentropy loss function.
        self._model.compile(optimizer='adam',
                            loss=losses.sparse_categorical_crossentropy,
                            metrics=['accuracy'])

    def train_model(self, train_images, class_labels):
        """
        Method used to train the built model. The whole dataset will be loaded into the memory at once.
        :param train_images: images that the model will be trained on
        :param class_labels: classes that the training images belong to
        """
        save_weights_callback = self._use_callback_for_saving_model()
        early_stopping_callback = self._use_callback_for_early_stopping()
        self._model.fit(train_images, class_labels, epochs=5, batch_size=256,
                        shuffle=True, validation_split=0.2,
                        callbacks=[save_weights_callback, early_stopping_callback])

        self._model.save(self.MODEL_PATH)

    def train_model_with_real_time_augmentation(self, training_images, training_labels,
                                                validation_images, validation_labels):
        """
        Method used to train the built model. The dataset will be loaded in batches.
        This method is slower than train_model because it uses real time data augmentation.
        :param training_images: images that the model will be trained on
        :param training_labels: classes that the training images belong to
        :param validation_images: images that the model will be validated on
        :param validation_labels: classes that the validating images belong to
        """

        # Defining the same Generator for both training and validation data to be used during training.
        training_generator = ImageDataGenerator(
            rotation_range=15,
            zoom_range=0.15,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.15,
            horizontal_flip=True,
            fill_mode="nearest"
        )

        validation_generator = copy.copy(training_generator)

        save_weights_callback = self._use_callback_for_saving_model()
        self._model.fit_generator(training_generator.flow(training_images, training_labels),
                                  steps_per_epoch=len(training_images) // 32,
                                  validation_data=validation_generator.flow(
                                      validation_images, validation_labels, batch_size=32),
                                  validation_steps=0.2 * len(training_images) // 32, epochs=6,
                                  callbacks=[save_weights_callback])

    def load_model(self, path):
        """
        Loads existing weights into the model
        :param path: existing weights file
        """
        self._model.load_weights(path)

    @staticmethod
    def _use_callback_for_saving_model():
        """
        Create a Callback that saves the model's weights.
        """
        save_weights_callback = callbacks.ModelCheckpoint(filepath='data/weights/new_weights.ckpt',
                                                          save_weights_only=True, verbose=1)
        return save_weights_callback

    @staticmethod
    def _use_callback_for_early_stopping():
        """
        Create a Callback that stops the model earlier if no improvements are made.
        It is used as an attempt to block potential overfitting.
        """
        early_stopping_callback = callbacks.EarlyStopping(monitor='val_accuracy', min_delta=0.001, patience=1)
        return early_stopping_callback

    def predict_classes_for_images(self, images):
        """
        Takes an array of images as argument and for each image predicts the class with maximum probability.
        :param images: input images which predictiosn will be acquired for
        :return: array of predictions for each input image
        """
        predictions = self._model.predict(images)
        max_predictions = []

        for idx in range(len(predictions)):
            max_predictions.append(np.argmax(predictions[idx]))

        return max_predictions
