import cv2
import numpy as np


def nothing(x):
    pass


cap = cv2.VideoCapture(0)
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

cv2.createTrackbar("L - H - 2", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S - 2", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V - 2", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H - 2", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S - 2", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V - 2", "Trackbars", 255, 255, nothing)
while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    l_h_2 = cv2.getTrackbarPos("L - H - 2", "Trackbars")
    l_s_2 = cv2.getTrackbarPos("L - S - 2", "Trackbars")
    l_v_2 = cv2.getTrackbarPos("L - V - 2", "Trackbars")
    u_h_2 = cv2.getTrackbarPos("U - H - 2", "Trackbars")
    u_s_2 = cv2.getTrackbarPos("U - S - 2", "Trackbars")
    u_v_2 = cv2.getTrackbarPos("U - V - 2", "Trackbars")
    lower_blue_1 = np.array([l_h, l_s, l_v])
    upper_blue_1 = np.array([u_h, u_s, u_v])
    lower_blue_2 = np.array([l_h_2, l_s_2, l_v_2])
    upper_blue_2 = np.array([u_h_2, u_s_2, u_v_2])
    mask = cv2.inRange(hsv, lower_blue_1, upper_blue_1) + cv2.inRange(hsv, lower_blue_2, upper_blue_2)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    #cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    #cv2.imshow("result", result)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
