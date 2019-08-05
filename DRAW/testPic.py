import cv2
import numpy as np

image = cv2.imread("../IMAGE/1Fpdf_image.png",cv2.IMREAD_GRAYSCALE)
cv2.namedWindow("Image",cv2.WINDOW_NORMAL)
canny = cv2.Canny(image,100,150)
cv2.imshow("Image",canny)
cv2.waitKey(0)
cv2.destroyWindow("Image")



