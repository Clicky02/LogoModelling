from cv2 import cv2 


def testFunction(logo, display):
    img = logo.img
    # Do stuff with img here
    logo.attributes["Average Saturation"] = 10
    print(10)

def aveBrightness(logo, Disp = True, Tol = 0.10):
    image = logo.img
    #Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

    sumColor = 0
    numBack = 0

    grayNoBack = gray.copy()
    
    rows, cols = gray.shape
    for i in range(rows):
      for j in range(cols):
        #If white, replace with black (remove background)
        if (image[i,j,3] <= (1-(255*(1-Tol)))):
            numBack = numBack + 1

        #Add current pixel to the total of pixels
        sumColor = sumColor + grayNoBack[i,j]

    #Display processed images
    if Disp == 1:
        cv2.imshow("Unfiltered", image)
        cv2.imshow("Gray", gray)
        cv2.imshow("Gray, No Background", grayNoBack)

    numTotal = rows * cols
    numLogo = numTotal - numBack

    #Average brightness value for only logo (no background)
    AveBrightness = sumColor / numLogo
    PercentBrightness = AveBrightness / 255 * 100

    logo.attributes["Percent Brightness"] = PercentBrightness
    
def gradients(logo, display = 0, Tol = 0.1):
    image = logo.img

    cv2.imshow('normal',image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Gray',gray)
    gradientsAndEdges = cv2.Canny(image,-10000,-10000)
    cv2.imshow('Gradients and Edges',gradientsAndEdges)
    edges = cv2.Canny(image,125,125)
    cv2.imshow('Edges', edges)

    gradients = cv2.bitwise_xor(gradientsAndEdges, edges)
    cv2.imshow('Gradients', gradients)

    logoPixelCount = 0
    numGradients = 0

    # Count the number of pixels in the logo
    rows, cols = gray.shape
    for i in range(rows):
      for j in range(cols):
        if (not((gray[i,j] <= (1-(255*(1-Tol)))) or gray[i,j] >= (255*(1-Tol)))):
            logoPixelCount = logoPixelCount + 1
        if (gradients[i,j] == 255):
            numGradients = numGradients + 1

    PercentGradients = numGradients / logoPixelCount * 100
    cv2.waitKey(0)

    logo.attributes["Percent Gradient"] = PercentGradients
    
#Add name of function to this array
ExportFunctions = [testFunction]

#Add name of function to this array if you want to test
TestFunctions = [testFunction]

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