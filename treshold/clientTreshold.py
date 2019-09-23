import argparse
import pickle
import socket
import struct
from collections import deque

import cv2
import imutils
import numpy as np


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 6001))
data = b""
payload_size = struct.calcsize(">L")
cap = cv2.VideoCapture(0)
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")

args = vars(ap.parse_args())
pts = deque(maxlen=args["buffer"])
while True:
    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        data += s.recv(4096)
    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += s.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")

    algus = cv2.imdecode(frame, cv2.COLOR_BGR2HSV)



    cv2.imshow('ImageWindow', algus)
    cv2.waitKey(1)