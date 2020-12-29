from keras import models
from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input
from werkzeug.utils import secure_filename
import numpy as np
import os

BASE_DIR = os.path.dirname(__file__)
#loading our model
model = models.load_model('model/mobilenet_1.00_224.h5')
def preprocess_image(img_file) :
    img = image.load_img(f'{img_file}',target_size = (224 , 224))
    img = image.img_to_array(img)
    img_expand = np.expand_dims(img , axis=0)
    return preprocess_input(img_expand)

def model_predict(img_file) :
    prep_img = preprocess_image(img_file)
    prediction = model.predict(prep_img).argmax(axis=1)[0]
    confidence = max(model.predict(prep_img)[0])
    return prediction , confidence

from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    # Main page
    return render_template('home.html')

@app.route('/result', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['inpFile']
      file_path = os.path.join(
            BASE_DIR, 'uploads', secure_filename(f.filename))
      f.save(file_path)
      pred ,confidence  = model_predict(file_path)
      if pred == 0 :
          result = 'Image has No Road'
      elif pred == 1 :
          result = 'Image has Road'
      return render_template('result.html',result = result , confidence = confidence)



if __name__ == '__main__':
    app.run(port=5001,debug=True)