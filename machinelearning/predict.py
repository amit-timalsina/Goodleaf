import os
import json
import tensorflow as tf
import pandas as pd 
import numpy as np 
from matplotlib.image import imread
import matplotlib.pyplot as plt
from django.conf import settings
from keras.models import load_model
from keras.preprocessing import image
import numpy as np

def augment_image(img_path):
  img = imread(img_path)
  img = tf.image.resize(img, [256,256], method='nearest')
  img = np.reshape(img, (1,256,256,3))
  img = img / 255
  return img 

module_dir = os.path.dirname(__file__)

json_dir = module_dir + "/model/model.json"
model_dir = module_dir + "/model/model.h5"
csv_dir = module_dir + "/model/model.csv"

Jfile = open(json_dir)
json_read = json.load(Jfile)
Jfile.close()

model = load_model(model_dir)
df = pd.read_csv(csv_dir)

def predict(df, img):
    img = augment_image("/home/amit/projects/KU/forum" + img)
    pred = model.predict(img)
    disease = np.where(pred == pred.max())[1][0]
    output = [df.loc[disease].Disease, df.loc[disease].Symptom, df.loc[disease].Treatment, df.loc[disease].Category]
    return output
