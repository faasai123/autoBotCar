import time
from buildhat import Motor, Hat
from huskylib import HuskyLensLibrary
from rplidar import RPLidar


# global varibles
wheel_circum = 6.88 # in cm
distance_covered_in_1_second = 10 # in cm (from measurement with speed=100 on both wheels)
motorL = Motor('B') # default
motorR = Motor('A') # default
green = 2 # the id we're looking for
red = 1
hat = Hat()
# Setup the huskylens
hl = HuskyLensLibrary("I2C","",address=0x32)
# Setup the RPLidar
lidar = RPLidar('/dev/ttyUSB0')

max_distance = 3000.0 # max size of the area (in mm)
wall_threshold = 150.0 # threshold for wall detection (in mm)
scan_data = [0]*360 # raw data from lidar
lidar_data = [0]*360 # processed data from lidar
min_left = min_right = max_distance # variables for deciding to turn left or right at a corner

# Define segments for each direction (adjust angles as needed)
front_start, front_end = 0, 89
right_start, right_end = 90, 179
rear_start, rear_end = 180, 269
left_start, left_end = 270, 359

# time functions    
def until_finds_hat(t):
    try:
        return Hat()
    except:
        if(t>0):
            time.sleep(1)
            return until_finds_hat(t-1)
        else:
            return False

def cal_timeneeded(distance,speedL,speedR):
    # calculate time needed for each given movement using v = s/t -> t = s/v
    if speedL == speedR: # if car is moving stright
        speed = speedL * distance_covered_in_1_second
    else:
        return -1 # an error, both wheel should be moving at the same speed to find the time needed 
    # time is calculated from using the rule of three of a given speed and 100 to given distance
    time = distance/distance_covered_in_1_second * speed/100
    return time

# huskylens functions
def try_getlearnedBlocks(): # safe way to get learned blocks
    try:
        return hl.learnedBlocks()
    except IndexError:
        return None

def validlearnedblocks(): # check if there is already some learned blocks
    return hl.learnedObjCount()>0

def searchlearnedblocks():
    if validlearnedblocks():
        for items in try_getlearnedBlocks():
            print(items.ID)
            return items.ID # for testing, only one id value will be returned 
    else:
        return -1 # error, there's no learned blocks 

def isRed(id):
    return id==red
def isGreen(id):
    return id==green

def decide(id):
    if isRed(id):
        print("Right")
        return [100,80] # go right (speed used for testing)
    elif isGreen(id):
        print("Left")
        return [80,100] # go left (speed used for testing)
    else:
        return [-1,-1] # error value -> found other colors that's not red or green

# motor functions
def resetmotors(): # a function that tries to stop the motor before changing move speed
    motorL.stop()
    motorR.stop()
    time.sleep(0.5)

def moveseperately(speedL,speedR,block,dist):
    #set up default speed according to input values
    motorL.set_default_speed(-speedL)
    motorR.set_default_speed(speedR)
    # t = cal_timeneeded(dist,speedL,speedR)
    t = 2 # fixed case for testing
    
    # run motor L and R for t seconds with blocking setting (True = Wait for first operation to end before running,
    # False = Run simultaneously)
    motorL.run_for_seconds(t, blocking=block)
    motorR.run_for_seconds(t, blocking=block)
    time.sleep(t)

def movestraight(speed, t, block):
    # setupmotor(motors)
    # define default speed, motorA is in opposite direction
    motorL.set_default_speed(-speed)
    motorR.set_default_speed(speed)

    # run motor L and R for t seconds with blocking setting (True = Wait for first op to end before running,
    # False = Run simultaneously)
    motorL.start()
    motorR.start()
    time.sleep(t)
    
def movestraight_until_stop(speed):
    motorL.set_default_speed(-speed)
    motorR.set_default_speed(speed) 
    motorL.start() # function too start motor to move indefinately until motor.stop() is called
    motorR.start()
# turn then move forward for 0.5 second (this is done inorder for motor speed to go back to normal before moving forward)
def turn_left(t1):
    motorL.run_for_seconds(t1,100,False)
    motorR.run_for_seconds(t1,100,False)
    time.sleep(t1)
    t = 0.5
    motorL.stop()
    motorR.stop()
    time.sleep(t)
    motorL.run_for_seconds(t, blocking=False)
    motorR.run_for_seconds(t, blocking=False)
    time.sleep(t)

def turn_right(t1):
    motorL.run_for_seconds(t1,-100,False)
    motorR.run_for_seconds(t1,-100,False)
    time.sleep(t1)
    t = 0.5
    motorL.stop()
    motorR.stop()
    time.sleep(t)
    motorL.run_for_seconds(t, blocking=False)
    motorR.run_for_seconds(t, blocking=False)
    time.sleep(t)
    

# lidar functions
def isFront(angle):
    return angle >= 0 and angle < 90
def isLeft(angle):
    return angle >= 90 and angle < 180
def isBack(angle):
    return angle >= 180 and angle < 270
def isRight(angle):
    return angle >= 270 and angle < 360

def find_walls(distance,angle):
    # Front angles [0, 90)
    if isFront(angle) and distance < wall_threshold:
        print("Front")
        return True
    # Right angles [90, 180)
    if isRight(angle) and distance < wall_threshold:
        print("Right")
        return True
    # Back angles [180, 270) -> is ignored because of how the lidar sensor is placed
    # Left angles [270, 360)
    if isLeft(angle) and distance < wall_threshold:
        print("Left")
        return True
    return False

def corner_turn():
    try:
        start_time = time.time()
        end_time = start_time + 1.0  # 1 second
        for measurement in lidar.iter_scans():
            print("scanning")
            if time.time() > end_time():
                lidar.stop()
                break
            for (_, angle, distance) in measurement:
                if isLeft(angle):
                    min_left = min(min_left,distance)
                elif isRight(angle):
                    min_right = min(min_right,distance)
        print(min_left,min_right)
        if min_left > min_right: # right wall is closer -> a left turn
            print("Turn Left")
            resetmotors()
            turn_left()
        else: # left wall is closer -> a right turn
            print("Turn Right")
            resetmotors()
            turn_right()
        return 1
    except Exception as e:
        return -1

def corner_find(): # decide to turn left or right at corners
    try:
        for measurement in lidar.iter_scans():
            for (_, angle, distance) in measurement:
                if distance != 0:
                    # print(angle,distance,isFront(angle))
                    if isFront(angle) and find_walls(distance,angle): # if find wall infront closer than wall_threshold
                        resetmotors()
                        time.sleep(1)
                        print(angle,distance)
                        lidar.stop()
                        return corner_turn()     
    except Exception as e:
        # print(e)
        return -1
        

def get_data():
    try:
        stop_flag = False  # Flag variable to indicate when to stop the outer loop
        for measurement in lidar.iter_scans():
            # list of tuple -> quality, degree, distance
            for (_, angle, distance) in measurement:
                if distance != 0:
                    print(distance,angle)
                    if find_walls(distance,angle):
                        stop_flag = True
                        break # stop the inner loop
            if stop_flag:
                resetmotors()
                break  # Stop the outer loop
        return 1
    except Exception as e:
        print(e)
        return -1

# main starts here
# recursive function to wait for hat to be connected
if until_finds_hat(30) is not None: # set maximum find time to 30 seconds
    time.sleep(1)
    movestraight_until_stop(20)
    print("moving")
    while True:
        flag = False
        if corner_find()==1:
            lidar.stop()
            print("Found")
            min_left = min_right = 0
        else:
            pass
            # print("error")
    
lidar.stop_motor()
lidar.stop()
lidar.disconnect()
    
# while True:
#     print(motor.get_aposition())

