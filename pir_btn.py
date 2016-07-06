#!/usr/bin/env python

import sys
import time # module provides various time-related functions
import RPi.GPIO as io 
import subprocess # module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
import os

io.setmode(io.BCM)
SHUTOFF_DELAY = 60
PIR_PIN = 25
BTN_PIN = 23

def main(): # main function defined 
    io.setup(PIR_PIN, io.IN)
    io.setup(BTN_PIN, io.IN)
    turned_off = False
    last_motion_time = time.time()

    while True:
        if io.input(PIR_PIN):
            last_motion_time = time.time()
            #print ".",
            sys.stdout.flush()
            while io.input(BTN_PIN):
                  subprocess.call("/home/pi/photoframe/download.py") #change to call All-in-one-pi
                  time.sleep(10)
            if turned_off:
                turned_off = False
                turn_on()
        else:
            if not turned_off and time.time() > (last_motion_time +
                                                SHUTOFF_DELAY):
                turned_off = True
                turn_off()

        time.sleep(.1)

def turn_on(): #function to turn on
    subprocess.call("sh /home/pi/photoframe/slideshow.sh", shell=True)#change to call All-in-one-pi

def turn_off():
    cmdKill = "pkill fbi"
    os.system(cmdKill)
    subprocess.call("sh /home/pi/photoframe/monitor_off.sh", shell=True)#change to call All-in-one-pi

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        io.cleanup()
