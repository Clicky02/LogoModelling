from cv2 import cv2 as cv

img = cv.imread('Opencv/cb.jpg')

cv.imshow('Boop my nose', img)

# Converting to grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

cv.imshow('Gray Boop my nose', gray)

cv.waitKey(0)

# Blur (uses GaussianBlur, there exists many different types of blur)
# (7,7) is the kernel size of the blur, decrease to suppose (3,3) to reduce blur. but both must be positive, odd and equal to each other.
blur = cv.GaussianBlur (img, (7,7), cv.BORDER_DEFAULT)

cv.imshow('BLURRED', blur)

cv.waitKey(0)

# Edge Cascade
canny = cv.Canny(img, 125, 175)
cv.imshow ('Canny Edges', canny)

# to reduce number of edges pass in a blurred image as an arguement,
# to get rid of lesser edges apply less blur to blur
# canny = cv.Canny(blur, 125, 175)
# cv.imshow ('Canny Edges', canny)

cv.waitKey(0)

# Dilating the image (dilates an image using a specific structuring element)
# One such structuring element is the canny image (which has the edges detected)
# increasing kernel size (7,7) can add more dilation
# incresing iteration can add thicker edges
dilated = cv.dilate(canny, (7,7), iterations=3)
cv.imshow('dilated', dilated)

cv.waitKey(0)

# Eroding
eroded = cv.erode(dilated, (7,7), iterations=3)
cv.imshow('Erosion', eroded)

cv.waitKey(0)

# Resize 
# To shrink an image, it will generally look best with #INTER_AREA interpolation, whereas to
# enlarge an image, it will generally look best with c#INTER_CUBIC (slow, higher quality) or #INTER_LINEAR (fast, lower quality)
resized = cv.resize(img, (500,500), interpolation=cv.INTER_AREA)
cv.imshow('resized', resized)

cv.waitKey(0)

# Cropping
cropped = img[50:200, 200:400]
cv.imshow('Cropped', cropped)

cv. waitKey(0)

