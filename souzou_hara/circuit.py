'''
3つのプログラムを統合
1.スイッチで明るさ調整した場合は指定した時間内は自動調整機能はオフ
'''
#必要なモジュールをインポート
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
from buildhat import Motor            #LEGOモーターを制御するためのライブラリをインポート
import cv2                          
import numpy as np
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート

motor = Motor('A')

#ポート番号の定義
switch_up = 17                       #変数"switch_up"に17を代入
switch_down = 18                     #変数"switch_down"に18を代入
led_pin = 21                        #変数"Led_pin"に21を代入
switch_motor = 22                    #変数""switch_motor"に22を代入

#GPIOの設定
GPIO.setmode(GPIO.BCM)              #GPIOのモードを"GPIO.BCM"に設定
GPIO.setup(led_pin, GPIO.OUT)       #GPIO18を出力モードに設定
GPIO.setup(switch_up, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(switch_down, GPIO.IN,pull_up_down=GPIO.PUD_UP) 
GPIO.setup(switch_motor,GPIO.IN,pull_up_down=GPIO.PUD_UP)


# #LEDの初期状態をオフに設定
# GPIO.output(led_pin,GPIO.LOW)

#初期の明るさ
duty_cycle = 50
pre_brightness = 0
cap = cv2.VideoCapture(0)  # 0はデフォルトのカメラを指定
flag = 1

duration = 60                       #自動調整機能をオフにする時間
rotation_num = 2

start = time.time()

def update_led_brightness():
    global start
    global flag
    PWM_LED.ChangeDutyCycle(duty_cycle)
    start = time.time()
    flag = 0
    #print(f"LEDの明るさを{duty_cycle}%に設定します")

def update_auto_led_brightness():
    #現在の明るさと前回の明るさの差を計算
    judge = abs(pre_brightness - duty_cycle)
    # 明るさの変化が30以上だと電圧を変化させる
    if (judge >= 30):
        PWM_LED.ChangeDutyCycle(duty_cycle)
        pre_brightness = duty_cycle

    #print(f"LEDの明るさを{duty_cycle}%に設定します")

def auto_brightness():
    global duty_cycle

    while True:
        ret,frame = cap.read()
        if ret:
            break

    # フレームの明るさを評価
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray_frame)

    # 明るさに応じてLEDの明るさを設定(0：暗い,255:明るい)
    duty_cycle = 100 - int(brightness / 2.55)  # 0-100の範囲に変換
    update_auto_led_brightness()
    time.sleep(0.1)

    #print(f"明るさ: {brightness:.2f}, LEDの明るさ: {duty_cycle}%")

def motor_drive():
    global duty_cycle

    motor.run_for_rotations(rotation_num)
    while motor.is_running():
        time.sleep(0.1)
    
    duty_cycle = 0
    PWM_LED.ChangeDutyCycle(duty_cycle)
    motor.run_for_rotations(-1*rotation_num)

try:
    PWM_LED = GPIO.PWM(led_pin, 1000)  # PWM周波数を設定
    PWM_LED.start(duty_cycle)

    while True:
        # GPIO.wait_for_edge(18, GPIO.FALLING)
        if GPIO.wait_for_edge(switch_motor,GPIO.FALLING):
            pass

        # 明るさを上げるスイッチが押されたらLEDの明るさを増加
        if GPIO.wait_for_edge(switch_up,GPIO.FALLING):
            duty_cycle += 10
            duty_cycle = min(duty_cycle, 100)  # 100%を超えないように制限
            update_led_brightness()
            time.sleep(0.2)  # スイッチのバウンスを考慮して短い待ち時間を入れる

        # 明るさを下げるスイッチが押されたらLEDの明るさを減少
        if GPIO.wait_for_edge(switch_down,GPIO.FALLING):
            duty_cycle -= 10
            duty_cycle = max(duty_cycle, 0)  # 0%未満にならないように制限
            update_led_brightness()
            time.sleep(0.2)  # スイッチのバウンスを考慮して短い待ち時間を入れる
        
        if (time.time() - start) >= duration:
            auto_brightness()

        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()