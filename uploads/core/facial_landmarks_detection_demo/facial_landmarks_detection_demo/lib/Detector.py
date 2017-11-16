import numpy as np
import cv2

import tensorflow as tf
import tensorflow.contrib.slim as slim

from uploads.core.facial_landmarks_detection_demo.facial_landmarks_detection_demo.lib.Network import ResNet
from uploads.core.facial_landmarks_detection_demo.facial_landmarks_detection_demo.lib.utils import *


class ShapeRegressor(object):
    def __init__(self, model_path):
        self.image_size = (160,160)
        self.num_landmarks = 68
        self.variance = (0.2, 0.2)


        ## create session
        cp = tf.ConfigProto()
        cp.allow_soft_placement = True
        cp.gpu_options.allow_growth = True
        self.sess = tf.Session(config=cp)
	
        ## create network
        self.net = ResNet(self.image_size, self.num_landmarks, self.variance)
        self.images_T, self.prediction_T = self.net.get_test_tensors()

        ## initialize variables
        self.sess.run(tf.global_variables_initializer())

        ## load model
        restorer = tf.train.Saver(slim.get_model_variables())
        restorer.restore(self.sess, model_path)

        ## create color map
        self.cmap = colormap(self.num_landmarks)

    def run(self, image):
        trans_image, H = preprocessing(image, self.image_size)
        points = self.sess.run(self.prediction_T, {self.images_T:trans_image[None]})
        return apply_perspective_transform(np.linalg.inv(H), points[0])

    def draw(self, image, points):
        radius = int(min(image.shape[:2])*0.015)
        return draw_points(image, points, self.cmap, radius)
