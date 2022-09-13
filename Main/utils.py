from cv2 import cv2
import numpy as np

def resize(frame):
    width = 500
    height = int(frame.shape[0]/frame.shape[1]*width)
    dimensions = (width,height)
    return cv2.resize(frame,dimensions, interpolation = cv2.INTER_AREA)

def calcPercentage(msk): 
	# returns the percentage of white in a binary image 
	height, width = msk.shape[:2] 
	num_pixels = height * width 
	count_white = cv2.countNonZero(msk) 
	percent_white = (count_white/num_pixels) * 100 
	percent_white = round(percent_white,2) 
	return percent_white

def Percentage_of_Colors(logo, display, colorName):
    img = logo.img
    # img = cv.imread('Opencv/dog.jpg')
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # converting to hsv for better color processing

    if (colorName == "red"):
        lower_bound1 = np.array([0, 70, 50])
        upper_bound1 = np.array([10, 255, 255])
        lower_bound2 = np.array([172, 70, 50])
        upper_bound2 = np.array([180, 255, 255])
        msk1 = cv2.inRange(img_hsv, lower_bound1, upper_bound1)
        msk2 = cv2.inRange(img_hsv, lower_bound2, upper_bound2)
        # msk = cv2.hconcat(msk1,msk2)
        # msk = cv2.addWeighted(msk1,0.5,msk2,0.5,0.0)
        msk = msk1+msk2

    elif (colorName == "orange"):
        lower_bound1 = np.array([10, 70, 50])
        upper_bound1 = np.array([20, 255, 255])
        msk = cv2.inRange(img_hsv, lower_bound1, upper_bound1)

    elif (colorName == "yellow"):
        lower_bound1 = np.array([20, 70, 50])
        upper_bound1 = np.array([30, 255, 255])
        msk = cv2.inRange(img_hsv, lower_bound1, upper_bound1)

    elif (colorName == "green"):
        lower_bound1 = np.array([31, 70, 50])
        upper_bound1 = np.array([70, 255, 255])
        msk = cv2.inRange(img_hsv, lower_bound1, upper_bound1)
    
    elif (colorName == "cyan"):
        lower_bound1 = np.array([71, 70, 50])
        upper_bound1 = np.array([100, 255, 255])
        msk = cv2.inRange(img_hsv, lower_bound1, upper_bound1)

    elif (colorName == "cyan-blue"):
        lower_bound1 = np.array([100, 70, 50])
        upper_bound1 = np.array([110, 255, 255])
        msk = cv2.inRange(img_hsv, lower_bound1, upper_bound1)

    elif (colorName == "blue"):
        lower_bound1 = np.array([110, 70, 50])
        upper_bound1 = np.array([120, 255, 255])
        msk = cv2.inRange(img_hsv, lower_bound1, upper_bound1)
    
    elif (colorName == "purple"):
        lower_bound1 = np.array([120, 70, 50])
        upper_bound1 = np.array([140, 255, 255])
        msk = cv2.inRange(img_hsv, lower_bound1, upper_bound1)

    elif (colorName == "magenta"):
        lower_bound1 = np.array([140, 70, 50])
        upper_bound1 = np.array([160, 255, 255])
        msk = cv2.inRange(img_hsv, lower_bound1, upper_bound1)

    elif (colorName == "pink"):
        lower_bound1 = np.array([160, 70, 50])
        upper_bound1 = np.array([172, 255, 255])
        msk = cv2.inRange(img_hsv, lower_bound1, upper_bound1)

    # HSV Value boundaries from http://www.workwithcolor.com/red-color-hue-range-01.htm

    # sensitivity = 20 # check hsv chart for understanding 
    # lower_bound = np.array([color - sensitivity, 100, 60]) # 50 is in the center of green so 50 +- 20 will give the entire width
    # upper_bound = np.array([color + sensitivity, 255, 255]) # of green. [H, S, V] h is hue value, s is saturation, v is value or brightness
    # creates a binary mask for only green parts of an image. 
    # So in this case the green parts of an image will be white and the rest of the regions will be black.
    # msk = cv2.inRange(img_hsv, lower_bound, upper_bound)

    logo.attributes["Percentage of " + colorName] = calcPercentage(msk)

    flag = 1
    if display == 1:
        if flag == 1:
            cv2.imshow(logo.name, resize(img))
            flag = 0
        cv2.imshow(logo.name + '_' + colorName, resize(msk))
        cv2.waitKey(0)

