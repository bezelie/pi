# Bezelie Sample Code for Raspberry Pi : Super Sonic Range Sensor Test

import RPi.GPIO as GPIO
import time
import bezelie

# Definition
trigger_pin = 18    # GPIO 18
echo_pin = 23       # GPIO 23
actionDistance = 10 # centi mater

# Set Up
bezelie.centering()
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

# Function
def send_trigger_pulse():
    GPIO.output(trigger_pin, True)
    time.sleep(0.0001)
    GPIO.output(trigger_pin, False)

def wait_for_echo(value, timeout):
    count = timeout
    while GPIO.input(echo_pin) != value and count > 0:
        count -= 1

def get_distance():
    send_trigger_pulse()
    wait_for_echo(True, 10000)
    start = time.time()
    wait_for_echo(False, 10000)
    finish = time.time()
    pulse_len = finish - start
    distance  = pulse_len / 0.000058
    return (distance)    

# Main Loop
try:
  while True:
    print(round(get_distance(),1))
    if get_distance() < actionDistance:
      bezelie.movePit (-30)
      time.sleep(0.5)
      bezelie.movePit (0, 4)
      time.sleep(0.5)
    else:
      time.sleep(0.5)
except KeyboardInterrupt:
  print " Interrupted by Keyboard"

GPIO.cleanup()
