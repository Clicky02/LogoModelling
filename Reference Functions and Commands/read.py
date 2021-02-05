#use 'from cv2' to remove squiggly lines 
from cv2 import cv2 as cv

# rescales image to smaller size
def rescaleFrame (frame, scale=0.1):
    width = int(frame.shape[1]*scale)
    height = int(frame.shape[0]*scale)
    dimensions = (width,height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

#read an image into a variable
img = cv.imread('Opencv/dog.jpg')

#calling rescaleFrame function
resized_image = rescaleFrame(img)

#Display rescales image ('Dog' is the name of the window to be displayed)
cv.imshow('Dog', resized_image)

#waits for key press to continue (0 is infinity)
cv.waitKey(0)

#display normally
cv.imshow('Dog', img)

cv.waitKey(0)