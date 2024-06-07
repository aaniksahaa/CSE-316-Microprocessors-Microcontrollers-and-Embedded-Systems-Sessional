import cv2
import numpy as np

img = cv2.imread('images/1.png')
# image_float = img.astype(np.float32)

# darkened_image = image_float * 0.5
# darkened_image = np.clip(darkened_image, 0, 255)
# darkened_image = darkened_image.astype(np.uint8)

# img = darkened_image
kernel = np.ones((5, 5), np.uint8)


# img = cv2.erode(img, kernel, iterations=3)

hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * 1, 0, 255)
img = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

# img = cv2.GaussianBlur(img, (15,15), 0)
img = cv2.dilate(img, kernel, iterations=1)

cv2.imshow('name', img)
cv2.waitKey(0)