def Number_of_Colors(logo, colorName):
    img = logo.img
    # img = cv.imread('Opencv/dog.jpg')
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # converting to hsv for better color processing

    if (colorName == "red"):
        lower_bound1 = np.array([0, 70, 50])
        upper_bound1 = np.array([10, 255, 255])
        lower_bound2 = np.array([172, 70, 50])
        upper_bound2 = np.array([180, 255, 255])
        msk1 = cv2.inRange(img_hsv, lower_bound1, upper_bound1)
        msk2 = cv2.inRange(img_hsv, lower_bound2, upper_bound2)
        # msk = cv2.hconcat(msk1,msk2)
        # msk = cv2.addWeighted(msk1,0.5,msk2,0.5,0.0)
        msk = msk1+msk2

    elif (colorName == "orange"):
        lower_bound1 = np.array([10, 70, 50])
        upper_bound1 = np.array([20, 255, 255])
        msk = cv2.inRange(img_hsv, lower_bound1, upper_bound1)

    elif (colorName == "yellow"):
        lower_bound1 = np.array([20, 70, 50])
        upper_bound1 = np.array([30, 255, 255])
        msk = cv2.inRange(img_hsv, lower_bound1, upper_bound1)

    elif (colorName == "green"):
        lower_bound1 = np.array([31, 70, 50])
        upper_bound1 = np.array([70, 255, 255])
        msk = cv2.inRange(img_hsv, lower_bound1, upper_bound1)
    
    elif (colorName == "cyan"):
        lower_bound1 = np.array([71, 70, 50])
        upper_bound1 = np.array([100, 255, 255])
        msk = cv2.inRange(img_hsv, lower_bound1, upper_bound1)

    elif (colorName == "cyan-blue"):
        lower_bound1 = np.array([100, 70, 50])
        upper_bound1 = np.array([110, 255, 255])
        msk = cv2.inRange(img_hsv, lower_bound1, upper_bound1)

    elif (colorName == "blue"):
        lower_bound1 = np.array([110, 70, 50])
        upper_bound1 = np.array([120, 255, 255])
        msk = cv2.inRange(img_hsv, lower_bound1, upper_bound1)
    
    elif (colorName == "purple"):
        lower_bound1 = np.array([120, 70, 50])
        upper_bound1 = np.array([140, 255, 255])
        msk = cv2.inRange(img_hsv, lower_bound1, upper_bound1)

    elif (colorName == "magenta"):
        lower_bound1 = np.array([140, 70, 50])
        upper_bound1 = np.array([160, 255, 255])
        msk = cv2.inRange(img_hsv, lower_bound1, upper_bound1)

    elif (colorName == "pink"):
        lower_bound1 = np.array([160, 70, 50])
        upper_bound1 = np.array([172, 255, 255])
        msk = cv2.inRange(img_hsv, lower_bound1, upper_bound1)

    return calcPercentage(msk)>0.0

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

def GetBlackWhiteBackground(img):
    pixelValues = {}

    row, col = img.shape[:2]

    for curRow in range(row-1):
        if curRow == 0:
            for curCol in range(col):
                UpdatePixelValues(pixelValues, img[0][curCol])
                UpdatePixelValues(pixelValues, img[row-1][curCol])
        else:
            UpdatePixelValues(pixelValues, img[curRow][0])
            UpdatePixelValues(pixelValues, img[curRow][col - 1])

    highestKey = ''
    highestValue = 0

    for key in pixelValues:
        if pixelValues[key] > highestValue:
            highestKey = key
            highestValue = pixelValues[key]

    return highestKey


def UpdatePixelValues(pixelValues, pixel):
    if isWhite(pixel):
        key = "white"
    elif isBlack(pixel):
        key = "black"
    else:
        key = "other"
    
    if key in pixelValues:
        pixelValues[key] += 1
    else:
        pixelValues[key] = 1


def removeBackground(img, color):
    assert(color == "white" or color == "black")

    row, col = img.shape[:2]

    for curRow in range(row):
        for curCol in range(col):
            if color == "white":
                if isWhite(img[curRow,curCol]):
                    img[curRow,curCol] = [0, 0, 0, 0]
            elif color == "black":
                if isBlack(img[curRow,curCol]):
                    img[curRow,curCol] = [0, 0, 0, 0]
    
    return img

def isWhite(pixel):
    return pixel[0] > 240 and pixel[1] > 240 and pixel[2] > 240

def isBlack(pixel):
    return pixel[0] < 15 and pixel[1] < 15 and pixel[2] < 15

def AddAlphaChannel(img):
    b_channel, g_channel, r_channel = cv2.split(img)
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

    backColor = utils.GetBlackWhiteBackground(img)

    if backColor != "other":
        imgNoBackground = utils.removeBackground(img_BGRA, backColor)
    else:
        imgNoBackground = img_BGRA

    return img_BGRA, imgNoBackground