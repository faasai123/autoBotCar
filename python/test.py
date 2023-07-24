import time
from datetime import datetime
from buildhat import Motor, Hat

def until_finds_hat(t):
    try:
        return Hat()
    except:
        if(t>0):
            time.sleep(1)
            return until_finds_hat(t-1)
        else:
            return False

# saves logs to cronlog in system
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Hello")
print("Latest login =",current_time)

# recursive function to wait for hat to be connected
if until_finds_hat(30) is not None: # set maximum find time to 30 seconds
    # basic motor function for visual proof that program is actually run on startup
    try:
        time.sleep(10)
        motorA = Motor('A')
        motorB = Motor('B')
        motorA.set_default_speed(-100)
        motorB.set_default_speed(100)
        motorA.run_for_seconds(1, blocking=False)
        motorB.run_for_seconds(1, blocking=False)
        time.sleep(3)
    except:
        print("Motor connection failed")
