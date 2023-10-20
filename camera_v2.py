import cv2
import time
from aiy.pins import (PIN_A, PIN_B)
from aiy.motor import Motor

# 顔と目を検出するためのカスケード分類器をロード
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# モーターの初期設定
motor = Motor(PIN_A)

def start_motor():
    """モーターを動かす関数"""
    motor.set_speed(50)  # 50%の速度でモーターを回転

def stop_motor():
    """モーターを停止する関数"""
    motor.set_speed(0)  # モーターを停止

# ウェブカメラのビデオキャプチャを開始
cap = cv2.VideoCapture(0)

# 眠っているかどうかを判断するための変数
sleep_start_time = None
sleep_detected = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)  # 顔を囲む
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(frame, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (0, 255, 0), 2)  # 目を囲む

        if len(eyes) >= 2:
            sleep_start_time = None
            if sleep_detected:
                print("User woke up!")
                stop_motor()
                sleep_detected = False
        else:
            if sleep_start_time is None:
                sleep_start_time = time.time()
            elif time.time() - sleep_start_time > 5:
                if not sleep_detected:
                    print("User is sleeping!")
                    start_motor()
                    sleep_detected = True

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
