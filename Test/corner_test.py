import cv2
import numpy as np
from os import listdir

def AddBorder(img, backgroundColor):
    row, col = img.shape[:2]
    bottom = img[row-2:row, 0:col]
    mean = cv2.mean(bottom)[0]

    bordersize = 10
    border = cv2.copyMakeBorder(
        img,
        top=bordersize,
        bottom=bordersize,
        left=bordersize,
        right=bordersize,
        borderType=cv2.BORDER_CONSTANT,
        value=backgroundColor
    )
    return border
    
def UpdateColorsWithPixel(colorDict, pixel):

    key = "{},{},{},{}".format(*pixel)

    if key in colorDict:
        colorDict[key] += 1
    else:
        colorDict[key] = 1

#Gets the most common color on the border of the passed in image.
#Hopfully, this is the background color
def GetBackground(img):

    colors = {}

    row, col = img.shape[:2]

    for curRow in range(row-1):
        if curRow == 0:
            for curCol in range(col):
                UpdateColorsWithPixel(colors, img[0][curCol])
                UpdateColorsWithPixel(colors, img[row-1][curCol])
        else:
            UpdateColorsWithPixel(colors, img[curRow][0])
            UpdateColorsWithPixel(colors, img[curRow][col - 1])

    highestKey = ''
    highestValue = 0

    for key in colors:
        if colors[key] > highestValue:
            highestKey = key
            highestValue = colors[key]

    return [int(i) for i in highestKey.split(",")]

        


for imgPath in listdir('Test/Logos/'):
    img = cv2.imread('Test/Logos/' + imgPath, cv2.IMREAD_UNCHANGED)

    img = AddBorder(img, GetBackground(img))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    corners = cv2.cornerHarris(gray, 8, 3, 0.04)
    
    #corners = cv2.dilate(corners, None)

    

    # Threshold for an optimal value, it may vary depending on the image.
    img[corners>0.01*corners.max()]=[0, 0, 255, 1]

    cv2.imshow(imgPath+" c", corners)
    cv2.imshow(imgPath+" g", gray)
    cv2.imshow(imgPath, img)

cv2.waitKey(0)
