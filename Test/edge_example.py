import cv2
import numpy as np
from os import listdir




def AddBorder(img):
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
        value=[mean, mean, mean]
    )
    return border

def GetBackground(img):
    print(img[0][100])

for imgPath in listdir('Test/Logos/'):
    img = cv2.imread('Test/Logos/' + imgPath, cv2.IMREAD_UNCHANGED)
    GetBackground(img)

    '''gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    corners = cv2.cornerHarris(gray, 8, 3, 0.04)
    
    #corners = cv2.dilate(corners, None)

    cv2.imshow(imgPath+" g", gray)

    # Threshold for an optimal value, it may vary depending on the image.
    img[corners>0.01*corners.max()]=[0,0,255]
    cv2.imshow(imgPath, img)'''

cv2.waitKey(0)
