import cv2
import dlib
import imutils
from imutils import face_utils
import numpy as np
import glob

# Load the face detector and predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Functions to calculate lengths
def calcLength(pointA, pointB):
    return np.linalg.norm(np.array(pointA) - np.array(pointB))

def func_drowsiness_ratio(frame, landmarks):
    # Ratio of how open the mouth is
    upper_lip_top = (landmarks.part(51).x, landmarks.part(51).y)
    lower_lip_bottom = (landmarks.part(57).x, landmarks.part(57).y)
    lip_left = (landmarks.part(48).x, landmarks.part(48).y)
    lip_right = (landmarks.part(54).x, landmarks.part(54).y)

    lip_vert_line_length = calcLength(upper_lip_top, lower_lip_bottom)
    lip_hor_line_length = calcLength(lip_left, lip_right)

    # Ratio of horizontal to vertical length
    drowsiness_ratio = (lip_hor_line_length / lip_vert_line_length)
    return drowsiness_ratio

# Define indices for eyes
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# List of image paths
image_paths = glob.glob("rect_*.jpg")

# Loop through each image
for image_path in image_paths:
    frame = cv2.imread(image_path)
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    subjects = detector(gray, 2)
    #print("Processing image:", image_path)

    for subject in subjects:
        shape = predictor(gray, subject)
        shape = face_utils.shape_to_np(shape)  # Converting to NumPy Array
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]

        # Calculate the mouth drowsiness ratio
        drowsiness_ratio = func_drowsiness_ratio(frame, predictor(gray, subject))

        print("Processing image:", image_path)
        print(f"Drowsiness Ratio: {drowsiness_ratio}")
