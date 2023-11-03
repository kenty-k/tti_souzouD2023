'''
ボタン入力->モータ回転(順方向)->LED消灯->モータ回転(逆回転)
'''

import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート[
from buildhat import Motor          #LEGOモーターを制御するためのライブラリをインポート
import time                         #時間制御用のモジュールをインポート
import sys 

motor = Motor('A')

switch_motor = 22                    #変数""switch_motor"に22を代入
led_pin = 21                         #変数"led_pin"に21を代入

#GPIOの設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin,GPIO.OUT)
GPIO.setup(switch_motor,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#LEDの初期状態をオンに設定

GPIO.output(led_pin,GPIO.OUT)

try:
    if GPIO.input(switch_motor) == GPIO.LOW:
        motor.run_for_rotations(2) # モーターを2回転
    # モーターの動作が完了するまで待つ
    while motor.is_running():
        time.sleep(0.1)
    
    #LEDを消灯する
    GPIO.output(led_pin,GPIO.LOW)

    #モーターを逆回転させる
    motor.run_for_rotations(-2)

    #モーターの動作が完了するまで待つ
    while motor.is_running():
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
    motor.stop()