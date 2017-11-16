import numpy as np
import cv2


def apply_perspective_transform(H, points):
    temp = np.dot(H, np.transpose(np.hstack((points, np.ones((len(points),1))))))
    return np.transpose(temp[:2]/temp[2])


def preprocessing(image, output_size):
    w,h = output_size

    ## default homography
    H = np.identity(3)

    ## align center
    cy, cx = 0.5*np.array(image.shape[:2])
    H = np.dot(np.array([[1,0,-cx],[0,1,-cy],[0,0,1]]), H)

    ## scaling
    scale = np.min(np.array([h,w])/np.array(image.shape[:2]).astype(np.float))
    H = np.dot(np.array([[scale,0,0],[0,scale,0],[0,0,1]]), H)

    ## restore origin
    H = np.dot(np.array([[1,0,w*0.5],[0,1,h*0.5],[0,0,1]]), H)

    ## apply affine transform to image
    return cv2.warpAffine(image, H[:2], (w,h), flags=cv2.INTER_LINEAR), H


def color_from_scale(scale, cmin=0, cmax=1):
    try:
        # normalize to [0,1]
        x = float(scale-cmin)/float(cmax-cmin)
    except ():
        # cmax = cmin
        x = 0.5
    blue = int(min((max((4*(0.75-x), 0.)), 1.))*255)
    red  = int(min((max((4*(x-0.25), 0.)), 1.))*255)
    green= int(min((max((4*np.abs(x-0.5)-1., 0.)), 1.))*255)
    return blue, green, red


def colormap(num_scale):
    return [color_from_scale(s) for s in np.linspace(0,1,num_scale)]


def draw_points(image, points, colors=(0,255,0), radius=2):
    if points.ndim == 1:
        points = np.expand_dims(points, axis=0)

    if np.array(colors).ndim == 1:
        cmap = [colors]*len(points)
    elif np.array(colors).ndim == 2:
        cmap = colors
    else:
        raise ValueError

    image = image.copy()

    for i in range(len(points)):
        pt = tuple(points[i].astype(np.int32).tolist())
        cv2.circle(image, pt, radius=radius, color=cmap[i], thickness=-1)

    return image