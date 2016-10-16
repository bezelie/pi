# -*- coding: utf-8 -*-
# Bezelie demo Code for Raspberry Pi : Voice Recording and Play

import RPi.GPIO as GPIO
import time
import picamera
import subprocess
import pyaudio
import wave
import bezelie

# Settin Up
trigger_pin = 18    # GPIO 18
echo_pin = 23       # GPIO 23
actionDistance = 10 # centi mater
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

# Pyaudio
FORMAT = pyaudio.paInt16  #データフォーマットは int16型
CHANNELS = 1              #モノラル
RATE = 16000              #サンプル周波数 取り込み１回分の時間
CHUNK = 2**11             #取り込み１回分のデータサイズ
RECORD_SECONDS = 2        #録音する時間の長さ
WAVE_OUTPUT_FILENAME = "test.wav"
audio = pyaudio.PyAudio() #pyaudioのインスタンスaudioを生成

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

def sensorCheck():
  if get_distance() < actionDistance:
    bezelie.centering()
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "ろくおんかいし" | aplay', shell=True)
    camera.stop_preview()
#   Recording
    print ("recording...")
    stream = audio.open(format=FORMAT, channels=CHANNELS,
      rate=RATE, input=True,  #入力モード
      input_device_index=0,   #デバイスのインデックス番号
      frames_per_buffer=CHUNK)
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
      data = stream.read (CHUNK )
      frames.append (data )
    print ("finished recording")
    stream.stop_stream()           # streamを停止
    stream.close()                 # streamを開放
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb') # wavファイルをwbモードで開く
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

#   Play
    subprocess.call('aplay test.wav', shell=True)

    camera.start_preview()

# Centering All Servos
bezelie.centering()

# Main Loop
try:
  with picamera.PiCamera() as camera:
    camera.resolution = (400, 240)   # Change this number for your display
    camera.rotation = 180            # comment out if your screen upside down
    camera.start_preview()
    time.sleep(0.2)
    pit = 0
    while (True):
      bezelie.moveRot (-15)
      bezelie.moveYaw (-40, 2)
      sensorCheck()
      time.sleep (1)
      bezelie.moveRot (15)
      bezelie.moveYaw (40, 2)
      sensorCheck()
      time.sleep (1)
      pit += 10
      if pit > 10:
        pit = -30
      bezelie.movePit (pit)
      time.sleep (1)

except KeyboardInterrupt:
  print " Interrupted by Keyboard"

GPIO.cleanup()
audio.terminate()              # インスタンスaudioを終了
