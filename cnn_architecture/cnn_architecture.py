from keras import models, layers, losses, regularizers

from hyper_parameters.hyper_parameters import NUMBER_OF_FILTERS_2, NUMBER_OF_FILTERS_3, \
    NUMBER_OF_FILTERS_4, KERNEL_SIZE, STRIDES, ACTIVATION_FUNCTION, POOL_SIZE, INPUT_SHAPE, DROPOUT_RATE, \
    DENSE_UNITS, NUMBER_OF_CLASSES, SECOND_ACTIVATION_FUNCTION


class CNNArchitecture:

    def __init__(self):
        self.model = models.Sequential()

    def build_model(self):
        self.model.add(layers.Conv2D(filters=NUMBER_OF_FILTERS_2, kernel_size=KERNEL_SIZE,
                                     strides=STRIDES, padding="same", activation=ACTIVATION_FUNCTION,
                                     input_shape=INPUT_SHAPE))
        self.model.add(layers.Conv2D(filters=NUMBER_OF_FILTERS_2, kernel_size=KERNEL_SIZE,
                                     strides=STRIDES, padding="same", activation=ACTIVATION_FUNCTION))
        self.model.add(layers.MaxPooling2D(pool_size=POOL_SIZE))

        self.model.add(layers.Conv2D(filters=NUMBER_OF_FILTERS_2, kernel_size=KERNEL_SIZE,
                                     strides=STRIDES, padding="same", activation=ACTIVATION_FUNCTION))
        self.model.add(layers.Conv2D(filters=NUMBER_OF_FILTERS_3, kernel_size=KERNEL_SIZE,
                                     strides=STRIDES, padding="same", activation=ACTIVATION_FUNCTION))
        self.model.add(layers.MaxPooling2D(pool_size=POOL_SIZE))

        self.model.add(layers.Conv2D(filters=NUMBER_OF_FILTERS_3, kernel_size=KERNEL_SIZE,
                                     strides=STRIDES, padding="same", activation=ACTIVATION_FUNCTION))
        self.model.add(layers.Conv2D(filters=NUMBER_OF_FILTERS_4, kernel_size=KERNEL_SIZE,
                                     strides=STRIDES, padding="same", activation=ACTIVATION_FUNCTION))
        self.model.add(layers.MaxPooling2D(pool_size=POOL_SIZE))

        self.model.add(layers.BatchNormalization())
        self.model.add(layers.Flatten())
        self.model.add(layers.Dropout(rate=DROPOUT_RATE))

        self.model.add(layers.Dense(DENSE_UNITS, activation=ACTIVATION_FUNCTION, kernel_regularizer=regularizers.l2(0.001)))
        self.model.add(layers.Dense(NUMBER_OF_CLASSES, activation=SECOND_ACTIVATION_FUNCTION))

        print(self.model.summary())

    def train_model(self, train_images, class_labels):

        self.model.compile(optimizer='adam',
                      loss=losses.sparse_categorical_crossentropy,
                           metrics=['accuracy'])
        history = self.model.fit(train_images, class_labels, epochs=3, batch_size=64, validation_split=0.1)

    def evaluate_model(self, test_images, class_labels):
        evaluate_metrics = self.model.evaluate(test_images, class_labels)
        print("\nEvaluation Accuracy = ", "{:.2f}%".format(evaluate_metrics[1] * 100), "\nEvaluation loss = ",
              "{:.6f}".format(evaluate_metrics[0]))


