import keras
from keras.layers import Dense , Activation
from keras.optimizers import Adam
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential , Model
from keras.applications import imagenet_utils
import os
import numpy as np

# making directories 
os.chdir(r'D:\ProjectsFolder\Road Detection Using MobileNet\Train_model')
train_dir = 'data/training_data/'
test_dir = 'data/testing_data/'

# image data generator
train_gen = ImageDataGenerator(
    preprocessing_function=keras.applications.mobilenet.preprocess_input,
)

test_gen = ImageDataGenerator(
    preprocessing_function=keras.applications.mobilenet.preprocess_input,
)

train_datagen = train_gen.flow_from_directory(
    directory=train_dir,
    target_size=(224,224),
    batch_size=32
)

test_datagen = train_gen.flow_from_directory(
    directory=test_dir,
    target_size=(224,224),
    batch_size=32
)

# create a mobilenet model
mobilenet_model = keras.applications.mobilenet.MobileNet()
mobilenet_model.summary()

x = mobilenet_model.layers[-6].output
output = Dense(units=2,activation='softmax')(x)
model = Model(inputs=mobilenet_model.input , outputs=output)
for layer in model.layers[:-23] :
    layer.trainable = False

#compiling the model
model.compile(optimizer=Adam(lr=0.0001) , loss='binary_crossentropy' , metrics = ['accuracy'])

# training the model
model.fit(x=train_datagen , validation_data=test_datagen , epochs=20 , verbose=2)

try :
    model.save('mobileNetModel1.h5')
    print('Model Saved')
except :
    print('Model Not Saved')