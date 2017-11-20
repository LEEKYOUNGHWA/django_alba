import numpy as np

import tensorflow as tf
import tensorflow.contrib.slim as slim


class LeNet(object):
    def __init__(self, image_size, num_class):
        self.image_size = image_size
        self.num_class = num_class
        self.reuse = False

    def model(self, images_T, is_training=True):
        bn_args = {
            'center': False,
            'scale': False,
            'is_training': is_training,
        }

        with tf.variable_scope('LeNet', reuse=self.reuse):
            ## data batch norm
            x = slim.batch_norm(images_T, scope='data_bn', **bn_args)

            ## stack convolution
            x = slim.conv2d(x, 24, 7, scope='conv1')
            x = slim.max_pool2d(x, 3, 2, scope='pool1')

            x = slim.conv2d(x, 32, 5, scope='conv2_1')
            x = slim.max_pool2d(x, 2, 2, scope='pool2')

            x = slim.conv2d(x, 48, 5, scope='conv3_1')
            x = slim.max_pool2d(x, 2, 2, scope='pool2')

            x = slim.conv2d(x, 64, 3, scope='conv4_1')
            x = slim.conv2d(x, 64, 3, scope='conv4_2')
            x = slim.conv2d(x, 64, 3, scope='conv4_3')
            # x = slim.max_pool2d(x, 2, 2, scope='pool3')

            ## top
            x = slim.flatten(x)
            x = slim.fully_connected(x, 256, scope='fc1')
            x = slim.dropout(x, keep_prob=0.6, is_training=is_training)
            x = slim.fully_connected(x, 256, scope='fc2')

            ## classifier
            x = slim.fully_connected(x, self.num_class, activation_fn=None, scope='score')

        self.reuse = True
        return x

    def get_test_tensors(self):
        images_T = tf.placeholder(tf.float32, (None, self.image_size[1], self.image_size[0], 1))
        prob_T = tf.nn.softmax(self.model(images_T, is_training=False), dim=-1)

        return images_T, prob_T

