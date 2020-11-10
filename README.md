# Video-Segmentation-using-Mask-RCNN


This is an implementation of [Mask R-CNN](https://arxiv.org/abs/1703.06870) on Python 3, Keras, and TensorFlow. The model generates bounding boxes and segmentation masks for each instance of an object in the image. It's based on Feature Pyramid Network (FPN) and a ResNet101 backbone.

[![Mask RCNN on 4K Video](Final_out.gif)]


# Step by Step procedure

## Step 1: FIRST LETS CLONE THE MASK R CNN REPO

!git clone https://github.com/akTwelve/Mask_RCNN.git

## Step 2: INSTALL ALL THE REQUIREMENTS

pip install -r /content/Mask_RCNN/requirements.txt

## Step 3: CLONE THE COCO API

!git clone https://github.com/philferriere/cocoapi.git

## Step 4: INSTALL ALL THE LIBRARIES FOR COCO

pip install git+https://github.com/philferriere/cocoapi.git#subdirectory=PythonAPI

## Step 5: DOWNLOAD THE WEIGHTS OF MASK RCNN TRAINED ON COCO DATASET

!wget https://github.com/matterport/Mask_RCNN/releases/download/v2.0/mask_rcnn_coco.h5

## Step 6: DOWNLOAD THE VIDEO TO TO ANALYSED USING (!WGET)

!wget https://mk0analyticsindf35n9.kinstacdn.com/wp-content/uploads/2020/07/traffic_vid2.mp4

## Step 7: CHECK THE GPU STATS

import tensorflow as tf
device_name = tf.test.gpu_device_name()
if device_name != '/device:GPU:0':
  raise SystemError('GPU device not found')
print('Found GPU at: {}'.format(device_name))

# Open the Python file and follow the inline code



