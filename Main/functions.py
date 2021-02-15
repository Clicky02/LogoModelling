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