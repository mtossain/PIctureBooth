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
makepicpin = 3                           # Pin on which detection of new picture is
backgroundpins = [6, 13, 19, 26]         # Pins for background

#########################################
# MAIN
#########################################

# Set the input GPIO pins and pull up
for i in range(0,len(backgroundpins)):
	GPIO.setup(backgroundpins[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(makepicpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lastbuttontime = 0
def GetSelectedBackground():
	while True:
		now = time.time()
	    for i in range(0,len(backgroundpins)):
			if not GPIO.input(backgroundpins[i]) and (now - lastbuttontime) > 0.2:
				lastbuttontime = now
				return i
		time.sleep(0.020)


while True:
	
	now = time.time()
	
	if not GPIO.input(makepicpin) and (now - lastbuttontime) > 0.2: # Button pressed, overcome the rebounce
		
		lastbuttontime = now

		# Ask & select the background
		os.system('mpg321 selectbackground.mp3') # Message to ask for picture selection
		BackgroundID = GetSelectedBackground()
		backgroundfilename = 'background'+str(BackgroundID)+'.jpg'
		
		# Countdown and take the snapshot
		os.system('mpg321 countdown.mp3') # Message that countdown starts
		os.system('raspistill -vf -o snapshot.jpg' # Make the snapshot
		
		# Wait and convert the picture
		os.system('mpg321 wait.mp3') # Tell the user to wait
		os.system('convert snapshot.jpg -fuzz 40% -transparent #1eff01 snapshot_green_removed.png') # Remove the green background with image magick
		outputfilename = 'snapshot_'+datetime.now().strftime("%Y%m%d_%H%M%S")+'.png'
		os.system('convert -composite '+backgroundfilename+' snapshot_green_removed.png -gravity center '+outputfilename) # Overlay on top of selected background
		
		# Print picture and inform ready
		os.system('lp -d Canon_CP900 '+outputfilename) # Print the picture with cups
		time.sleep(30)
		os.system('mpg321 ready.mp3')	

    time.sleep(0.020)
	
