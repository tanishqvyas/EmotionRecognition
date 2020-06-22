from __future__ import print_function
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, BatchNormalization
from keras.layers import Conv2D, MaxPooling2D
import tensorflow as tf
from tensorflow.keras import regularizers
import matplotlib.pyplot as plt
import numpy

import os


num_classes = 5  # we have 5 kinds of emotions
img_rows, img_cols = 48, 48
batch_size = 32



# Dataset Path
train_data_dir = os.path.join("data","train")
validation_data_dir = os.path.join("data","validation")


# gen of images from one image
train_datagen = ImageDataGenerator(

					rescale = 1./255,
					rotation_range = 30,
					shear_range = 0.3,
					zoom_range = 0.3,
					width_shift_range = 0.4,
					height_shift_range = 0.4,
					horizontal_flip = True,
					fill_mode = 'nearest'
								)

# gen of validation images by rescaling
validation_datagen = ImageDataGenerator(rescale = 1./255)

# 
train_generator = train_datagen.flow_from_directory(

						train_data_dir,
						color_mode = 'grayscale',
						target_size = (img_rows, img_cols),
						batch_size = batch_size,
						class_mode = 'categorical',
						shuffle = True
									)

validation_generator = validation_datagen.flow_from_directory(

							validation_data_dir,
							color_mode = 'grayscale',
							target_size = (img_rows, img_cols),
							batch_size = batch_size,
							class_mode = 'categorical',
							shuffle = True
									)

# Now we define our CNN

model = Sequential()

# Block 1 of our CNN

model.add(Conv2D(32,(3,3), padding = 'same', kernel_initializer='he_normal', input_shape=(img_rows,img_cols,1) ))

# model.add(Activation('elu'))
model.add(Activation('relu'))

model.add(BatchNormalization())
model.add(Conv2D(32,(3,3), padding = 'same', kernel_initializer='he_normal', input_shape=(img_rows,img_cols,1) ))

model.add(Activation('elu'))
# model.add(Activation('relu'))

model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

# Block 2 of our CNN
model.add(Conv2D(64,(3,3), padding = 'same', kernel_initializer='he_normal' ))

model.add(Activation('elu'))
# model.add(Activation('relu'))

model.add(BatchNormalization())
model.add(Conv2D(64,(3,3), padding = 'same', kernel_initializer='he_normal' ))
model.add(Activation('elu'))
# model.add(Activation('relu'))

model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

# Block 3 of our CNN
model.add(Conv2D(128,(3,3), padding = 'same', kernel_initializer='he_normal' ))
model.add(Activation('elu'))
# model.add(Activation('relu'))

model.add(BatchNormalization())
model.add(Conv2D(128,(3,3), padding = 'same', kernel_initializer='he_normal' ))
model.add(Activation('elu'))
# model.add(Activation('relu'))

model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

# Block 4 of our CNN
model.add(Conv2D(256,(3,3), padding = 'same', kernel_initializer='he_normal' ))

model.add(Activation('elu'))
# model.add(Activation('relu'))

model.add(BatchNormalization())
model.add(Conv2D(256,(3,3), padding = 'same', kernel_initializer='he_normal' ))

model.add(Activation('elu'))
# model.add(Activation('relu'))

model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

# Block 5 >>> CNN is completed now flattening will start
model.add(Flatten())
model.add(Dense(64, kernel_initializer='he_normal'))
model.add(Activation('elu'))
# model.add(Activation('relu'))

model.add(BatchNormalization())
model.add(Dropout(0.3))

# Block 6
model.add(Dense(64, kernel_initializer='he_normal'))
model.add(Activation('elu'))
# model.add(Activation('relu'))

model.add(BatchNormalization())
model.add(Dropout(0.4))

# Block 7
model.add(Dense(num_classes,kernel_initializer='he_normal'))
model.add(Activation('softmax'))



print(model.summary())


# Abhi training krenge
from keras.optimizers import RMSprop, SGD, Adam
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau


name_of_model = os.path.join("model","mach_three.h5")


checkpoint = ModelCheckpoint(
					name_of_model,
					# monitor = 'val_loss',
					monitor = 'val_accuracy',
					mode = 'max',
					save_best_only = True,
					verbose = 1
						)

earlystop = EarlyStopping(

				monitor = 'val_accuracy',
				min_delta = 0,
				patience = 7,
				verbose = 1,
				restore_best_weights = True
						)

reduce_lr = ReduceLROnPlateau(
				monitor = 'val_accuracy',
				factor = 0.2,
				patience = 2,
				verbose = 1,
				min_delta = 0.0001
						)

callbacks = [earlystop, checkpoint, reduce_lr ]
# callbacks = [checkpoint, reduce_lr]




model.compile(loss='categorical_crossentropy',
				optimizer = Adam(lr=0.00169),
				metrics = ['accuracy']
					)

nb_train_samples = 18812
nb_validation_samples = 6791
epochs = 32


history = model.fit_generator(
			train_generator,
			steps_per_epoch = nb_train_samples//batch_size,
			epochs = epochs,
			callbacks = callbacks,
			validation_data = validation_generator,
			validation_steps = nb_validation_samples//batch_size
				)


# list all data in history
print(history.history.keys())

# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
# plt.plot(history.history['lr'])

plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')

plt.legend(['train acc', 'val acc', 'train loss', 'val loss'], loc='upper right')
plt.show()


