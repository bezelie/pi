# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : Talking Test by AquesTalk Pi

from time import sleep
import subprocess

# Main Loop
try:
  while (True):
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "こんにちわー" | aplay', shell=True)
    sleep(3)
except KeyboardInterrupt:
  print ' Interrupted by Keyboard'
