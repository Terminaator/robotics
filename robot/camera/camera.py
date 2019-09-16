import pickle
import struct
import cv2
import numpy as np


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.frame = None

    def read(self):
        _, self.frame = self.cap.read()
        _, frame = cv2.imencode('.jpg', self.frame)
        data = pickle.dumps(frame, 0)
        size = len(data)
        return struct.pack(">L", size) + data

    def mask(self, frame):
        img = np.flip(frame, axis=1)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        return cv2.inRange(hsv, np.array([0, 120, 70]), np.array([10, 255, 255])) + cv2.inRange(hsv, np.array(
            [170, 120, 70]), np.array([180, 255, 255]))
