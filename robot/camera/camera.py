import pickle
import struct
import cv2


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.frame = None

    def read(self):
        _, self.frame = self.cap.read()
        result, frame = cv2.imencode('.jpg', self.frame)
        data = pickle.dumps(frame, 0)
        size = len(data)
        return struct.pack(">L", size) + data
