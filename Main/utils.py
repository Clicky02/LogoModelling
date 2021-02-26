from cv2 import cv2 

def resize(frame):
    width = 500
    height = int(frame.shape[0]/frame.shape[1]*width)
    dimensions = (width,height)

    return cv2.resize(frame,dimensions, interpolation = cv2.INTER_AREA)