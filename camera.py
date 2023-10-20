import cv2
import time
import dlib

# 顔と目を検出するためのカスケード分類器をロード
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

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

    # グレースケールに変換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 顔を検出
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # 顔領域を抽出
        roi_gray = gray[y:y+h, x:x+w]

        # 顔領域内で目を検出
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            sleep_start_time = None
            if sleep_detected:
                print("User woke up!")
                sleep_detected = False
        else:
            if sleep_start_time is None:
                sleep_start_time = time.time()
            elif time.time() - sleep_start_time > 5:  # ここで設定する時間（秒）が睡眠と判断する閾値
                if not sleep_detected:
                    print("User is sleeping!")
                    sleep_detected = True

    # ビデオストリームを表示
    cv2.imshow('Video', frame)

    # 'q'キーでループを終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ウェブカメラのビデオキャプチャを終了
cap.release()
cv2.destroyAllWindows()
