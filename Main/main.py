import sys
from cv2 import cv2 
from os import listdir, path
import numpy as np
import functions

TEST_MODE = True

#Main function for data Collection
def main(folderName="Logos", functionList=functions.ExportFunctions, debug=False):

    dir_path = path.dirname(path.realpath(__file__)) + "\\..\\"+folderName+"\\"

    logos = []

    for imgPath in listdir(dir_path):

        img = cv2.imread(dir_path + imgPath, cv2.IMREAD_UNCHANGED)

        if (len(img[0,0]) < 4): # If there is no alpha value
            img = AddAlphaChannel(img)
 
        logo = Logo(img, imgPath)
        
        for function in functionList:
            function(logo, False)  


        for function in functions.TestFunctions:
            function(logo, True)

        if debug:
            print(logo.name)
            print(logo.attributes)


        logos.append(logo)

class Logo:
    def __init__(self, img, name):
        self.img = img
        self.name = name
        self.attributes = {}

def AddAlphaChannel(img):
    b_channel, g_channel, r_channel = cv2.split(img)
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
    return img_BGRA
    

if __name__ == "__main__":
    
    if TEST_MODE:
        main("TestLogos", functions.TestFunctions, True)
    else:
        main()
