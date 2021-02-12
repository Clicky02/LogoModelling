# Nicholas Haehn
# Brightnes Module

# This module implements a function in order to determine the brightness
# of a logo based on the amount of 'white' in the image

import cv2 as cv
import numpy as np

def rescaleFrame (frame, scale=0.1):
    width = int(frame.shape[1]*scale)
    height = int(frame.shape[0]*scale)
    dimensions = (width,height)

    return cv.resize(frame,dimensions, interpolation = cv.INTER_AREA)
    
def aveBrightness(image):

    cv.imshow("Unfiltered", image)

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    cv.imshow("Gray", gray)

    sumColor = 0
    numBack = 0

    rows, cols = gray.shape
    for i in range(rows):
      for j in range(cols):
        #If white, replace with black (remove background)
        if gray[i,j] >= 230:
            gray[i,j] = 0
            numBack = numBack + 1

        #Add current pixel to the total of pixels
        sumColor = sumColor + gray[i,j]
    
    cv.imshow("Gray black", gray)

    numTotal = len(gray)*len(gray[0])
    numLogo = numTotal - numBack

    #Average brightness value for only logo (no background)
    AveBrightness = sumColor / numTotal
    PercentBrightness = AveBrightness / 255 * 100

    return PercentBrightness

    
    

img = cv.imread("Test.jpg")
img = rescaleFrame(img, 0.5)
ave = aveBrightness(img)
print("{0:0.2f}%\n".format(ave))

#img = removeBackground(img)

