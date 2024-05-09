from picamera2 import Picamera2
import time
import cv2
import os
import serial
from scipy.spatial import distance
import dlib
import imutils
from imutils import face_utils
import numpy as np
import glob

# init
picam2 = Picamera2()
picam2.start_preview()  # Starting the preview without specifying the display method
serial_port = "/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_75131313632351905081-if00"  # Change this to match your serial port
ser = serial.Serial(serial_port, 9600)
time.sleep(0.1)
ser.close()
ser.open()

picam2.start()

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
thresh = 0.3

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def calcLength(pointA, pointB):
    return np.linalg.norm(np.array(pointA) - np.array(pointB))

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

while True:
    timestamp = time.strftime("%S")
    filename = f"image_{timestamp}.jpg"
    filename2 = f"rect_image_{timestamp}.jpg"
    picam2.capture_file(filename)

    image = cv2.imread(filename)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    subjects = detector(gray, 2)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1, minSize=(10, 10))
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imwrite(filename2, image)
        time.sleep(4)
        os.remove(filename2)

    flag = 0
    for subject in subjects:
        shape = predictor(gray, subject)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(image, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(image, [rightEyeHull], -1, (0, 255, 0), 1)

        if ear < thresh:
            flag += 1
            d = "0\n"
            ser.write(d.encode())
            time.sleep(2)
            dp = "0\n"
            ser.write(dp.encode())
            print("Pull over!, driver may be drowsy")
        else:
            d_ = "1\n"
            ser.write(d_.encode())
            print("Driver is not drowsy")
