# import openCV and numpy 
import cv2
import numpy as np

# use openCV to read an image, store image as 'src'
src = cv2.imread("tzj.jpg", cv2.IMREAD_ANYCOLOR)

'''
# canny edge detection without slider
edge = cv2.Canny(src, 100, 100, apertureSize=3, L2gradient=True)
cv2.imshow('canny', edge)
cv2.waitKey(0) '''

# tracker
# empty callback function for creating trackar
def callback(foo):
    pass

# create windows and trackbar
cv2.namedWindow('parameters')
cv2.createTrackbar('threshold1', 'parameters', 0, 255, callback)
cv2.createTrackbar('threshold2', 'parameters', 0, 255, callback)

while(True):
    # get threshold value from trackbar
    th1 = cv2.getTrackbarPos('threshold1', 'parameters')
    th2 = cv2.getTrackbarPos('threshold2', 'parameters')

    # blur to remove noise
    blurred = cv2.bilateralFilter(src, 7, 100, 100)
    
    # edge detection
    edge = cv2.Canny(src, th1, th2, apertureSize=3, L2gradient=True)
    cv2.imshow('canny', edge)
    
    # press q to exit
    if cv2.waitKey(1)&0xFF == ord('q'):
        break
        
cv2.destroyAllWindows()
