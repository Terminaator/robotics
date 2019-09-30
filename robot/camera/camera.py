import argparse
import pickle
import struct
from collections import deque

import cv2
import imutils
import numpy as np
import pyrealsense2 as rs
import serial

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")

args = vars(ap.parse_args())
pts = deque(maxlen=args["buffer"])


class SerialController:
    def __init__(self, ):
        self.ser = serial.Serial("/dev/ttyACM0")
        self.end = bytes([13, 10])
        if not self.ser.isOpen():
            raise Exception('Missing serials name')
        self.fail_safe("0")

    def fail_safe(self, b):
        self.ser.write(('fs:' + b).encode() + self.end)

    def move(self, speed):
        self.ser.write('d:3000'.encode() + self.end)

    def rotate(self):
        self.ser.write('sd:10:-10:0:0'.encode() + self.end)

    def stop(self):
        self.ser.write('sd:0:0:0:0'.encode() + self.end)

    def close(self):
        self.ser.close()


ser = SerialController()


class Camera:
    def __init__(self):
        self.pipeline_1 = rs.pipeline()
        self.config = rs.config()
        self.config.enable_device('801212070130')
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.frame = None
        self.pipeline_1.start(self.config)

    def read(self):
        frames = self.pipeline_1.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())

        frame = imutils.resize(color_image, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        mask = cv2.inRange(hsv, np.array([18, 81, 70]), np.array([73, 255, 240]))
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        # Stack both images horizontally
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)

            # only proceed if the radius meets a minimum size
            if radius > 5:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(color_image, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                ser.stop()
            else:
                ser.rotate()
        else:
            ser.rotate()
        for i in range(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
        return color_image


ctx = rs.context()
if len(ctx.devices) > 0:
    for d in ctx.devices:
        print('Found device: ',
              d.get_info(rs.camera_info.name), ' ',
              d.get_info(rs.camera_info.serial_number))
else:
    print("No Intel Device connected")
came = Camera()
while True:
    cv2.imshow('frame', came.read())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
