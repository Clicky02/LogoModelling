from cv2 import cv2
from os import listdir, path
import numpy as np
import logo_processing
import utils
import os
from cairosvg import svg2png
from PIL import Image
from io import BytesIO
from excel import exportToExcel
from logo import Logo

TEST_MODE = False

#Main function for data Collection
def main(folderName="500Logos", functionList=logo_processing.ExportFunctions, debug=False):

    # Gets path to the directory holding the logos
    dir_path = os.path.join(path.dirname(path.realpath(__file__)), "..\\"+folderName+"\\")

    logos = []

    i = 0
    totalLogos = len(listdir(dir_path))
    for imgPath in listdir(dir_path):

        extension = imgPath.split('.')[-1]

        if extension != "svg":
            img = cv2.imread(dir_path + imgPath, cv2.IMREAD_UNCHANGED)
        else:
            svgFile = open(dir_path + imgPath, mode='r')
            svgContent = svgFile.read()
            svgFile.close()
            try:
                png = svg2png(svgContent)
                                
                pil_img = Image.open(BytesIO(png)).convert('RGBA')
                
                img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGBA2BGRA)

            except:
                print("SVG Failed to load " + imgPath + ".\n")
                continue

        #Do not try to load directories
        if os.path.isdir(dir_path + imgPath):  
            continue
        
        #Handle images not loading
        if img is None:
            clearConsoleLine()
            print("Failed to load " + imgPath + ".\n")
            continue
        
        #Converts grayscale to color images
        if not(isinstance(img[0,0], np.ndarray)):
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        #Casts images to uint8 if necessary so all opencv functions work on them
        if (img.dtype != "uint8"):
            img = img.astype('uint8')

        origImg = img

        #Converts BGR images to BGRA images with the background removed
        if (len(img[0,0]) < 4): 
            origImg, img = utils.AddAlphaChannel(img)



        img[np.where(cv2.split(img)[3] == 0)] = [0,0,0,0] #Enforce fully transparent pixels

        logo = Logo(img, origImg, imgPath)
        
        for function in functionList:
            try:
                function(logo, False) 

            except Exception as e:
                clearConsoleLine()
                print("\nFunction Failed") 
                print("Logo: " + logo.name)
                print("Function: " + function.__name__)
                print("Exception: " + str(e))

        if debug:
            clearConsoleLine()
            print(logo.name)
            print(logo.attributes)

        logos.append(logo)

        printProgressBar(i, totalLogos)
        i += 1

    clearConsoleLine()
    print("Exporting to Excel...\n")

    exportToExcel(logos)

    print("Finished\n")

def printProgressBar(iteration, total):
    percentFilled = iteration / total
    amountFilled = int(30 * percentFilled)
    amountEmpty = 30 - amountFilled
    print(f"  {percentFilled*100:.1f}% [" + ("█" * amountFilled) + ("-" * amountEmpty) + "]", end = '\r')

def clearConsoleLine():
    print('\r                                                                         ', end = '\r')


if __name__ == "__main__": 
    if TEST_MODE:
        main("TestLogos", logo_processing.TestFunctions, True)
    else:
        main()
