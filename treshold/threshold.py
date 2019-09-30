import cv2
import numpy as np
import pyrealsense2 as rs


def nothing(x):
    pass


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
pipeline_1 = rs.pipeline()
config = rs.config()
config.enable_device('801212070130')
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline_1.start(config)
while True:
    frames = pipeline_1.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    color_image = np.asanyarray(color_frame.get_data())
    hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
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

    cv2.imshow("mask", mask)
    key = cv2.waitKey(1)
    if key == 27:
        break
