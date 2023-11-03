import sqlite3

# データベースに接続
def connect_to_database():
    conn = sqlite3.connect('study_time.db')  # データベースファイル名を指定
    return conn

# テーブルを作成
def create_table():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS study_records (
            id INTEGER PRIMARY KEY,
            start_time DATETIME,
            stop_time DATETIME,
            elapsed_time REAL
        )
    ''')
    conn.commit()
    conn.close()

# 勉強時間を記録
def record_study_time(start_time, stop_time, elapsed_time):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO study_records (start_time, stop_time, elapsed_time)
        VALUES (?, ?, ?)
    ''', (start_time, stop_time, elapsed_time))
    conn.commit()
    conn.close()

# 最新の5つの記録を取得
def get_latest_records(limit=5):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM study_records
        ORDER BY id DESC
        LIMIT ?
    ''', (limit,))
    records = cursor.fetchall()
    conn.close()
    return records

if __name__ == '__main__':
    create_table()
