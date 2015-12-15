import time
import numpy
import os
import threading
import datetime
from datetime import datetime
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#########################################
# CONFIG
#########################################
Volume = str(15) # Volume of messages from 0 - 100
MakePicPin = 3 # Pin on which detection of new picture is
FlashPin = 4 # Pin to enable the flash lights
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
GPIO.setup(FlashPin,GPIO.OUT)
GPIO.output(FlashPin,GPIO.LOW)

def GetSelectedBackground():
    lastbuttontime = 0
    while True:
        now = time.time()
        for i in range(0,len(BackgroundPins)):
            if not GPIO.input(BackgroundPins[i]) and (now - lastbuttontime) > 0.3:
                lastbuttontime = now
                return i
        time.sleep(0.020)


lastbuttontime = 0 
while True:
    
    now = time.time()
    
    if not GPIO.input(MakePicPin) and (now - lastbuttontime) > 0.2: # Button pressed, overcome the rebounce
        
        lastbuttontime = now

        # Ask & select the background
        os.system('mpg321 -g '+Volume+' welkom.mp3') # Message welcome
        time.sleep(1)
        
        os.system('mpg321 -g '+Volume+' selecteer.mp3') # Message to ask for picture selection
        for i in range(0,len(BackgroundOptions)):
            time.sleep(0.5)
            os.system('mpg321 -g '+Volume+' '+BackgroundOptions[i]+'.mp3')
        print('% Entering selecting the background routine')
        BackgroundID = GetSelectedBackground()
        print('% Gevonden pin: '+str(BackgroundID))
        os.system('mpg321 -g '+Volume+' geselecteerd.mp3') # Message to tell which one selected
        time.sleep(1)
        os.system('mpg321 -g '+Volume+' '+BackgroundOptions[BackgroundID]+'.mp3')
        backgroundfilename = BackgroundOptions[BackgroundID]+'.jpg'
        
        # Countdown and take the snapshot
        time.sleep(1)
        os.system('mpg321 -g '+Volume+' poseer.mp3') # Message that countdown starts
        time.sleep(1)
        os.system('mpg321 -g '+Volume+' vijf.mp3') # Message that countdown starts
        time.sleep(1)
        GPIO.output(FlashPin,GPIO.HIGH)
        os.system('raspistill -o snapshot.jpg &') # Make the snapshot
        os.system('mpg321 -g '+Volume+' vier.mp3') # Message that countdown starts
        time.sleep(1)
        os.system('mpg321 -g '+Volume+' drie.mp3') # Message that countdown starts
        time.sleep(1)
        os.system('mpg321 -g '+Volume+' twee.mp3') # Message that countdown starts
        time.sleep(1)
        os.system('mpg321 -g '+Volume+' een.mp3') # Message that countdown starts
        print('% Picture taken, now converting')

        # Wait and convert the pictures
        time.sleep(2)
        os.system('mpg321 -g '+Volume+' wachten.mp3') # Tell the user to wait
        GPIO.output(FlashPin,GPIO.LOW)
        os.system('convert snapshot.jpg -resize 2400x1600 -crop 1800x1600+120+0 snapshot2.jpg')
        #os.system('convert snapshot2.jpg -fuzz 40% -transparent \'90af61\' snapshot_green_removed.png') # Remove the green background with image magick
        os.system('convert snapshot2.jpg -fuzz 20% -transparent green snapshot_green_removed.png') # Remove the green background with image magick
        outputfilename = 'snapshot_'+datetime.now().strftime("%Y%m%d_%H%M%S")+'.jpg'
        os.system('convert -composite '+backgroundfilename+' snapshot_green_removed.png -geometry +300 '+outputfilename) # Overlay on top of selected background
        print('% Converting ended, now printing')

        # Print picture and inform ready
        #os.system('lp -d Canon_CP910_ipp '+outputfilename) # Print the picture with cups
        time.sleep(30)
        os.system('mpg321 -g '+Volume+' klaar.mp3') # Tell user that it is finished

    time.sleep(0.020)
    
