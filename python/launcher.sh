#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/Desktop/projects
sudo python3 test.py # change this line to the target program (main) 
cd /
