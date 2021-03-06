# -*- coding: utf-8 -*-
"""Final video segmentation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zf8DvaFBvQNVSSUve1_PpNGN5EV6IJE0

# **STEP 1: FIRST LETS CLONE THE MASK R CNN REPO**
"""

!git clone https://github.com/akTwelve/Mask_RCNN.git

"""# **STEP 2: INSTALL ALL THE REQUIREMENTS**"""

pip install -r /content/Mask_RCNN/requirements.txt

"""# **STEP 3: CLONE THE COCO API**"""

import os
os.chdir('/content/Mask_RCNN')

!git clone https://github.com/philferriere/cocoapi.git

"""## **STEP 4: INSTALL ALL THE LIBRARIES FOR COCO**"""

pip install git+https://github.com/philferriere/cocoapi.git#subdirectory=PythonAPI

"""# **STEP 5: DOWNLOAD THE WEIGHTS OF MASK RCNN TRAINED ON COCO DATASET**"""

!wget https://github.com/matterport/Mask_RCNN/releases/download/v2.0/mask_rcnn_coco.h5

"""## **STEP 6: DOWNLOAD THE VIDEO TO TO ANALYSED USING (!WGET)**"""

os.mkdir('/content/Mask_RCNN/videos')
os.chdir('/content/Mask_RCNN/videos')

!wget https://mk0analyticsindf35n9.kinstacdn.com/wp-content/uploads/2020/07/traffic_vid2.mp4

"""## **STEP 7: CHECK IF GPU IS ENABLED**"""

import tensorflow as tf
device_name = tf.test.gpu_device_name()
if device_name != '/device:GPU:0':
  raise SystemError('GPU device not found')
print('Found GPU at: {}'.format(device_name))

"""# **STEP 8: IMPORTING REQUIREMENTS**"""


import sys
import os
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt


# TO GET THE CURRENT WORKING DIRECTORY
ROOT_DIR = '/content/Mask_RCNN'
os.chdir(ROOT_DIR)
print('The Root directory is :', ROOT_DIR)

from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize

# TO GET THE COCO FILE DIRECTORY
coco_dir = os.path.join(ROOT_DIR, 'samples')
os.chdir(coco_dir)
print('The current directory is :',coco_dir)

from coco import coco
# %matplotlib inline 


# CREATING LOG DIRECTORY
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# CREATING VIDEO DIRECTORY
VIDEO_DIR = '/content/Mask_RCNN/videos'
VIDEO_SAVE_DIR = os.path.join(VIDEO_DIR, "save")

# MODEL WEIGHT DIRECTORY
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

# CHECKS IF IT EXISTS OR NOT
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

# DIRECTORY TO RUN TEST IMAGES
IMAGE_DIR = '/content/Mask_RCNN/images'

"""## **STEP 9: CONFIGURING THE COCO**"""

class InferenceConfig(coco.CocoConfig):
   
    GPU_COUNT = 1
    IMAGES_PER_GPU = 3

config = InferenceConfig()
config.display()

"""## **STEP 10: DEFINING FEW FUNCTIONS FOR MASKING**"""

import cv2
import numpy as np

def random_colors(N):
    np.random.seed(1)
    colors = [tuple(255 * np.random.rand(3)) for _ in range(N)]
    return colors


def apply_mask(image, mask, color, alpha=0.5):
    for n, c in enumerate(color):
        image[:, :, n] = np.where(
            mask == 1,
            image[:, :, n] * (1 - alpha) + alpha * c,
            image[:, :, n]
        )
    return image


def display_instances(image, boxes, masks, ids, names, scores):
    n_instances = boxes.shape[0]
    colors = random_colors(n_instances)

    if not n_instances:
        print('NO INSTANCES TO DISPLAY')
    else:
        assert boxes.shape[0] == masks.shape[-1] == ids.shape[0]

    for i, color in enumerate(colors):
        if not np.any(boxes[i]):
            continue

        y1, x1, y2, x2 = boxes[i]
        label = names[ids[i]]
        score = scores[i] if scores is not None else None
        caption = '{} {:.2f}'.format(label, score) if score else label
        mask = masks[:, :, i]

        image = apply_mask(image, mask, color)
        image = cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        image = cv2.putText(
            image, caption, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.7, color, 2
        )

    return image

