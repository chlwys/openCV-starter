#this code opens an image with openCV

#import openCV 
import cv2

#use openCV to read an image, store image as 'src'
src = cv2.imread("./tzj.jpg", cv2.IMREAD_ANYCOLOR)

#display image in a window
cv2.imshow("Image", src)
cv2.waitKey(0)
cv2.destroyAllWindows()
