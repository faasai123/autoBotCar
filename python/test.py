import time
from datetime import datetime
from buildhat import Motor

# saves logs to cronlog in system
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Hello")
print("Latest login =",current_time)

# basic motor function for visual proof that program is actually run on startup
motorA = Motor('A')
motorB = Motor('B')
motorA.set_default_speed(-100)
motorB.set_default_speed(100)
motorA.run_for_seconds(1, blocking=False)
motorB.run_for_seconds(1, blocking=False)
time.sleep(3)
