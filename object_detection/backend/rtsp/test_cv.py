import cv2 as cv
import numpy as np

# print(f'CV Version: {cv2.__version__}')

test_image = cv.imread("simple-car.jpg", cv.IMREAD_GRAYSCALE)
cv.imshow("Test Image", test_image)
cv.waitKey(0)
cv.destroyAllWindows()
