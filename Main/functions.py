from cv2 import cv2
import utils
import numpy as np

def detectShapes(logo, display):
    img = logo.borderedImg

    #img = cv2.resize(img, (img.shape[1]*2, img.shape[0]*2))

    if (display):
        disImg = img.copy()

    grayImg = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    #edges = cv2.Canny(grayImg, 30, 100)  

    contours, hierarchy = cv2.findContours(grayImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    rectangles = 0
    triangles = 0
    circles = 0

    blur = cv2.medianBlur(grayImg, 5)

    circleObjects = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, 100)

    if circleObjects is not None:

        circles = len(circleObjects[0])

        if display:
            circleObjects = np.round(circleObjects[0, :]).astype("int") #round locations to integers
            for (x, y, r) in circleObjects:
                cv2.circle(disImg, (x, y), r, (0, 0, 255), 4) #draw circle

    for cnt in contours:

        epsilon = 0.005*cv2.arcLength(cnt, True)

        if epsilon >= .05:

            approx = cv2.approxPolyDP(cnt, epsilon, True)

            newDisImg = img.copy()

            cv2.drawContours(newDisImg, cnt, -1, (255,50,90), 3)

            if len(approx) == 3:

                triangles += 1

                if display:
                    cv2.drawContours(disImg, cnt, -1, (0,255,0), 3)

            elif len(approx) == 4:

                rectangles += 1

                if display:
                    cv2.drawContours(disImg, cnt, -1, (255,0,0), 3)


    logo.attributes["Rectangles"] = rectangles
    logo.attributes["Triangles"] = triangles
    logo.attributes["Circles"] = circles

    if (display):
        cv2.imshow("abc", disImg)
        cv2.waitKey(0)

def colorfulness(logo, display):
    img = logo.img

    # split the image into its respective RGB components
    B, G, R, A = cv2.split(img)


    rg = np.absolute(R - G)
    yb = np.absolute(0.5 * (R + G) - B)

    rbMean, rbStd = (np.mean(rg), np.std(rg))
    ybMean, ybStd = (np.mean(yb), np.std(yb))

	# combine the mean and standard deviations
    stdRoot = np.sqrt((rbStd ** 2) + (ybStd ** 2))
    meanRoot = np.sqrt((rbMean ** 2) + (ybMean ** 2))

	# derive the "colorfulness" metric and return it
    colorfulness = stdRoot + (0.3 * meanRoot)

    logo.attributes["Colorfulness"] = colorfulness

def colorVariance(logo, display):
    img = logo.img

    #Seperate alpha channel to use as mask
    A = cv2.split(img)[3]

    ret, mask = cv2.threshold(A, 30, 255, cv2.THRESH_BINARY)

    bgrMean, bgrStdDev = cv2.meanStdDev(img, mask=mask)

    logo.attributes["Average R"] = bgrMean[2][0]
    logo.attributes["Average G"] = bgrMean[1][0]
    logo.attributes["Average B"] = bgrMean[0][0]
    logo.attributes["Standard Deviation R"] = bgrStdDev[2][0]
    logo.attributes["Standard Deviation G"] = bgrStdDev[1][0]
    logo.attributes["Standard Deviation B"] = bgrStdDev[0][0]

    hsvImg = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGRA2BGR), cv2.COLOR_BGR2HSV)

    hueValues = cv2.split(hsvImg)[0]

    #Inverts mask (because of how numpy masks work)
    mask = ((mask / 255) - 1) * -1

    masked = np.ma.masked_array(hueValues, mask=mask)
    hueValues = masked.compressed() #Gets a 1d array of non-masked values

    #Convert hue (normally in degrees) to radians
    hueValuesRad = np.deg2rad(hueValues)

    #Get x and y positions
    x = np.cos(hueValuesRad)

    y = np.sin(hueValuesRad)

    #Get average hue (in degrees)
    averageHue = np.arctan2(np.mean(y),np.mean(x))*(180/3.14159265358979)

    #Create function to get the distance between the value and the average hue
    def GetHueDistance(hue):
        d = abs(hue - averageHue)
        if d > 90:
            d = 180 - d
        return d

    #Vectorize it (make it so it will apply to all values in an array)
    distFunc = np.vectorize(GetHueDistance)

    #Calculate std dev using this formula
    hueStdDev = (np.sum(np.square(distFunc(hueValues)))/(len(hueValues)))**(1/2)

    logo.attributes["Average Hue"] = averageHue*(359/179) #Hue scaled to 360 degree convention
    logo.attributes["Hue Standard Deviation"] = hueStdDev*(359/179) #Hue scaled to 360 degree convention

def whitespace(logo, display):
    '''
    This function determines how much whitespace there is as a percent
    by going across each row of pixels and counting how many transparent
    pixels there are between colored pixels.
    '''
    img = logo.img

    if display:
        disImg = np.zeros_like(img)

    rows, columns = img.shape[:2]

    horizontalWhitespace = 0
    totalCountedPixels = 0
    for row in range(rows):

        hasFoundForeground = False #whether a non-whitespace pixel has already been found in the row
        currentGap = 0 #Used to count the current amount of whitespace in succession

        for col in range(columns):
            if img[row, col, 3] < 10:
                currentGap += 1
            else:
                #If it finds a colored pixel after finding another colored
                #pixel and whitespace, add the amount of whitespace to the
                #total whitespace
                if currentGap > 0 and hasFoundForeground:
                    horizontalWhitespace += currentGap
                    totalCountedPixels += currentGap

                    if display:
                        for i in range(col-currentGap, col):
                            disImg[row, i] = [255, 255, 255, 255]


                totalCountedPixels += 1
                currentGap = 0
                hasFoundForeground = True

                if display:
                    disImg[row, col] = [128, 128, 128, 255]

    if display:
        cv2.imshow("whitespace", disImg)
        cv2.waitKey(0)

<<<<<<< HEAD
    logo.attributes["Percent Whitespace"] = horizontalWhitespace/totalCountedPixels

=======
    logo.attributes["Percent Whitespace"] = horizontalWhitespace/totalCountedPixels * 100
    
>>>>>>> f735ce031d5db86292f82ffb6a85d7f1478f10a5
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
def percentBlackWhiteColor(logo, display):
    img = logo.img
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sumBlack = 0
    sumWhite = 0
    sumColor = 0
    for i in range(gray.shape[0]):
        for j in range(gray.shape[1]):
            if gray[i,j] <= 20:
                sumBlack += 1
            elif gray[i,j] >= 230:
                sumWhite += 1
            else:
                sumColor += 1
    Total = gray.shape[1]*gray.shape[0]
    percentBlack = sumBlack / Total * 100
    percentWhite = sumWhite / Total * 100
    percentColor = sumColor / Total * 100
    logo.attributes['% Black'] = percentBlack
    logo.attributes['% White'] = percentWhite
    logo.attributes['% Color'] = percentColor
#Add name of function to this array
ExportFunctions = [detectShapes, whitespace, colorfulness]

#Add name of function to this array if you want to test
<<<<<<< HEAD
TestFunctions = [percentBlackWhiteColor]
=======
TestFunctions = [detectShapes]
>>>>>>> f735ce031d5db86292f82ffb6a85d7f1478f10a5

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