"""## **STEP 11: INITIATING THE MODEL AND PROCESSING THE VIDEO**"""

# CREATING THE MODEL INSTANCE
model = modellib.MaskRCNN( mode="inference", model_dir=MODEL_DIR, config=config)

# LOADING THE PRE TRAINED WEIGHTS
model.load_weights(COCO_MODEL_PATH, by_name=True)

# DEFINING THE CLASSES OF CONTENTS PRE-TRAINED IN COCO
class_names = [
        'BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
        'bus', 'train', 'truck', 'boat', 'traffic light',
        'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
        'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
        'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
        'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
        'kite', 'baseball bat', 'baseball glove', 'skateboard',
        'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
        'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
        'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
        'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
        'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
        'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
        'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
        'teddy bear', 'hair drier', 'toothbrush'
    ]

# INPUT VIDEO USING OPENCV
capture = cv2.VideoCapture(os.path.join(VIDEO_DIR, 'traffic_vid2.mp4'))
try:
  if not os.path.exists(VIDEO_SAVE_DIR):
    os.makedirs(VIDEO_SAVE_DIR)
except OSError:
  print ('Error while creating the directory')
    
    
frames = []
frame_count = 0
batch_size = 3
t =1  
while True:
  # READING FRAME BY FRAME
  ret, frame = capture.read()

  # IF NO FRAMES DETECTED IT STOPS
  if not ret:
    break
        
  frame_count += 1
  frames.append(frame)
  print('frame :{0}'.format(frame_count))
  if len(frames) == batch_size:
    results = model.detect(frames, verbose=0)
    print('Processed batch: {}'.format(t))
    t+=1
    for i, item in enumerate(zip(frames, results)):
      frame = item[0]
      r = item[1]

      # CALLING THE INSTANCE SEG FUNCTION
      frame = display_instances(frame, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])
      name = '{0}.jpg'.format(frame_count)
      name = os.path.join(VIDEO_SAVE_DIR, name)
      cv2.imwrite(name, frame)
      
      frames = []
capture.release()

# CHECKING THE CONTENTS 
!ls /content/Mask_RCNN/videos/save

"""# **STEP 12: FUNCTION TO CONVERT IMAGES TO VIDEO**"""

# CHECKING THE VIDEO FPS
video = cv2.VideoCapture(os.path.join(VIDEO_DIR, 'traffic_vid2.mp4'));
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
if int(major_ver)  < 3 :
  fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
  print("Frames per second of the input video: {0}".format(fps))
else:
  fps = video.get(cv2.CAP_PROP_FPS)
  print("Frames per second of the input video: {0}".format(fps))
video.release();

# FUNCTION TO GENERATE VIDEO FROM IMAGES
def make_video(images, outimg=None, fps=fps, size=None,
               is_color=True, format="XVID"):
    
    from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
    fourcc = VideoWriter_fourcc(*format)
    vid = None
    for image in images:
        if not os.path.exists(image):
            raise FileNotFoundError(image)
        img = imread(image)
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = VideoWriter(outvid, fourcc, float(fps), size, is_color)
        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = resize(img, size)
        vid.write(img)
    vid.release()
    return vid

# SORTING THE IMAGES
import glob
images = list(glob.iglob(os.path.join(VIDEO_SAVE_DIR, '*.*')))
images = sorted(images, key=lambda x: float(os.path.split(x)[1][:-3]))

# CALLING THE FUNCTION
outvid = os.path.join(VIDEO_DIR, "Final_out.mp4")
make_video(images)

"""# **FINAL STEP: DOWNLOADING...**"""

from google.colab import files
files.download('/content/Mask_RCNN/videos/Final_out.mp4')
