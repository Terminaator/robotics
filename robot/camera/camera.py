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
        self.config_1.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 15)
        self.config_1.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 15)
        self.frame = None
        self.pipeline_1.start(self.config_1)

    def read(self):
        frames_1 = self.pipeline_1.wait_for_frames()
        color_frame_1 = frames_1.get_color_frame()
        color_image_1 = np.asanyarray(color_frame_1.get_data())
        _, frame = cv2.imencode('.jpg', color_image_1)

        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, np.array([69, 91, 41]), np.array([95, 255, 255]))
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        data = pickle.dumps(mask, 0)
        size = len(data)
        return struct.pack(">L", size) + data
