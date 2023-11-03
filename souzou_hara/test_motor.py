'''
モーターを回転させるためだけのプログラム
'''

from buildhat import Motor
import time

motor = Motor('A')

try:
    motor.run_for_rotations(3)

    while motor.is_running():
        time.sleep(0.1)

    motor.run_for_rotations(-3)

    while motor.is_running():
        time.sleep(0.1)

except KeyboardInterrupt:

    motor.stop()
