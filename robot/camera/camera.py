import pickle
import struct
import cv2
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
        data = pickle.dumps(frame, 0)
        size = len(data)
        return struct.pack(">L", size) + data
