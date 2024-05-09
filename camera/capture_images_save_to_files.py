from picamera2 import Picamera2
import time
import cv2
import os

# Initialize Picamera2
picam2 = Picamera2()
picam2.start_preview()  # Starting the preview without specifying the display method
picam2.start()

while True:
    timestamp = time.strftime("%S")
    filename = f"image_{timestamp}.jpg"
    filename2 = f"face_detected_image_{timestamp}.jpg"
    filename3 = f"rect_image_{timestamp}.jpg"
    picam2.capture_file(filename)

    image = cv2.imread(filename)

    # Convert the captured image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Load the cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(25, 25))
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imwrite(filename2, image)
        cv2.imwrite(filename3, image)

        time.sleep(1)
        os.remove(filename2)
