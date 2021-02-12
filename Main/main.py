import sys
from cv2 import cv2 
from os import listdir
import functions as functions

TEST_MODE = True

def main():
    for imgPath in listdir('Logos/'):
        logo = Logo(cv2.imread('Logos/' + imgPath, cv2.IMREAD_UNCHANGED), imgPath)
        
        for function in functions.ExportFunctions:
            function(logo, False)

def test():
    for imgPath in listdir('TestLogos/'):
        logo = Logo(cv2.imread('TestLogos/' + imgPath, cv2.IMREAD_UNCHANGED), imgPath)

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