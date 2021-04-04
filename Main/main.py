import sys
from cv2 import cv2
from os import listdir, path
import numpy as np
import functions
import utils
import xlsxwriter
import shutil
import os
from cairosvg import svg2png
from PIL import Image
from io import BytesIO

TEST_MODE = False

#Main function for data Collection
def main(folderName="500Logos", functionList=functions.ExportFunctions, debug=False):

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
            origImg, img = AddAlphaChannel(img)



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

class Logo:
    def __init__(self, img, originalImg, name):
        self.img = img
        self.originalImg = originalImg
        self.name = name
        self.attributes = {}

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

def exportToExcel(logos):
    #There must be at least one logo
    assert(len(logos) > 0)
    
    workbook = xlsxwriter.Workbook('LogoDataNew.xlsx')
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})

    #Create Header Row
    worksheet.write(0, 0, "Company Name", bold)
    worksheet.write(0, 1, "Start Year", bold)
    worksheet.write(0, 2, "End Year", bold)

    col = 3
    for key in logos[0].attributes:
        worksheet.write(0, col, key, bold)
        col += 1

    #Increase width of columns
    worksheet.set_column(0, col, 20)
    
    #Fill in the data for all other logos
    row = 1
    for logo in logos:
        try:
            logoDescriptors = logo.name.split(".")[0].split("_")

            worksheet.write(row, 0, logoDescriptors[0]) #Company Name
            worksheet.write(row, 1, logoDescriptors[1]) #Logo Start Year
            worksheet.write(row, 2, logoDescriptors[2]) #Logo End Year

            col = 3
            for key in logos[0].attributes:
                worksheet.write(row, col, str(logo.attributes[key]))
                col += 1
            row += 1
        except:
            print("\nWriting to excel failed for " + logo.name + ".")
            print("Check and see if the name is formatted correctly.\n")

    workbook.close()

def printProgressBar(iteration, total):
    percentFilled = iteration / total
    amountFilled = int(30 * percentFilled)
    amountEmpty = 30 - amountFilled
    print(f"  {percentFilled*100:.1f}% [" + ("█" * amountFilled) + ("-" * amountEmpty) + "]", end = '\r')

def clearConsoleLine():
    print('\r                                                                         ', end = '\r')

if __name__ == "__main__":
    
    if TEST_MODE:
        main("TestLogos", functions.TestFunctions, True)
    else:
        main()
