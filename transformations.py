from cv2 import cv2 as cv
import numpy as np

img = cv.imread('Opencv/cb.jpg')

cv.imshow('Boop my nose', img)

# Translation
# Shifting an image along the x axis or y axis
def Translate(img, x, y):
    transMat = np.float32([[1,0,x],[0,1,y]]) #trasnMat is Translation matrix
    dimensions = (img.shape[1], img.shape[0])
    return cv.warpAffine(img, transMat, dimensions)

# -x --> Left
# -y --> Up
#  x --> Right
#  y --> Down

translated = Translate (img, -100, 100)
cv.imshow('Translated', translated)

# Rotation (by some angle from a set point (usually the center))
def rotate (img, angle, rotPoint=None):
    (height, width) = img.shape[:2] # [:2] takes values from shape [0] and shape [1] and puts into height and width

    if rotPoint is None:
        rotPoint = (width//2,height//2) # the floor division // rounds the result down to the nearest whole number
    
    rotMat = cv.getRotationMatrix2D(rotPoint, angle, 1.0)
    dimensions = (width,height)

    return cv.warpAffine(img, rotMat, dimensions) 
    
rotated = rotate(img, 45) # rotates counterclockwise by 45 degrees, pass negative values to rotate clockwise

cv.imshow('Rotated', rotated)

# you can also rotate rotated images

# Resizing
resized = cv.resize(img, (500,500), interpolation=cv.INTER_AREA)

cv.imshow('resized', resized)

# Flipping
flip = cv.flip(img, 0) # flipCode could either be 0,1 or -1 
                      #  0 = flip vertically (by the x-axis)
                      #  1 = flip horizontally (by the y-axis)
                      # -1 = flips both hori and vert

cv.imshow('Flip', flip)

# Cropping
crop = img[200:400, 300:400]

cv.imshow('Cropped', crop)

cv.waitKey(0)