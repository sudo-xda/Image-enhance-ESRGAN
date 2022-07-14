import cv2
import numpy as np

image = cv2.imread('1.jpeg')
sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharpen = cv2.filter2D(image, -1, sharpen_kernel)
cv2.imwrite('sharp.png', sharpen)
cv2.waitKey()