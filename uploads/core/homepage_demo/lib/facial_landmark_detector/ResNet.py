import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim as slim


class ResNet(object):
    def __init__(self, image_size, num_landmarks, variance=[0.1, 0.1]):
        self.image_size = image_size
        self.num_landmarks = num_landmarks
        self.variance = variance
        self.reuse = False

    def model(self, images_T, is_training=True):
        bn_args = {
            'center': True,
            'scale': True,
            'is_training': is_training,
        }

        with tf.variable_scope('ResNet', reuse=self.reuse):
            ## data batch norm
            x = slim.batch_norm(images_T, center=False, scale=False, is_training=is_training, scope='data_bn')

            ## initial convolution
            x = slim.conv2d(x, 32, 7, 2, normalizer_fn=slim.batch_norm, normalizer_params=bn_args,
                            biases_initializer=None, scope='conv1')

            ## residual blocks
            x = residual_block(x, [64, 64], 3, 1, 'block1', is_training)
            x = residual_block(x, [128, 128], 3, 2, 'block2', is_training, 'pre')
            x = residual_block(x, [128, 128], 3, 1, 'block3', is_training, 'pre')

            x = residual_block(x, [128, 128], 3, 2, 'block4', is_training, 'pre')
            x = residual_block(x, [128, 128], 3, 1, 'block5', is_training, 'pre')

            x = residual_block(x, [128, 128], 3, 2, 'block6', is_training, 'pre')
            x = residual_block(x, [128, 128], 3, 1, 'block7', is_training, 'pre')

            x = slim.batch_norm(x, scope='post_bn', **bn_args)
            x = tf.nn.relu(x)

            ## top
            h,w = x.get_shape().as_list()[1:3]

            y_proj = slim.conv2d(x, 64, (h,1), padding='VALID', normalizer_fn=slim.batch_norm,
                                 normalizer_params=bn_args, biases_initializer=None, scope='y_proj')
            y_proj = slim.flatten(y_proj)
            x_score = slim.fully_connected(y_proj, self.num_landmarks, activation_fn=None, scope='x_score')
            x_score = tf.reshape(x_score, (-1, self.num_landmarks, 1))

            x_proj = slim.conv2d(x, 64, (1,w), padding='VALID', normalizer_fn=slim.batch_norm,
                                 normalizer_params=bn_args, biases_initializer=None, scope='x_proj')
            x_proj = slim.flatten(x_proj)
            y_score = slim.fully_connected(x_proj, self.num_landmarks, activation_fn=None, scope='y_score')
            y_score = tf.reshape(y_score, (-1, self.num_landmarks, 1))

            x = tf.concat([x_score, y_score], axis=2)

        self.reuse = True
        return x

    def get_test_tensors(self):
        images_T = tf.placeholder(tf.float32, (None, self.image_size[1], self.image_size[0], 3))
        prediction_T = self._decode_global_points(self.model(images_T, is_training=False))

        return images_T, prediction_T

    def _decode_global_points(self, score_T):
        '''
        convert prediction to points(landmarks)
        Input
            score_T: 3d tensor, shape=(batch_size,num_landmark,2)
        Output
            points_T: 3d tensor, shape=(batch_size,num_landmark,2)
        '''
        w,h = self.image_size
        temp_T = 0.5*tf.constant(self.image_size, tf.float32)
        points_T = score_T*tf.constant(self.variance, tf.float32)*temp_T+temp_T
        x_T = tf.clip_by_value(points_T[:,:,0], 0, w-1e-3)
        y_T = tf.clip_by_value(points_T[:,:,1], 0, h-1e-3)
        return tf.concat([tf.expand_dims(x_T, axis=2), tf.expand_dims(y_T, axis=2)], axis=2)


def residual_block(input_T, filters, kernel_size, strides, name, is_training=True,
                   activation_position=None,
                   weights_initializer=slim.initializers.variance_scaling_initializer(),
                   weights_regularizer=None):
    """Helper function to build residual block
    Input
        input_T: input tensor
        filters: list of integers, length 2 for basic block, 3 for bottleneck block
        kernel_size: integer
        strides: integer or list of integer(length is 2)
        name: prefix name for layers
        activation_position: None or 'pre' or 'post'
    Output
        output_T: output tensor
    """

    bn_args = {
        'center':True,
        'scale':True,
        'is_training':is_training,
    }
    conv_args = {
        'weights_initializer': weights_initializer,
        'weights_regularizer': weights_regularizer,
        'biases_initializer': None,
    }
    conv_bn_args = {
        'normalizer_fn': slim.batch_norm,
        'normalizer_params': bn_args,
        'weights_initializer': weights_initializer,
        'weights_regularizer': weights_regularizer,
        'biases_initializer': None,
    }

    channels_in = input_T.get_shape().as_list()[-1]
    channels_out = filters[-1]
    need_projection = channels_in != channels_out or np.any(np.array(strides) > 1)

    with tf.variable_scope(name):
        ## default output of the shortcut connection is same as the input
        shortcut_T = input_T

        if activation_position == 'pre':
            input_T = slim.batch_norm(input_T, scope='pre_bn', **bn_args)
            input_T = tf.nn.relu(input_T)

        if need_projection:
            shortcut_T = slim.conv2d(input_T, filters[-1], 1, stride=strides, activation_fn=None,
                                     scope='shortcut_conv', **conv_args)
            if activation_position == 'post':
                shortcut_T = slim.batch_norm(shortcut_T, scope='shortcut_bn', **bn_args)

        ## basic residual block
        if len(filters) == 2:
            ## block1
            residual_T = slim.conv2d(input_T, filters[0], kernel_size, stride=strides,
                                     scope='conv1', **conv_bn_args)

            ## block2
            residual_T = slim.conv2d(residual_T, filters[1], kernel_size, stride=1, activation_fn=None,
                                     scope='conv2', **conv_args)
            if activation_position == 'post':
                residual_T = slim.batch_norm(residual_T, scope='conv2_bn', **bn_args)

        ## bottleneck
        elif len(filters) == 3:
            ## block1
            residual_T = slim.conv2d(input_T, filters[0], 1, stride=strides,
                                     scope='conv1', **conv_bn_args)

            ## block2
            residual_T = slim.conv2d(residual_T, filters[1], kernel_size, stride=1,
                                     scope='conv2', **conv_bn_args)

            ## block3
            residual_T = slim.conv2d(residual_T, filters[2], 1, stride=1, activation_fn=None,
                                     scope='conv3', **conv_args)
            if activation_position == 'post':
                residual_T = slim.batch_norm(residual_T, scope='conv3_bn', **bn_args)
        else:
            raise LookupError

        output_T = tf.add(shortcut_T, residual_T)
        if activation_position == 'post':
            output_T = tf.nn.relu(output_T)

    return output_T