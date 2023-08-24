import os
import time
from math import floor
from rplidar import RPLidar
from buildhat import MotorPair, Hat
from huskylib import HuskyLensLibrary
import RPi.GPIO as GPIO


nearestRight=3000.00
nearestFront=3000.00
nearestLeft=3000.00
# Setup the RPLidar
# PORT_NAME = '/dev/ttyUSB0'
# lidar = RPLidar(None, PORT_NAME, timeout=3)
lidar = RPLidar('/dev/ttyUSB0',baudrate=115200)
hl = HuskyLensLibrary("I2C","",address=0x32)
lidar.connect()  # Open the serial port for the LiDAR
info = lidar.get_info()
print("LidarInfo",info)
health = lidar.get_health()
print("LidarHeealth",health)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)#LEDใช้ขา7
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def find_hat(t):
    try:
        return Hat()
    except:
        if(t>0):
            time.sleep(1)
            return find_hat(t-1)
        
# huskylens functions
def try_getlearnedBlocks(): # safe way to get learned blocks
    try:
        return hl.learnedBlocks()
    except Exception:
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
    return id==1
def isGreen(id):
    return id==2

#lidar.clean_input()
#lidar.reset()
#funtion for scan object variable myCount is amount of round to scan

lidar._set_pwm(2750)
def scan():
    try:
        stop_flag = False
        global nearestRight
        global nearestFront
        global nearestLeft
        for scan_data in lidar.iter_scans():   
            for data in scan_data:
                angle = float(data[1])
                distance = float(data[2])

                if angle <= 30 and angle >= 0:
                    nearestLeft = distance
                    stop_flag = True
                        
                elif angle >= 60 and angle <= 120:
                    nearestFront = distance                      
                    stop_flag = True
                        
                elif angle >= 150 and angle <= 180:
                    nearestRight = distance
                    stop_flag = True 
            if stop_flag:
                stop_flag = True    
                break 
            if stop_flag:  
                stop_flag = True    
                break
        lidar.stop()    
        return  True
    except Exception as e:
        print(e)
        return  False
########################################### 
def processNear():
    print("nearestLeft=",nearestLeft)
    print("nearestFront=",nearestFront)  
    print("nearestRight=",nearestRight)

def compareLeftRight():#funcเปรียบเทียบซ้ายขวาเพื่อเลือกเลี้ยว
    if nearestLeft >  nearestRight:
        print("left")
        pair.run_for_degrees(150,speedl=40, speedr=40)#Turnleft
        lidar.clean_input
    elif nearestLeft <  nearestRight:
        print("Right")
        pair.run_for_degrees(150,speedl=-40, speedr=-40) #TurnRight
        lidar.clean_input  

def scan_for_lights():
    deltadisL = 0.0
    deltadisR = 0.0
    lastdis = 0.0
    pair.run_for_degrees(120,speedl=5, speedr=5) #turnLeft
    end_time = time.time()+2.0
    for scan_data in lidar.iter_scans():   
            for (_,angle,distance) in scan_data:
                # print(angle,distance)                
                if angle >= 60 and angle <= 120:
                    if lastdis==0 :
                        lastdis=distance
                        continue
                    deltadisL = max(deltadisL,abs(lastdis-distance))
                    lastdis = distance
            if time.time() > end_time:
                lidar.stop()
                break
    print(deltadisL)
    pair.run_for_degrees(190,speedl=-5, speedr=-5) # turnright
    end_time = time.time()+2.0
    for scan_data in lidar.iter_scans():   
            for (_,angle,distance) in scan_data:
                # print(angle,distance)                
                if angle >= 60 and angle <= 120:
                    if lastdis==0 :
                        lastdis=distance
                        continue
                    deltadisR = max(deltadisR,abs(lastdis-distance))
                    lastdis = distance
            if time.time() > end_time:
                lidar.stop()
                break
    print(deltadisR)
    pair.run_for_degrees(120,speedl=5, speedr=5) #turnback
    if deltadisL > deltadisR : # object is on the left
        pair.run_for_degrees(120,speedl=5, speedr=5) #turnLeft
    else : # object is on the right
        pair.run_for_degrees(120,speedl=-5, speedr=-5) #turnRight
    pair.start(-20,20)
    stop_flag = False
    for scan_data in lidar.iter_scans():   
            for (_,angle,distance) in scan_data:                
                if angle >= 60 and angle <= 120:
                    if distance <= 200 :
                        pair.stop()
                        stop_flag = True
                        break
            if stop_flag:
                break
    pair.run_for_degrees(120,speedl=-80, speedr=-40)
pair.run_for_degrees(60,speedl=-40, speedr=-40)
# move accordingly

#Main funtion start

#ans =scan()
 
time.sleep(1)
while True:
    if GPIO.input(13) == 1:
        break
if find_hat(30) is not None:
    pair = MotorPair('B', 'A')
    print("starting")
    scan_for_lights()
    # end_time = time.time() + 60
    # while True:
    #     if time.time()>end_time:
    #         break
    #     #pair.start(speedl=-100, speedr=100)#forward
    #     ans =scan()
    #     lidar.stop()
    #     print("nearestLeft=",nearestLeft)
    #     print("nearestFront=",nearestFront)  
    #     print("nearestRight=",nearestRight)
    #     wall = 200
    #     corner_wall = 700
    #     s = 60
    #     angle = 300
    #     speed = s
    #     if nearestFront >= corner_wall:
    #         if nearestLeft >= wall and nearestRight >= wall:
    #             print("1")
    #             pair.start(speedl = -speed , speedr = speed) #forward
    #         elif nearestLeft < wall and nearestRight >= wall:
    #             print("2")
    #             pair.run_for_degrees(angle,speedl=-s, speedr=-s) #TurnRight
    #             lidar.clean_input
    #         elif nearestLeft >= wall and nearestRight <= wall:
    #             print("3")
    #             pair.run_for_degrees(angle,speedl=s, speedr=s)#turnleft
    #             lidar.clean_input   
    #         elif nearestLeft < wall and nearestRight < wall:
    #             print("4")
    #             pair.run_for_degrees(angle,speedl=s, speedr=s) #TurnLeft  
    #     elif nearestFront < corner_wall:
    #         if nearestLeft >= corner_wall and nearestRight >= corner_wall:
    #             print("5")
    #             compareLeftRight()
    #         elif nearestLeft < corner_wall and nearestRight >= corner_wall:
    #             print("6Right")
    #             pair.run_for_degrees(angle,speedl=-s, speedr=-s) #TurnRight
    #             lidar.clean_input
    #         elif nearestLeft >= corner_wall and nearestRight < corner_wall:
    #             print("7left")
    #             pair.run_for_degrees(angle,speedl=s, speedr=s)#Turnleft
    #             lidar.clean_input 
    #         elif nearestLeft < corner_wall and nearestRight < corner_wall:
    #             print("8")
    #             pair.run_for_degrees(angle,speedl=-s, speedr=-s) #TurnRight  
    lidar.stop_motor()
    lidar.stop()
    lidar.disconnect()
