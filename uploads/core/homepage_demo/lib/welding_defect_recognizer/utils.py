import numpy as np
import cv2


def first_preprocessing(image, roi=None, params={}):
    roi_params = params['roi']
    output_size = roi_params.get('output_size')
    margin_ratio = roi_params.get('margin_ratio')
    roi = np.array(roi)

    ## default homography
    H = np.identity(3)

    ## move the roi so that the center of the roi is the origin.
    cx, cy = roi.reshape(2,2).mean(axis=0)
    H = np.dot(translation(-cx, -cy), H)

    ## scaling
    sx, sy = np.array(output_size, np.float)*(1-margin_ratio)/(roi[2:]-roi[:2]+1)
    H = np.dot(scaling(sx, sy), H)

    ## restore origin
    w,h = output_size
    H = np.dot(translation(0.5*w, 0.5*h), H)

    ## apply affine transform to image and roi
    image = cv2.warpAffine(image, H[:2], (w,h), flags=cv2.INTER_LINEAR)
    roi = apply_perspective_transform(H, roi.reshape(2,2)).ravel().tolist()

    if 'to_gray' in params:
        if params['to_gray'] and image.ndim == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        elif not params['to_gray'] and image.ndim == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    return image, roi


def second_preprocessing(image, roi=None, params={}):
    ## convert uint8 image to float32
    if image.dtype == np.uint8:
        image = image.astype(np.float32)/255.0

    ## output size
    w,h = params.get('output_size', image.shape[:2][::-1])

    ## check roi
    if roi is None:
        roi = [0,0,w-1,h-1]
    roi = np.array(roi)

    ## default homography
    H = np.identity(3)

    ## move the roi so that the center of the roi is the origin.
    cx, cy = roi.reshape(2,2).mean(axis=0)
    H = np.dot(translation(-cx, -cy), H)

    ## fit roi to output size
    sx, sy = np.array([w,h], np.float)/(roi[2:]-roi[:2]+1)
    H = np.dot(scaling(sx, sy), H)

    ## restore origin
    H = np.dot(translation(0.5*w, 0.5*h), H)

    ## apply affine transform to image
    image = np.clip(cv2.warpAffine(image, H[:2], (w,h), flags=cv2.INTER_LINEAR), 0.0, 1.0)

    ## to bgr
    if 'color' in params:
        if params['color'].get('to_bgr', False) and image.ndim == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        elif not params['color'].get('to_bgr', False) and image.ndim == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ## scale up to 255.0 (intensity)
    image *= 255.0

    if image.ndim == 2:
        image = np.expand_dims(image, axis=2)

    return image


def translation(dx, dy):
    T = np.identity(3)
    T[0,2] = dx
    T[1,2] = dy
    return T


def scaling(sx, sy):
    return np.diag([sx, sy, 1])


def apply_perspective_transform(H, points):
    temp = np.dot(H, np.transpose(np.hstack((points, np.ones((len(points),1))))))
    return np.transpose(temp[:2]/temp[2])

