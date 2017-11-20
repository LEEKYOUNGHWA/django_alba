import tensorflow as tf

from uploads.core.homepage_demo.lib.facial_landmark_detector.ShapeRegressor import ShapeRegressor
from uploads.core.homepage_demo.lib.welding_defect_recognizer.Recognizer import Recognizer


class SessionManager(object):
    def __init__(self):
        ## create session
        cp = tf.ConfigProto()
        cp.allow_soft_placement = True
        cp.gpu_options.allow_growth = True
        self.sess = tf.Session(config=cp)

    def close(self):
        tf.reset_default_graph()
        self.sess.close()


    ##############################
    ## facial landmark detector ##
    ##############################

    def init_facial_landmark_detector(self, model_path):
        self.fld = ShapeRegressor(self.sess, model_path)

    def run_facial_landmark_detector(self, image):
        return self.fld.run(image)

    def draw_facial_landmark_detector(self, image, points):
        return self.fld.draw(image, points)


    ##############################
    ## welding defect recognizer ##
    ##############################

    def init_welding_defect_recognizer(self, model_path):
        self.wdr = Recognizer(self.sess, model_path)

    def run_welding_defect_recognizer(self, image):
        return self.wdr.run(image)

    def draw_welding_defect_recognizer(self, image, label):
        return self.wdr.draw(image, label)

