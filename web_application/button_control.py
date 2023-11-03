import RPi.GPIO as GPIO
import time
from database_operations import record_study_time

# GPIOピン番号
button_pin = 18

# GPIO設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ボタンが押された回数を記録する変数
button_press_count = 0
start_time = None

def handle_button_press():
    global button_press_count
    global start_time

    button_state = GPIO.input(button_pin)

    if button_state == GPIO.LOW:
        button_press_count += 1

        if button_press_count % 2 == 1:
            start_time = time.time()
            return "start"

        else:
            if start_time is not None:
                stop_time = time.time()
                elapsed_time = stop_time - start_time
                record_study_time(start_time, stop_time, elapsed_time)
                start_time = None
                return f"stop ({elapsed_time}秒)"
