import cv2
import numpy as np

image = cv2.imread("./IMAGE/5f.png")
img_fireman = cv2.imread("./IMAGE/fireman.png")
img_fireman = cv2.resize(img_fireman,(50,50))
print(image.ndim)
cv2.namedWindow("Image")
cv2.imshow("Image",image)
cv2.waitKey(0)
a=0
b=0
image[a:a+50,b:b+50] = img_fireman
cv2.imshow("Image",image)
cv2.waitKey(0)
cv2.destroyAllWindows()
