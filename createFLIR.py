#this script should be inside FLIR_ADAS_1_3 directory where there is train, val
#first run: pip install opencv-python
from pathlib import Path
from tqdm import tqdm
import numpy as np
import json
import urllib
import PIL.Image as Image
import cv2
import torch
import torchvision
from IPython.display import display
from sklearn.model_selection import train_test_split


import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns
from pylab import rcParams
import matplotlib.pyplot as plt
from matplotlib import rc

# %matplotlib inline
# %config InlineBackend.figure_format='retina'
# sns.set(style='whitegrid', palette='muted', font_scale=1.2)
# rcParams['figure.figsize'] = 16, 10

np.random.seed(42)
# from nuimages import NuImages
# nuim = NuImages(dataroot='./', version='v1.0-mini', verbose=True, lazy=True) #to change

#1. get samples_train and samples_val
# Opening JSON file to read sample.json
f = open('./train/thermal_annotations.json', mode='r') 
# returns JSON object as a dictionary
samples_train = json.load(f)    #each sample is an annotated image basically
# Closing file
f.close()

# Opening JSON file to read sample.json
f = open('./val/thermal_annotations.json', mode='r') 
# returns JSON object as a dictionary
samples_val = json.load(f)    #each sample is an annotated image basically
# Closing file
f.close()

#2. create list of images_json
images_train = samples_train.get('images')
images_val = samples_val.get('images')


#3. create list of categories using dict.get('key')
categories_dict = samples_train.get('categories') #categories_dict is an array of dictionaries
# print('categories is: ',categories_dict)
categories = []
for d in categories_dict:
  categories.append(d['name'])
# print('categories is: ', categories)


#4. create annotations for train and val
annotations_train = samples_train.get('annotations')
annotations_val = samples_val.get('annotations')

#5. create_dataset function
#yolov5 format is <class_index> bbox_x_center bbox_y_center bbox_width bbox_height
def create_dataset(dataset_type, annotations, images_json):
  IMG_W = 640
  IMG_H = 512
  images_path = Path(f"../{dataset_type}/images")
  images_path.mkdir(parents=True, exist_ok=True)

  labels_path = Path(f"../{dataset_type}/labels")
  # labels_path = Path(f"clothing/labels/{dataset_type}")
  labels_path.mkdir(parents=True, exist_ok=True)

  for img_id, row in enumerate(tqdm(images_json)):
    #img_id is 0 to n, row is just an element in images_json
    image_name = f"{img_id}.jpeg"
    ###testing
    # row = train_clothing[0] #row is just an image in training set
    # row = train_clothing[0]   #row is row 
    # print('row is ',row)

    #1. get img id and img path
    img_path = '/home/diho0521/FLIRdataset/FLIR_ADAS_1_3/' + dataset_type + '/' + row['file_name'] #edit this part (to be editted)
    # print(' \n image path is: ',img_path) #testing delete after done

    # img_path = row['file_name']
    img_id = row['id']
    # key_camera_token = row['key_camera_token'] 
    # for sample_data in samples_data:  ##for each sample_data in sample_data.json
    #     if key_camera_token == sample_data['token']:
    #       img_path = sample_data['filename']    #row is just an image in training set

    
    #method1: Resize image resize using opencv or cv
    # from google.colab.patches import cv2_imshow
    #step 1: resize using cv
    img = cv.imread(img_path, 1) #1 for image color, 0 for gray color
    img = cv.resize(img, (416,416), interpolation = cv.INTER_CUBIC)
    #step 2: save the img using cv
    im_path = str(images_path / image_name)
    print('im_path',im_path)
    cv.imwrite(im_path, img)    #e.g.: cv.imwrite('/content/savedImage.jpg', img)
    
    ###################################
    
    #method2: original   
    # img = Image.open(img_path)
    # img.save(str(images_path / image_name), "JPEG")
    #end of original

    label_name = f"{img_id}.txt"


    with (labels_path / label_name).open(mode="w") as label_file: 
      # category_token = ''     
      for obj_anno in annotations:  #write all annotations and category for this image using object_ann.json
        if img_id == obj_anno['image_id']:
          # label = ''
          #get bounding box
          b_box = obj_anno['bbox']
          x_min, y_min, w, h = b_box[0], b_box[1], b_box[2], b_box[3]
          #normalized the data
          w_norm = w / IMG_W 
          h_norm = h / IMG_H
          x_cent_norm = (x_min + w/2) / IMG_W
          y_cent_norm = (y_min + h/2) / IMG_H

          #get category id
          category_idx = obj_anno['category_id'] - 1 # minus 1 because annotation in json start at 1 but list start at 0  

          # category_token = obj_anno['category_token']   
          # bbox_width = x2 - x1
          # bbox_height = y2 - y1

          # #normalized the data
          # w = bbox_width / 1600
          # h = bbox_height/900
          # x_cent = (x1 + bbox_width/2) /1600
          # y_cent = (y1 + bbox_height/2) /900

          label_file.write(f"{category_idx} {x_cent_norm} {y_cent_norm} {w_norm} {h_norm}\n")
                  
          # # for a in row['annotation']:     #for each image
          # key_camera_token
          # for label in a['label']:      #write all annotations and category for this image using object_ann.json
        
#6. call create_dataset(dataset_type, annotations, images_json):
create_dataset('train', annotations_train, images_train) # samples_train is samples
create_dataset('val', annotations_val, images_val) # samples_train is samples