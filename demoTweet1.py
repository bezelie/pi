# -*- coding: utf-8 -*-
# Bezelie demo Code for Raspberry Pi : Voice Recognition and Tweeting

import RPi.GPIO as GPIO
import time
import picamera
import subprocess
import requests
import tweepy
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
RECORD_SECONDS = 5       #録音する時間の長さ
WAVE_OUTPUT_FILENAME = "test.wav"

# docomo voice recognition API
path = '/home/pi/bezelie/pi/test.wav'
url = "https://api.apigw.smt.docomo.ne.jp/amiVoice/v1/recognize?APIKEY={}".format("6b696876634774444d58347572613931614d644c32376c6777304738586865395658636647655967396238")
files = {"a": open(path, 'rb'), "v":"on"}

# Tweepy
CONSUMER_KEY = '2RYcvvpQ7aBdAQKilJYwVNhaB'
CONSUMER_SECRET = 'oXbvlaK9iubKU18L1dJ6EGLAwtwEHEymWCW8uPDdFzyNrCmMnR'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
ACCESS_TOKEN = '352124433-ekLsAKzEP4fx6XnjcHYDJPMQkuyD0TsImYQ26pus'
ACCESS_SECRET = 'cItWOg3raqDuy75OBCODxNCn5MucIDbgXfRCslDGJbgI5'
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

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
#    time.sleep(3)    
#    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "ろくおんかいし" | aplay', shell=True)
#    time.sleep(3)    
#    camera.stop_preview()
#   Recording
    print ("recording...")
    audio = pyaudio.PyAudio() #pyaudioのインスタンスaudioを生成
    stream = audio.open(format=FORMAT, channels=CHANNELS,
      rate=RATE, input=True,  #入力モード
      input_device_index=0,   #デバイスのインデックス番号
      frames_per_buffer=CHUNK)
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
      data = stream.read (CHUNK )
      frames.append (data )
    print ("finished recording")
#    time.sleep(1)    
    stream.stop_stream()           # streamを停止
    stream.close()                 # streamを開放
    audio.terminate()              # インスタンスaudioを終了
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb') # wavファイルをwbモードで開く
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

#   voice recognition
    r = requests.post(url, files=files)
    message = r.json()['text']
    print message

#   tweet
#    api.update_status(status = "hello" )
    api = tweepy.API(auth)
    api.update_status(status = message )
    time.sleep(1)
#    camera.start_preview()

# Centering All Servos
bezelie.centering()

# Main Loop
try:
  with picamera.PiCamera() as camera:
    camera.resolution = (400, 240)   # Change this number for your display
    camera.rotation = 180            # comment out if your screen upside down
#    camera.start_preview()
    time.sleep(0.2)
    pit = 0
    while (True):
      bezelie.moveRot (-15)
      bezelie.moveYaw (-40, 2)
      sensorCheck()
      time.sleep (0.1)
      bezelie.moveRot (15)
      bezelie.moveYaw (40, 2)
      sensorCheck()
      time.sleep (0.1)
      pit += 10
      if pit > 10:
        pit = -30
      bezelie.movePit (pit)

except KeyboardInterrupt:
  print " Interrupted by Keyboard"

GPIO.cleanup()
