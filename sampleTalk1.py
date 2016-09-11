# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : Talking Test by AquesTalk Pi

import time
import subprocess

try:
  while (True):
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "こんにちわー" | aplay', shell=True)
    time.sleep(3)
except KeyboardInterrupt:
  print ' Interrupted!'

  

