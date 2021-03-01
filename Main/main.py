import sys
from cv2 import cv2 
from os import listdir, path
import numpy as np
import functions
import utils
import xlsxwriter

TEST_MODE = True

#Main function for data Collection
def main(folderName="Logos", functionList=functions.ExportFunctions, debug=False):

    dir_path = path.dirname(path.realpath(__file__)) + "\\..\\"+folderName+"\\"

    logos = []

    for imgPath in listdir(dir_path):

        img = cv2.imread(dir_path + imgPath, cv2.IMREAD_UNCHANGED)

        if (len(img[0,0]) < 4): # If there is no alpha value
            img = AddAlphaChannel(img)
            
        bImg = utils.AddBorder(img, [0,0,0,0])
 
        logo = Logo(img, bImg, imgPath)
        
        for function in functionList:
            function(logo, True)  

        if debug:
            print(logo.name)
            print(logo.attributes)

        logos.append(logo)
    
    exportToExcel(logos)

class Logo:
    def __init__(self, img, borderedImg, name):
        self.img = img
        self.borderedImg = img
        self.name = name
        self.attributes = {}

def AddAlphaChannel(img):
    b_channel, g_channel, r_channel = cv2.split(img)
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

    backColor = utils.GetBackground(img)

    if backColor == [0,0,0] or backColor == [255,255,255]:
        img_BGRA = utils.removeColor(img_BGRA, backColor)

    return img_BGRA

def exportToExcel(logos):
    #There must be at least one logo
    assert(len(logos) > 0)

    workbook = xlsxwriter.Workbook('LogoData.xlsx')
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})

    #Create Header Row
    worksheet.write(0, 0, "Company Name", bold)
    worksheet.write(0, 1, "Start Year", bold)
    worksheet.write(0, 2, "End Year", bold)

    column = 3
    for key in logos[0].attributes:
        worksheet.write(0, column, key, bold)
        column += 1

    #Increase width of columns
    worksheet.set_column(0, column, 20)
    
    #Fill in the data for all other logos
    row = 1
    for logo in logos:

        logoDescriptors = logo.name.split(".")[0].split("_")

        worksheet.write(row, 0, logoDescriptors[0]) #Company Name
        worksheet.write(row, 1, logoDescriptors[1]) #Logo Start Year
        worksheet.write(row, 2, logoDescriptors[2]) #Logo End Year

        column = 3
        for key in logos[0].attributes:
            worksheet.write(row, column, str(logos[0].attributes[key]))
            column += 1
        row += 1

    workbook.close()


if __name__ == "__main__":
    
    if TEST_MODE:
        main("TestLogos", functions.TestFunctions, True)
    else:
        main()
