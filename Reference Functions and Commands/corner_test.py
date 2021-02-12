from cv2 import cv2 # added "from cv2" to remove all squiggly lines underneath cv2 functions, fix found from stackoverflow
import numpy as np
from os import listdir
import colorsys

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
    
def UpdateColorsWithPixel(colorDict, pixel, useAlpha):
    if useAlpha:
        key = "{},{},{},{}".format(*pixel)
    else:
        key = "{},{},{}".format(*pixel)

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
                UpdateColorsWithPixel(colors, img[0][curCol], True)
                UpdateColorsWithPixel(colors, img[row-1][curCol], True)
        else:
            UpdateColorsWithPixel(colors, img[curRow][0], True)
            UpdateColorsWithPixel(colors, img[curRow][col - 1], True)

    highestKey = ''
    highestValue = 0

    for key in colors:
        if colors[key] > highestValue:
            highestKey = key
            highestValue = colors[key]

    return [int(i) for i in highestKey.split(",")]


def GetAllColors(img):

    colors = {}

    row, col = img.shape[:2]

    lowestBlue = 256
    highestBlue = -1

    numBlue = 0
    totalNum = 0

    for curRow in range(row):
        for curCol in range(col):
            UpdateColorsWithPixel(colors, img[curRow][curCol][:3], False)

            hsv = colorsys.rgb_to_hsv(img[curRow][curCol][2]/255, img[curRow][curCol][1]/255, img[curRow][curCol][0]/255)

            if hsv[0] > .5028 and hsv[0] < .8333:
                numBlue += 1

            if img[curRow][curCol][0] != 0 or img[curRow][curCol][1] != 0 or img[curRow][curCol][2] != 0:
                totalNum += 1
                

            if hsv[0] < lowestBlue and hsv[0] != 0:
                lowestBlue = hsv[0] 
            if hsv[0] > highestBlue:
                highestBlue = hsv[0] 
    
    #print(colors)
    print(len(colors))
    print(lowestBlue)
    print(highestBlue)
    print(numBlue)
    print(totalNum)
    print(numBlue/totalNum)
    print(hsv)


for imgPath in listdir('Test/Logos/'):
    
    img = cv2.imread('Test/Logos/' + imgPath, cv2.IMREAD_UNCHANGED)

    GetAllColors(img)

    img = AddBorder(img, GetBackground(img))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    corners = cv2.cornerHarris(gray, 2, 1, 0.15)
    
    #corners = cv2.dilate(corners, None)

    # Threshold for an optimal value, it may vary depending on the image.
    img[corners>0.01*corners.max()]=[0, 0, 255, 1]

    cv2.imshow(imgPath, img)

cv2.waitKey(0)
