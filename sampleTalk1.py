# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : Talking Test by AquesTalk Pi

from time import sleep
import subprocess
import bezelie

# Get Started
bezelie.centering()

# Main Loop
try:
  while (True):
    bezelie.movePit (20, 1)
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "こんにちわー" | aplay', shell=True)
    sleep(0.5)
    bezelie.movePit (0, 1)
    sleep(2)

except KeyboardInterrupt:
  print ' Interrupted by Keyboard'
