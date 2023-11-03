from buildhat import Motor

motor = Motor('A')

try:
    # モーターを3回転させる
    motor.run_for_rotations(3)
    # モーターが終了するまで待つ
    motor.wait_until_not_moving()

    # モーターを逆方向に3回転させる
    motor.run_for_rotations(-3)
    # モーターが終了するまで待つ
    motor.wait_until_not_moving()

except KeyboardInterrupt:
    # Ctrl+Cが押された場合はモーターを停止
    motor.stop()
