from cv2 import cv2 
import utils

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
        # I don't think this block of code is necessary anymore as main.py gives all pixels an alpha value of 255 (opaque) ~ PG
        if (image[i,j,3] <= (255-(255*(1-Tol)))):
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
        if (image[i,j,3] <= (255-(255*(1-Tol)))):
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

def Main_for_Percent_of_Colors(logo, display):
    utils.Percentage_of_Colors(logo, display, "red")
    utils.Percentage_of_Colors(logo, display, "orange")
    utils.Percentage_of_Colors(logo, display, "yellow")
    utils.Percentage_of_Colors(logo, display, "green")
    utils.Percentage_of_Colors(logo, display, "cyan")
    utils.Percentage_of_Colors(logo, display, "cyan-blue")
    utils.Percentage_of_Colors(logo, display, "blue")
    utils.Percentage_of_Colors(logo, display, "purple")
    utils.Percentage_of_Colors(logo, display, "magenta")
    utils.Percentage_of_Colors(logo, display, "pink")
    cv2.destroyAllWindows() # removes all open windows for the referenced logo

def Main_for_Number_of_Colors(logo, display): # Black and White do not count as colors
    ctr = 0
    if(utils.Number_of_Colors(logo, "red")): #Number of colors returns true or false if red % is >0
        ctr = ctr + 1
    if(utils.Number_of_Colors(logo, "orange")):
        ctr = ctr + 1
    if(utils.Number_of_Colors(logo, "yellow")):
        ctr = ctr + 1
    if(utils.Number_of_Colors(logo, "green")):
        ctr = ctr + 1
    if(utils.Number_of_Colors(logo, "cyan")):
        ctr = ctr + 1
    if(utils.Number_of_Colors(logo, "cyan-blue")):
        ctr = ctr + 1
    if(utils.Number_of_Colors(logo, "blue")):
        ctr = ctr + 1
    if(utils.Number_of_Colors(logo, "purple")):
        ctr = ctr + 1
    if(utils.Number_of_Colors(logo, "magenta")):
        ctr = ctr + 1
    if(utils.Number_of_Colors(logo, "pink")):
        ctr = ctr + 1
    
    if(ctr>=2):
        logo.attributes["Multicolored?"] = True
        logo.attributes["Number of colors"] = ctr
    else:
        logo.attributes["Multicolored?"] = False

#Add name of function to this array
ExportFunctions = []

#Add name of function to this array if you want to test
TestFunctions = [aveBrightness, gradients, Main_for_Percent_of_Colors, Main_for_Number_of_Colors]

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