from flask import Flask, render_template, request, jsonify
import time
from database_operations import create_table, record_study_time, get_latest_records
import RPi.GPIO as GPIO

app = Flask(__name__)

# GPIOピン番号
button_pin = 17

# GPIO設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ボタンが押された回数を記録する変数
button_press_count = 0
start_time = None

# メインページ
@app.route('/')
def index():
    latest_records = get_latest_records()
    return render_template('index.html', latest_records=latest_records)

# ボタンが押されたときの動作
@app.route('/button_pressed', methods=['POST'])
def button_pressed():
    global button_press_count
    global start_time

    button_state = GPIO.input(button_pin)

    if button_state == GPIO.LOW:
        button_press_count += 1

        if button_press_count % 2 == 1:
            start_time = time.time()
            return "start"  # クライアントに"start"を返す

        else:
            if start_time is not None:
                stop_time = time.time()
                elapsed_time = stop_time - start_time
                record_study_time(start_time, stop_time, elapsed_time)
                start_time = None
                return f"stop ({elapsed_time}秒)"  # クライアントに"stop"と経過時間を返す

if __name__ == '__main__':
    create_table()
    app.run(debug=True, host='0.0.0.0')

