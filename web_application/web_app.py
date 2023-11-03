from flask import Flask, render_template, request, jsonify
import time
from database_operations import create_table, record_study_time, get_latest_records, get_latest_elapsedtimes
from button_control import handle_button_press

app = Flask(__name__)

# メインページ
@app.route('/')
def index():
    data = get_latest_elapsedtimes(limit=5)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    create_table()
    app.run(debug=True, host='0.0.0.0')

