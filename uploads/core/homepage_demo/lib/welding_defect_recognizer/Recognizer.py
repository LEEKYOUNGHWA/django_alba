import tensorflow as tf
import tensorflow.contrib.slim as slim

from uploads.core.homepage_demo.lib.welding_defect_recognizer.LeNet import LeNet
from uploads.core.homepage_demo.lib.welding_defect_recognizer.utils import *


class Recognizer(object):
    def __init__(self, sess, model_path):
        self.image_size = (120,48)
        self.num_class = 2
        self.roi = [11, 500, 2570, 1523]
        self.colors = [(0,0,255), (0,255,0)]
        self.label_to_class = ['NG', 'OK']
        self.sess = sess

        ## create network
        self.net = LeNet(self.image_size, self.num_class)
        self.images_T, self.prob_T = self.net.get_test_tensors()

        ## get model variables
        variables = slim.filter_variables(slim.get_model_variables(), include_patterns=['LeNet'])

        ## initialize variables
        self.sess.run(tf.variables_initializer(variables))

        ## load model
        restorer = tf.train.Saver(variables)
        restorer.restore(self.sess, model_path)

        ## transform params
        self.first_transform_params = {
            "to_gray": True,
            "roi": {
                "output_size": [320,128],
                "margin_ratio": 0.3,
            }
        }
        self.second_transform_params = {
            "color": {
                "to_bgr": False,
            },
            "output_size": [120,48],
        }

    def run(self, image):
        image, roi = first_preprocessing(image, self.roi, self.first_transform_params)
        image = second_preprocessing(image, roi, self.second_transform_params)
        prob = self.sess.run(self.prob_T, {self.images_T:image[None]})[0]
        return np.argmax(prob)

    def draw(self, image, label):
        image = image.copy()
        class_name = self.label_to_class[label]
        # class_conf = '{:.2f}'.format(conf)
        color = self.colors[label]
        cv2.putText(image, class_name, (10,280), cv2.FONT_HERSHEY_PLAIN, 25, color, thickness=20)
        # cv2.putText(image, class_conf, (10,550), cv2.FONT_HERSHEY_PLAIN, 25, color, thickness=20)
        return image
