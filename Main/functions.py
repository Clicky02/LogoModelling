from cv2 import cv2 


def testFunction(logo, display):
    img = logo.img
    # Do stuff with img here
    logo.attributes["Average Saturation"] = 10
    print(10)

#Add name of function to this array
ExportFunctions = [testFunction]

#Add name of function to this array if you want to test
TestFunctions = [testFunction]