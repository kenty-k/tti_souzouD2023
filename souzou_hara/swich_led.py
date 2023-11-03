'''
二つのスイッチを使用してLEDの明るさを調整する
'''

#必要なモジュールをインポート
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート

#ポート番号の定義
switch_up = 17                       #変数"switch_up"に17を代入
switch_down = 18                     #変数"switch_down"に18を代入
led_pin = 21                        #変数"Led_pin"に21を代入

#GPIOの設定
GPIO.setmode(GPIO.BCM)              #GPIOのモードを"GPIO.BCM"に設定
GPIO.setup(led_pin, GPIO.OUT)       #GPIO18を出力モードに設定
GPIO.setup(switch_up, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(switch_down, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

# #LEDの初期状態をオフに設定
# GPIO.output(led_pin,GPIO.LOW)

#初期の明るさ
duty_cycle = 50

def update_led_brightness():
    PWM_LED.ChangeDutyCycle(duty_cycle)
    #print(f"LEDの明るさを{duty_cycle}%に設定します")

try:
    PWM_LED = GPIO.PWM(led_pin, 1000)  # PWM周波数を設定
    PWM_LED.start(duty_cycle)

    while True:
        # 明るさを上げるスイッチが押されたらLEDの明るさを増加
        if GPIO.input(switch_up) == GPIO.LOW:
            duty_cycle += 10
            duty_cycle = min(duty_cycle, 100)  # 100%を超えないように制限
            update_led_brightness()
            time.sleep(0.2)  # スイッチのバウンスを考慮して短い待ち時間を入れる

        # 明るさを下げるスイッチが押されたらLEDの明るさを減少
        if GPIO.input(switch_down) == GPIO.LOW:
            duty_cycle -= 10
            duty_cycle = max(duty_cycle, 0)  # 0%未満にならないように制限
            update_led_brightness()
            time.sleep(0.2)  # スイッチのバウンスを考慮して短い待ち時間を入れる

        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()