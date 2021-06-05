#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 18:31:44 2021

@author: mainak
"""

#Import necessary libraries
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
 
import numpy as np
import os
import tensorflow as tf
from tf.keras.preprocessing.image import load_img
from tf.keras.preprocessing.image import img_to_array
from tf.keras.models import load_model
 
#load model
model=load_model('/home/mainak/Documents/Jupyter/AppleLeaf_Disease/model/inception_v31 .h5')
 
print('@@ Model loaded')
 
 
def apple_disease(apple_plant):
  test_image=load_img(apple_plant,target_size=(224,224)) # load image 
  print("@@ Got Image for prediction")
   
  test_image=img_to_array(test_image)/255 # convert image to np array and normalize
  test_image=np.expand_dims(test_image, axis = 0) # change dimention 3D to 4D
   
  result=model.predict(test_image).round(3) # predict diseased plant or not
  print('@@ Raw result = ', result)
   
  pred=np.argmax(result) # get the index of max value
 
  if pred==0:
    return 'Complex' 
  elif pred==1:
      return 'frog_eye_leaf_spot'
  elif pred==2:
      return 'frog_eye_leaf_spot complex'
  elif pred==3:
      return 'healthy'
  elif pred==4:
      return 'powdery mildew'
  elif pred==5:
      return 'powdery mildew complex'
  elif pred==6:
      return 'rust'
  elif pred==7:
      return 'rust complex'
  elif pred==8:
      return 'rust frog eye leaf spot'
  elif pred==9:
      return 'scab'
  elif pred==10:
      return 'scrab frog eye leaf spot'
  else:
      return 'scrab frog eye leaf spot complex'
  
 
 
#**********************************************************
     
 
# Create flask instance
app = Flask(__name__)
 
# render index.html page
@app.route("/", methods=['GET', 'POST'])
def home():
        return render_template('index.html')
     
  
# get input image from client then predict class and render respective .html page for solution
@app.route("/predict", methods = ['GET','POST'])
def predict():
     if request.method == 'POST':
        file = request.files['image'] # fet input
        filename = file.filename        
        print("@@ Input posted = ",filename)
         
        file_path = os.path.join('/home/mainak/Documents/Jupyter/AppleLeaf_Disease/static/uploads',secure_filename(filename))
        file.save(file_path)
 
        print("@@ Predicting class......")
        pred=apple_disease(apple_plant=file_path)
        result=pred      
        return result
    
     
# For local system &amp; cloud
if __name__ == "__main__":
    app.run(threaded=False,host="0.0.0.0",port="5001",debug=True) 
