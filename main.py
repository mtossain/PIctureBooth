import time
import numpy
import os
import threading
import datetime
from datetime import timedelta
from datetime import date
import math
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#########################################
# CONFIG
#########################################
MakePicPin = 3 # Pin on which detection of new picture is
BackgroundPins = [6, 13, 19, 26] # Pins for background
BackgroundOptions = ['1kerst', '2strand', '3harrypotter', '4leeuwen']
# Note externally numbers are from 1,...
# Internally it ranges from 0,...

#########################################
# MAIN
#########################################

# Set the input GPIO pins and pull up
for i in range(0,len(BackgroundPins)):
    GPIO.setup(BackgroundPins[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(MakePicPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lastbuttontime = 0
def GetSelectedBackground():
    while True:
        now = time.time()
        for i in range(0,len(BackgroundPins)):
            if not GPIO.input(BackgroundPins[i]) and (now - lastbuttontime) > 0.2:
                lastbuttontime = now
                return i
        time.sleep(0.020)


while True:
    
    now = time.time()
    
    if not GPIO.input(MakePicPin) and (now - lastbuttontime) > 0.2: # Button pressed, overcome the rebounce
        
        lastbuttontime = now

        # Ask & select the background
        os.system('mpg321 welkom.mp3') # Message welcome
        time.sleep(2)
        
        os.system('mpg321 selecteer.mp3') # Message to ask for picture selection
        for i in range(0,len(BackgroundOptions)):
            time.sleep(1)
            os.system('mpg321 '+BackgroundOptions[i]+'.mp3') 
        BackgroundID = GetSelectedBackground()
        os.system('mpg321 geselecteerd.mp3') # Message to tell which one selected
        time.sleep(1)
        os.system('mpg321 '+BackgroundOptions[i]+'.mp3')
        backgroundfilename = 'background'+str(BackgroundID)+'.jpg'
        
        # Countdown and take the snapshot
        time.sleep(2)
        os.system('mpg321 poseer.mp3') # Message that countdown starts
        os.system('raspistill -vf -o snapshot.jpg' # Make the snapshot
        
        # Wait and convert the picture
        time.sleep(2)
        os.system('mpg321 wachten.mp3') # Tell the user to wait
        os.system('convert snapshot.jpg -fuzz 40% -transparent #1eff01 snapshot_green_removed.png') # Remove the green background with image magick
        outputfilename = 'snapshot_'+datetime.now().strftime("%Y%m%d_%H%M%S")+'.png'
        os.system('convert -composite '+backgroundfilename+' snapshot_green_removed.png -gravity center '+outputfilename) # Overlay on top of selected background
        
        # Print picture and inform ready
        os.system('lp -d Canon_CP900 '+outputfilename) # Print the picture with cups
        time.sleep(30)
        os.system('mpg321 klaar.mp3')   

    time.sleep(0.020)
    
