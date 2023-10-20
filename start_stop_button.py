import RPi.GPIO as GPIO
import time

# GPIOピン番号
button_pin = 17

# GPIO設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ボタンが押された回数を記録する変数
button_press_count = 0
print("Hello world!")

# startからstopまでの時間を記録する変数
start_time = None

try:
    while True:
        # ボタンの状態を監視
        button_state = GPIO.input(button_pin)
        
        # ボタンが押された場合
        if button_state == GPIO.LOW:
            print("ボタンが押されました")
            button_press_count += 1
            
            # ボタンが奇数回押された場合
            if button_press_count % 2 == 1:
                start_time = time.time()
                print("start ボタンが押されました")
            
            # ボタンが偶数回押された場合
            else:
                if start_time is not None:
                    stop_time = time.time()
                    elapsed_time = stop_time - start_time
                    print(f"stop ボタンが押されました\n経過時間: {elapsed_time}秒")
                    start_time = None
            
        # 一時的なディレイ
        time.sleep(0.2)

except KeyboardInterrupt:
    pass

# GPIO設定のクリーンアップ
GPIO.cleanup()

