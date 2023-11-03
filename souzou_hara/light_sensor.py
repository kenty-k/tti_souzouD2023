'''
カメラを光センサのように使用して周囲の明るさを検出してLEDの明るさを制御するプログラム
'''
import RPi.GPIO as GPIO
import cv2
import numpy as np
import time

# GPIOのモードをBCMに設定
GPIO.setmode(GPIO.BCM)

# 使用するピンの設定
led_pin = 21  # LEDの制御ピン（このピンは必要に応じて変更してください）

# ピンのセットアップ
GPIO.setup(led_pin, GPIO.OUT)

# # LEDの初期状態をオフに設定
# GPIO.output(led_pin, GPIO.LOW)

# カメラの初期化
cap = cv2.VideoCapture(0)  # 0はデフォルトのカメラを指定

duty_cycle = 0
pre_brightness = 0

flag = 1

def update_led_brightness():
    #現在の明るさと前回の明るさの差を計算
    global flag
    judge = abs(pre_brightness - duty_cycle)

    if (flag == 1 or judge >= 30):
        PWM_LED.ChangeDutyCycle(duty_cycle)
        pre_brightness = duty_cycle
        flag = 0
    #print(f"LEDの明るさを{duty_cycle}%に設定します")


try:
    PWM_LED = GPIO.PWM(led_pin, 1000)  # PWM周波数を設定
    PWM_LED.start(duty_cycle)

    while True:
        ret, frame = cap.read()  # カメラからフレームを取得
        if not ret:
            continue

        # フレームの明るさを評価
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray_frame)

        # 明るさに応じてLEDの明るさを設定(0：暗い,255:明るい)
        duty_cycle = 100 - int(brightness / 2.55)  # 0-100の範囲に変換
        update_led_brightness()
        time.sleep(0.1)

        #print(f"明るさ: {brightness:.2f}, LEDの明るさ: {duty_cycle}%")

except KeyboardInterrupt:
    cap.release()
    GPIO.cleanup()
