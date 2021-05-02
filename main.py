import mediapipe as mp
import PoseEstimationModule as pea
import numpy as np
import cv2
import win32api

dict_PoseAngle = {}
dict_PoseLength = {}
cap = cv2.VideoCapture(0)
count = 0
state = 0

with mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        _, frame = cap.read()
        white_img = cv2.imread('640x480-white-solid-color-background.jpg')

        image, white_img = pea.pose_estimation(frame, holistic, dict_PoseAngle, dict_PoseLength,  white_img)

        cv2.imshow('Cam Bg Pose Estimation', image)
        cv2.imshow('White Bg Pose Estimation', white_img)

        #스쿼트 횟수 측정
        if 0.4 <= dict_PoseLength['26, 24'] / dict_PoseLength['28, 26'] <= 0.8 \
                and 0.4 <= dict_PoseLength['25, 23'] / dict_PoseLength['27, 25'] <= 0.8:
            print("squat")
            if state != 1:
                state = 1
        elif 1.1 <= dict_PoseLength['26, 24'] / dict_PoseLength['28, 26'] \
                and 1.1 <= dict_PoseLength['25, 23'] / dict_PoseLength['27, 25']:
            if state != 0:
                state = 0
                count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        """if 60 <= dict_PoseAngle['RightElbow'] <= 130 and 60 <= dict_PoseAngle['LeftElbow'] <= 130:
                if 0.7 <= dict_PoseLength['11, 12'] / dict_PoseLength['11, 15'] <= 1.05 and\
                        0.7 <= dict_PoseLength['11, 12'] / dict_PoseLength['12, 16'] <= 1.05:
                    print('PushUp')"""

print(str(count))

cap.release()
cv2.destroyAllWindows()