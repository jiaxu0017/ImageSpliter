import cv2

src = cv2.imread("PictureBooks\\img_17.jpg")
dst = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(dst, 127, 255, 0)
thresh = 255 - thresh
cv2.imshow("src", src)
cv2.imshow("thresh", thresh)
cv2.waitKey(0)
