from flask import Flask, render_template, request, jsonify
import time
from database_operations import create_table, record_study_time, get_latest_records
from button_control import handle_button_press

app = Flask(__name__)

# メインページ
@app.route('/')
def index():
    latest_records = get_latest_records()
    return render_template('index.html', latest_records=latest_records)

# ボタンが押されたときの動作呼び出し
@app.route('/button_pressed', methods=['POST'])
def button_pressed():
    result = handle_button_press()
    return result

if __name__ == '__main__':
    create_table()
    app.run(debug=True, host='0.0.0.0')

