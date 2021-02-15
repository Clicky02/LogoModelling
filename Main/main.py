import sys
from cv2 import cv2 
from os import listdir, path
import functions

TEST_MODE = False

#Main function for data Collection
def main():
    dir_path = path.dirname(path.realpath(__file__)) + "\\..\\Logos"

    for imgPath in listdir(dir_path):
        logo = Logo(cv2.imread(dir_path + imgPath, cv2.IMREAD_UNCHANGED), imgPath)
        
        for function in functions.ExportFunctions:
            function(logo, False)
        

#Test function to test individual features
def test():
    #Passes each logo into each function in the TestFunction array
    dir_path = path.dirname(path.realpath(__file__)) + "\\..\\TestLogos"

    for imgPath in listdir(dir_path):
        logo = Logo(cv2.imread(dir_path + imgPath, cv2.IMREAD_UNCHANGED), imgPath)

        for function in functions.TestFunctions:
            function(logo, False)

        print(logo.name)
        print(logo.attributes)

class Logo:
    def __init__(self, img, name):
        self.img = img
        self.name = name
        self.attributes = {}



if __name__ == "__main__":
    
    if TEST_MODE:
        test()
    else:
        main()
