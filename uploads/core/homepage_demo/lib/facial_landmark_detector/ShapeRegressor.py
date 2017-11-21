import tensorflow as tf
import tensorflow.contrib.slim as slim

from uploads.core.homepage_demo.lib.facial_landmark_detector.ResNet import ResNet
from uploads.core.homepage_demo.lib.facial_landmark_detector.utils import *


class ShapeRegressor(object):
    def __init__(self, sess, model_path):
        self.image_size = (160,160)
        self.num_landmarks = 68
        self.variance = (0.2, 0.2)
        self.sess = sess

        ## create network
        self.net = ResNet(self.image_size, self.num_landmarks, self.variance)
        self.images_T, self.prediction_T = self.net.get_test_tensors()

        ## get model variables
        variables = slim.filter_variables(slim.get_model_variables(), include_patterns=['ResNet'])

        ## initialize variables
        self.sess.run(tf.variables_initializer(variables))

        ## load model
        restorer = tf.train.Saver(variables)
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
