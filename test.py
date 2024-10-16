import cv2 

img = cv2.imread('test.webp') 
cv2.imshow('Test', img) 

img_canny = cv2.Canny(img, 100, 150) 
cv2.imshow('Test img Edge', img_canny) 

cv2.waitKey(0) 
cv2.destroyAllWindows() 
