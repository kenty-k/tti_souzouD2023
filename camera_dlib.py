import cv2
import time
import dlib
import RPi.GPIO as GPIO

# モデルの初期化
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# GPIOピンの設定
MOTOR_PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PIN, GPIO.OUT)
motor = GPIO.PWM(MOTOR_PIN, 100)
motor.start(0)

def start_motor():
    motor.ChangeDutyCycle(50)

def stop_motor():
    motor.ChangeDutyCycle(0)

cap = cv2.VideoCapture(0)

sleep_start_time = None
sleep_detected = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        x, y, w, h = (face.left(), face.top(), face.width(), face.height())
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        landmarks = predictor(gray, face)
        left_eye = landmarks.parts()[36:42]
        right_eye = landmarks.parts()[42:48]

        cv2.polylines(frame, [[(point.x, point.y) for point in left_eye]], True, (0, 255, 0), 2)
        cv2.polylines(frame, [[(point.x, point.y) for point in right_eye]], True, (0, 255, 0), 2)

        if len(faces) > 0 and (not left_eye or not right_eye):
            if sleep_start_time is None:
                sleep_start_time = time.time()
            elif time.time() - sleep_start_time > 5:
                if not sleep_detected:
                    print("User is sleeping!")
                    start_motor()
                    sleep_detected = True
        else:
            sleep_start_time = None
            if sleep_detected:
                print("User woke up!")
                stop_motor()
                sleep_detected = False

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
motor.stop()
GPIO.cleanup()
