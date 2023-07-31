import time
from buildhat import Motor, Hat
from huskylib import HuskyLensLibrary
from math import floor
from adafruit_rplidar import RPLidar


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
lidar = RPLidar(None, '/dev/ttyUSB0', timeout=3)

max_distance = 3000.0 # max size of the area (in mm)
wall_threshold = 300.0 # threshold for wall detection (in mm)
scan_data = [0]*360 # raw data from lidar
lidar_data = [0]*360 # processed data from lidar

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
def resetmotors():
    motorL.stop()
    motorR.stop()
    time.sleep(0.1)

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
    motorL.run_for_seconds(t, blocking=block)
    motorR.run_for_seconds(t, blocking=block)
    time.sleep(t)
    
def movestraight_until_stop(speed):
    motorL.set_default_speed(-speed)
    motorR.set_default_speed(speed) 
    motorL.start()
    motorR.start()
    
def stopmotor():
    motorL.stop()
    motorR.stop()

# lidar functions
# def is_wall_nearby_in_direction(start_angle, end_angle):
#     return any(distance < wall_threshold for distance in lidar_data[start_angle:end_angle+1])

def isFront(data):
    return data[1] >= 0 and data[1] < 90
def isLeft(data):
    return data[1] >= 90 and data[1] < 180
def isBack(data):
    return data[1] >= 180 and data[1] < 270
def isRight(data):
    return data[1] >= 270 and data[1] < 360

def find_walls(data):
    # Front angles [0, 90)
    if isFront(data) and data[2] < wall_threshold:
        print("Front")
        return True
    # Right angles [90, 180)
    if isRight(data) and data[2] < wall_threshold:
        print("Right")
        return True
    # Back angles [180, 270)
    if isBack(data) and data[2] < wall_threshold:
        print("Back")
        return True
    # Left angles [270, 360)
    if isLeft(data) and data[2] < wall_threshold:
        print("Left")
        return True
    return False

def get_data():
    try:
        stop_flag = False  # Flag variable to indicate when to stop the outer loop
        for measurement in lidar.iter_scans():
            # list of tuple -> quality, degree, distance
            # print(measurement)
            for data in measurement:
                if data[2] != 0:
                    print(data[2])
                    if find_walls(data):
                        stop_flag = True
                        break  # Stop the inner loop
            if stop_flag:
                stopmotor()
                break  # Stop the outer loop
        return 1
    except Exception as e:
        print(e)
        return -1

# main starts here
# movestraight(100,10,False)
# recursive function to wait for hat to be connected
if until_finds_hat(30) is not None: # set maximum find time to 30 seconds
    time.sleep(1)
    if hl.algorthim("ALGORITHM_COLOR_RECOGNITION") is not None:
        if validlearnedblocks():
            current = searchlearnedblocks()
            if current!=-1:
                speed = decide(current)
                if speed != [-1,-1]: # if founded red or green
                    moveseperately(speed[0],speed[1],False,1) # dist is still fixed case for testing -> t is always 2 s
    resetmotors()
    movestraight_until_stop(20)
    get_data()
    
lidar.stop_motor()
lidar.stop()
lidar.disconnect()
    
# while True:
#     print(motor.get_aposition())
