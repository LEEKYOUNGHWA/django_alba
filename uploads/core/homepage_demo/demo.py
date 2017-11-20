import cv2
from uploads.settings import BASE_DIR
from uploads.settings import sm
#from uploads.core.homepage_demo.lib.SessionManager import SessionManager

def FacialLandmark(filepath, filename):

    ###################################
    ## Test facial landmark detector ##
    ###################################

    ##print('initialize network...')
    ## create session manager
    #sm = SessionManager()

    imagePath = BASE_DIR

    ## initialize facial landmark detector
    #model_path = imagePath+'/uploads/core/homepage_demo/model/facial_landmark_detector/final'
    #sm.init_facial_landmark_detector(model_path)

    ## read image
    image = cv2.imread(imagePath + filepath)
    ## detect facial landmarks
    points = sm.run_facial_landmark_detector(image)

    ## draw landmarks on image
    result = sm.draw_facial_landmark_detector(image, points)

    ## save result
    newimagepath = imagePath + "/media/result/" + filename
    cv2.imwrite(newimagepath, result)
    cv2.waitKey(0)

    ## close session manager
    ##sm.close()

    return "/media/result/" + filename

def WeldingDefect(filepath, filename):
    ####################################
    ## Test welding defect recognizer ##
    ####################################

    print('initialize network...')
    ## create session manager
    #sm = SessionManager()

    imagePath = BASE_DIR

    ## initialize welding defect recognizer
    ##model_path = imagePath+'/uploads/core/homepage_demo/model/welding_defect_recognizer/final'
    ##sm.init_welding_defect_recognizer(model_path)

    ## read image
    image = cv2.imread(imagePath + filepath)

    ## recognize welding defect
    label = sm.run_welding_defect_recognizer(image)

    ## draw landmarks on image
    result = sm.draw_welding_defect_recognizer(image, label)

    ## save result
    newimagepath = imagePath + "/media/result/" + filename
    cv2.imwrite(newimagepath, result)
    cv2.waitKey(0)
    ## close session manager
    #sm.close()

    return "/media/result/" + filename


