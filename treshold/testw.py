import imutils
import numpy as np
import cv2


def nothing(x):
    pass


cv2.namedWindow("Trackbars")
cv2.createTrackbar("BLUR_ALPHA", "Trackbars", 0, 10, nothing)
cv2.createTrackbar("L - H - 1", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - S - 1", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V - 1", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H - 1", "Trackbars", 179, 255, nothing)
cv2.createTrackbar("U - S - 1", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V - 1", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("MASK_1", "Trackbars", 0, 1, nothing)
cv2.createTrackbar("MASK_2", "Trackbars", 0, 1, nothing)
cv2.createTrackbar("MASK_3", "Trackbars", 0, 1, nothing)
cv2.createTrackbar("KERNEL_SIZE", "Trackbars", 0, 10, nothing)
cv2.createTrackbar("ITERATIONS", "Trackbars", 1, 10, nothing)

cap = cv2.VideoCapture(0)


def hsv_values():
    return (
        cv2.getTrackbarPos("L - H - 1", "Trackbars"), cv2.getTrackbarPos("L - S - 1", "Trackbars"),
        cv2.getTrackbarPos("L - V - 1", "Trackbars"),
        cv2.getTrackbarPos("U - H - 1", "Trackbars"), cv2.getTrackbarPos("U - S - 1", "Trackbars"),
        cv2.getTrackbarPos("U - V - 1", "Trackbars"),
    )


def iterations():
    return cv2.getTrackbarPos("ITERATIONS", "Trackbars")


def masks():
    return (
        cv2.getTrackbarPos("MASK_1", "Trackbars"),
        cv2.getTrackbarPos("MASK_2", "Trackbars"),
        cv2.getTrackbarPos("MASK_3", "Trackbars")
    )


def kernel_size():
    val = cv2.getTrackbarPos("KERNEL_SIZE", "Trackbars")
    return np.ones((val, val), np.uint8)


while (True):
    # Capture frame-by-frame
    _, frame = cap.read()
    if frame is None:
        continue
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)

    # Our operations on the frame come here
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    l_h, l_s, l_v, u_h, u_s, u_v = hsv_values()
    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower, upper)

    m1, m2, m3 = masks()
    if m1 == 1:
        mask = cv2.erode(mask, None, iterations=iterations())
    if m2 == 2:
        mask = cv2.dilate(mask, None, iterations=iterations())
    if m3 == 3:
        mask = cv2.morphologyEx(mask, cv2.MORPH_ELLIPSE, kernel_size())
    # Display the resulting frame
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1.2, 100)
    if circles is not None:

        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(mask, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(mask, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    cv2.imshow('frame', mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
