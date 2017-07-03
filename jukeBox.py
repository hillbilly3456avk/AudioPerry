#!/usr/bin/python
import RPi.GPIO as GPIO
import sys
import os
import time
import glob
from pygame import mixer
from subprocess import PIPE, STDOUT

#play all mp3 in the specific folder assigned to the button
#@para global volume
#@para the list conataining the mp3 files to play
#return the global volume
def ButtonPressed(vol, list):
  print "the unsorted list:"
  print list
  list=sorted(list)
  print "the sorted list:"
  print(list)
  #init music player
  mixer.init()
  mixer.music.set_volume(vol)
  #play the list
  for x in range(0, len(list)):
   print(list[x])
   mixer.music.load(list[x])
   mixer.music.play()
   time.sleep(2)
   while mixer.music.get_busy()==True:
    time.sleep(0.5)
    #check if other button is pressed
    if GPIO.input(4)==0 or GPIO.input(17)==0 or GPIO.input(27)==0 or GPIO.input(22)==0 or GPIO.input(10)==0 or GPIO.input(9)==0 or GPIO.input(13)==0:
     mixer.music.stop()
     mixer.quit()
     return vol
    #check volume
    if GPIO.input(5)==0:
     vol=vol-0.02
     vol=clamp(vol)
     print vol
     mixer.music.set_volume(vol)
    if GPIO.input(6)==0:
     vol=vol+0.02
     vol=clamp(vol)
     print vol
     mixer.music.set_volume(vol)
    continue
   time.sleep(2)
  #cleanup
  mixer.quit()
  return vol

#clamp the volume to a min (0.1) and max (0.7) level
#@para n the volume to limit
#@return the limited volume
def clamp(volume):
    minn=0.01
    maxn=0.7
    if volume < minn:
        return minn
    elif volume > maxn:
        return maxn
    else:
        return volume

def standby(vol):
  while GPIO.input(13)==1:
   time.sleep(2)
  time.sleep(2)
  startupchord(vol)
  return vol

def startupchord(vol):
  #init the pygame mixer
  mixer.init()
  #init the gobal volume to 0.1
  vol=0.10
  mixer.music.set_volume(vol)
  mixer.music.load("/home/pi/radioMarit/startup.mp3")
  mixer.music.play()
  time.sleep(1.7)
  mixer.music.stop()
  return vol


#here we have the famous main
print('Marit\s Music Player')
#init the GPIO module
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(5, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(9, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(10, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#define global volume variable
vol=0.1
#play the startup chord ;-)
vol=startupchord(vol)

print "--- Press button #1-6 to select folder and play mp3, ..."
print "--- button info and menu to decrease/increase volume. ---"


#endless
while True:
 time.sleep(1)

#button 1
 if(GPIO.input(4)==0):
  list=glob.glob("/mnt/radioMarit/001/*.mp3")
  print "Button 1 pressed"
  vol=ButtonPressed(vol, list)
#button 2
 if(GPIO.input(17)==0):
  list=glob.glob("/mnt/radioMarit/002/*.mp3")
  print "Button 2 pressed"
  vol=ButtonPressed(vol, list)
#button 3
 if(GPIO.input(27)==0):
  list=glob.glob("/mnt/radioMarit/003/*.mp3")
  print "Button 3 pressed"
  vol=ButtonPressed(vol, list)
#button 4
 if(GPIO.input(22)==0):
  list=glob.glob("/mnt/radioMarit/004/*.mp3")
  print "Button 4 pressed"
  vol=ButtonPressed(vol, list)
#button 5
 if(GPIO.input(10)==0):
  list=glob.glob("/mnt/radioMarit/005/*.mp3")
  print "Button 5 pressed"
  vol=ButtonPressed(vol, list)
#button 6
 if(GPIO.input(9)==0):
  list=glob.glob("/mnt/radioMarit/006/*.mp3")
  print "Button 6 pressed"
  vol=ButtonPressed(vol, list)
#button shutdown
 if(GPIO.input(13)==0):
  print "shutdown pressed"
  time.sleep(2)
  vol=standby(vol)
