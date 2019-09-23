import pickle
import struct
import cv2
import imutils
import numpy as np
import pyrealsense2 as rs

class Camera:
    def __init__(self):
        self.pipeline_1 = rs.pipeline()
        self.config_1 = rs.config()
        self.config_1.enable_device('801212070130')
        self.config_1.enable_stream(rs.stream.depth, 600, 600, rs.format.z16, 30)
        self.config_1.enable_stream(rs.stream.color, 600, 600, rs.format.rgb8, 30)
        self.frame = None
        self.pipeline_1.start(self.config_1)

    def read(self):
        frames_1 = self.pipeline_1.wait_for_frames()
        color_frame_1 = frames_1.get_color_frame()
        color_image_1 = np.asanyarray(color_frame_1.get_data())
        _, frame = cv2.imencode('.jpg', color_image_1)

        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, np.array([69, 91, 41]), np.array([95, 255, 255]))
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        return mask

came = Camera()
while True:
    cv2.imshow('frame',came.read())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break