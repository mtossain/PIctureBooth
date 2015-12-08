import time
import numpy
import os
import threading
import datetime
from datetime import datetime
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

def GetSelectedBackground():
    lastbuttontime = 0
    while True:
        now = time.time()
        for i in range(0,len(BackgroundPins)):
            if not GPIO.input(BackgroundPins[i]) and (now - lastbuttontime) > 0.1:
                lastbuttontime = now
                return i
        time.sleep(0.020)


lastbuttontime = 0 
while True:
    
    now = time.time()
    
    if not GPIO.input(MakePicPin) and (now - lastbuttontime) > 0.2: # Button pressed, overcome the rebounce
        
        lastbuttontime = now

        # Ask & select the background
        os.system('mpg321 -g 5 welkom.mp3') # Message welcome
        time.sleep(1)
        
        os.system('mpg321 -g 5 selecteer.mp3') # Message to ask for picture selection
        for i in range(0,len(BackgroundOptions)):
            time.sleep(0.5)
            os.system('mpg321 -g 5 '+BackgroundOptions[i]+'.mp3')
        print('% Entering selecting the background routine')
        BackgroundID = GetSelectedBackground()
        print('% Gevonden pin: '+str(BackgroundID))
        os.system('mpg321 -g 5 geselecteerd.mp3') # Message to tell which one selected
        time.sleep(1)
        os.system('mpg321 -g 5 '+BackgroundOptions[BackgroundID]+'.mp3')
        backgroundfilename = BackgroundOptions[BackgroundID]+'.jpg'
        
        # Countdown and take the snapshot
        time.sleep(1)
        os.system('mpg321 -g 5 poseer.mp3') # Message that countdown starts
        time.sleep(1)
        os.system('mpg321 -g 5 vijf.mp3') # Message that countdown starts
        time.sleep(1)
        os.system('mpg321 -g 5 vier.mp3') # Message that countdown starts
        time.sleep(1)
        os.system('raspistill -vf -o snapshot.jpg &') # Make the snapshot
        os.system('mpg321 -g 5 drie.mp3') # Message that countdown starts
        time.sleep(1)
        os.system('mpg321 -g 5 twee.mp3') # Message that countdown starts
        time.sleep(1)
        os.system('mpg321 -g 5 een.mp3') # Message that countdown starts
        print('% Picture taken, now converting')
        
        # Wait and convert the pictures
        time.sleep(2)
        os.system('mpg321 -g 5 wachten.mp3') # Tell the user to wait
        os.system('convert snapshot.jpg -resize 2400x1600 snapshot2.jpg')
        os.system('convert snapshot2.jpg -fuzz 40% -transparent \'#5b5e2f\' snapshot_green_removed.png') # Remove the green background with image magick
        outputfilename = 'snapshot_'+datetime.now().strftime("%Y%m%d_%H%M%S")+'.png'
        os.system('convert -composite '+backgroundfilename+' snapshot_green_removed.png -gravity center '+outputfilename) # Overlay on top of selected background
        print('% Converting ended, now printing')

        # Print picture and inform ready
        os.system('lp -d HP_Photosmart_6520_series '+outputfilename) # Print the picture with cups
        time.sleep(30)
        os.system('mpg321 -g 5 klaar.mp3') # Tell user that it is finished

    time.sleep(0.020)
    
