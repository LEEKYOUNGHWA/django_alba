import os
import numpy as np
import cv2
import timeit as ti
from uploads.settings import BASE_DIR
from uploads.settings import sr
from uploads.core.facial_landmarks_detection_demo.facial_landmarks_detection_demo.lib.Detector import ShapeRegressor

def FacialLandmark(filepath, filename):
    imagePath = BASE_DIR
    ## read image
    image = cv2.imread(imagePath + filepath)

    ## initialize network
    #print('initialize network...')
    #model_path = BASE_DIR+'/uploads/core/facial_landmarks_detection_demo/facial_landmarks_detection_demo/model/final'
    #sr = ShapeRegressor(model_path)

    ## detect facial landmarks
    print('detect facial landmarks...')
    t1 = ti.default_timer()
    points = sr.run(image)
    t2 = ti.default_timer()
    print('  {:.4f} sec elapsed'.format(t2-t1))

    ## draw landmarks on image
    print('draw landmarks...')
    result = sr.draw(image, points)

    ## show result
    ##cv2.namedWindow('result', cv2.WINDOW_KEEPRATIO)
    ##cv2.imshow('result', result)
    ##cv2.waitKey()
    ##cv2.destroyAllWindows()

    ## save result
    newimagepath = imagePath + "/media/result/detect" + filename
    cv2.imwrite(newimagepath, result)
    cv2.waitKey(0)
    return "/media/result/detect" + filename
