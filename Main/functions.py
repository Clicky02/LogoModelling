from cv2 import cv2 
import utils
import numpy as np

def testFunction(logo, display):
    img = logo.img
    # Do stuff with img here
    logo.attributes["Average Saturation"] = 10
    print(10)

def aveBrightness(logo, display = False, Tol = 0.10):
    image = logo.img
    #Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

    sumColor = 0
    numBack = 0

    grayNoBack = gray.copy()
    
    rows, cols = gray.shape
    for i in range(rows):
      for j in range(cols):
        #If background is transparent, add one to the number of background pixels
        if (image[i,j,3] <= (1-(255*(1-Tol)))):
            numBack = numBack + 1

        #Add current pixel to the total of pixels
        sumColor = sumColor + grayNoBack[i,j]

    #Display processed images
    if display == 1:
        cv2.imshow("Unfiltered", utils.resize(image))
        cv2.imshow("Gray", utils.resize(gray))
        cv2.imshow("Gray, No Background", utils.resize(grayNoBack))
        cv2.waitKey(0)

    numTotal = rows * cols
    numLogo = numTotal - numBack

    #Average brightness value for only logo (no background)
    AveBrightness = sumColor / numLogo
    PercentBrightness = AveBrightness / 255 * 100

    logo.attributes["Percent Brightness"] = PercentBrightness
    
def gradients(logo, display = False, Tol = 0.1):
    image = logo.img

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)          # Create Grayscale
    gradientsAndEdges = cv2.Canny(image,-10000,-10000)      # Create gradients and edges
    edges = cv2.Canny(image,200,200)                        # Create edges
    gradients = cv2.bitwise_xor(gradientsAndEdges, edges)   # Subtract edges from gradients and edges to get only gradients

    numBack = 0
    numGradients = 0

    # Count the number of pixels in the logo
    rows, cols = gray.shape
    for i in range(rows):
      for j in range(cols):
        #If background is transparent, add one to the number of background pixels
        if (image[i,j,3] <= (1-(255*(1-Tol)))):
            numBack = numBack + 1
        if (gradients[i,j] == 255):
            numGradients = numGradients + 1

    # Display processed images
    if display == 1:
        cv2.imshow("Unfiltered", utils.resize(image))
        cv2.imshow("Gray", utils.resize(gray))
        cv2.imshow('Gradients and Edges', utils.resize(gradientsAndEdges))
        cv2.imshow('Edges', utils.resize(edges))
        cv2.imshow('Gradients', utils.resize(gradients))
        cv2.waitKey(0)

    numTotal = rows * cols
    numLogo = numTotal - numBack

    PercentGradients = numGradients / numLogo * 100
    cv2.waitKey(0)

    logo.attributes["Percent Gradient"] = PercentGradients

def calcPercentage(msk): 
	# returns the percentage of white in a binary image 
	height, width = msk.shape[:2] 
	num_pixels = height * width 
	count_white = cv2.countNonZero(msk) 
	percent_white = (count_white/num_pixels) * 100 
	percent_white = round(percent_white,2) 
	return percent_white

def MAIN_FOR_PERCENT_OF_COLORS(logo, display):
    Percentage_of_Colors(logo, display, 50, 20, "green")
    Percentage_of_Colors(logo, display, 5, 5, "red")
    Percentage_of_Colors(logo, display, 100, 10, "light blue")
    Percentage_of_Colors(logo, display, 120, 10, "dark blue")

def Percentage_of_Colors(logo, display, color, sensitivity, colorName):
    img = logo.img
    # img = cv.imread('Opencv/dog.jpg')
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # converting to hsv for better color processing

    sensitivity = 20 # check hsv chart for understanding 
    lower_bound = np.array([color - sensitivity, 100, 60]) # 50 is in the center of green so 50 +- 20 will give the entire width
    upper_bound = np.array([color + sensitivity, 255, 255]) # of green. [H, S, V] h is hue value, s is saturation, v is value or brightness
    # creates a binary mask for only green parts of an image. 
    # So in this case the green parts of an image will be white and the rest of the regions will be black.
    msk = cv2.inRange(img_hsv, lower_bound, upper_bound)

    logo.attributes["Percentage of " + colorName] = calcPercentage(msk)
    
#Add name of function to this array
ExportFunctions = []

#Add name of function to this array if you want to test
TestFunctions = [aveBrightness]

'''
HOW TO TEST YOU FUNCTION
------------------------

1. Pick what logos you want to test with and make sure they are 
the only logos in the TestLogos folder

2. Add your function name to the TestFunctions array (and delete any 
other functions in there unless you want to test those functions too)

3. Make sure the TEST_MODE variable in the main.py file is set to True.

4. Run main.py

This will run your function once for every logo in the TestLogos folder.

Note: If the logo has an alpha channel (transparent parts), each pixel in
the image will have 4 values. The last one is an alpha value.
'''