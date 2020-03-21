from keras import models, layers, losses


class CNNArchitecture():

    def __init__(self):
        self.model = models.Sequential()

    def build_model(self):
        self.model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)))
        self.model.add(layers.MaxPooling2D((2, 2)))
        self.model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        self.model.add(layers.MaxPooling2D((2, 2)))
        self.model.add(layers.Conv2D(64, (3, 3), activation='relu'))

        self.model.add(layers.Flatten())
        self.model.add(layers.Dense(64, activation='relu'))
        self.model.add(layers.Dense(10))

        print(self.model.summary())

    def train_model(self, train_images, class_labels):
        self.model.compile(optimizer='adam',
                      loss=losses.SparseCategoricalCrossentropy(from_logits=True),
                           metrics=['accuracy'])
        history = self.model.fit(train_images, class_labels, epochs=4)


