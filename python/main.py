import time
from buildhat import Motor, Hat
from huskylib import HuskyLensLibrary


# global varibles
wheel_circum = 6.88 # in cm
motorL = Motor('A') # default
motorR = Motor('B') # default
green = 2 # the id we're looking for
red = 1
hat = Hat()
hl = HuskyLensLibrary("I2C","",address=0x32)

# time functions
 
def cal_timeneeded(distance,speedL,speedR):
    # calculate time needed for each given movement
    time
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

def moveseperately(speedL,speedR,block,dist):
    #set up default speed according to input values
    motorL.set_default_speed(-speedL)
    motorR.set_default_speed(speedR)
    # t = cal_timeneeded(dist,speedL,speedR)
    t = 2 # fixed case for testing
    
    # run motor L and R for t seconds with blocking setting (True = Wait for first op to end before running,
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


# main starts here
# movestraight(100,10,False)

time.sleep(1)
if validlearnedblocks():
    current = searchlearnedblocks()
    if current!=-1:
        speed = decide(current)
        if speed != [-1,-1]: # if founded red or green
            moveseperately(speed[0],speed[1],False,1) # dist is still fixed case for testing -> t is always 2 s

# while True:
#     print(motor.get_aposition())
