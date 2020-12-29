import keras
from keras.layers import Dense , Activation
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
import os
import numpy as np

def preprocess_image(img_file) :
    img = image.load_img(f'{img_file}',target_size = (224 , 224))
    img = image.img_to_array(img)
    img_expand = np.expand_dims(img , axis=0)
    return keras.applications.mobilenet.preprocess_input(img_expand)

os.chdir('D:/ProjectsFolder/Road Detection Using MobileNet/Train_model')

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

# loading the trained model
model = keras.models.load_model('mobileNetModel.h5')

#predicting the model
print(test_datagen.class_indices)
print(test_datagen.labels)
y_pred = model.predict(x=test_datagen)
y_pred.argmax(axis=1)

from sklearn.metrics import confusion_matrix , accuracy_score
cm = confusion_matrix(test_datagen.classes , y_pred.argmax(axis=1))
cm

print(f'Accuracy : {accuracy_score(test_datagen.classes , y_pred.argmax(axis=1))}')

filename = input('Enter filename (with extension) : ')  + '.jpg'

try :
    
    labels = ['No Road' , 'Road']
    prep_img = preprocess_image(filename)
    print('Result : {}'.format(labels[model.predict(prep_img).argmax(axis=1)[0]]))
except :
    print(f"File '{filename}' doesn't exist.")