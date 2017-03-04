# -*- coding: utf-8 -*-
# Bezelie demo Code for Raspberry Pi : Voice Recording and Play

import time
from time import sleep
import subprocess
import pyaudio
import wave
import bezelie

# Pyaudio
FORMAT = pyaudio.paInt16  #データフォーマットは int16型
CHANNELS = 1              #モノラル
RATE = 16000              #サンプル周波数 取り込み１回分の時間
CHUNK = 2**11             #取り込み１回分のデータサイズ
RECORD_SECONDS = 2        #録音する時間の長さ
WAVE_OUTPUT_FILENAME = "test2.wav"
audio = pyaudio.PyAudio() #pyaudioのインスタンスaudioを生成

# Centering All Servos
bezelie.initPCA9685()
bezelie.moveCenter()

# Main Loop
try:
  while (True):
    bezelie.moveHead (20)
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "録音開始" | aplay', shell=True)
    sleep (0.1)
    print ("recording...")
# Record
    stream = audio.open(format=FORMAT, channels=CHANNELS,
      rate=RATE, input=True,  #入力モード
      input_device_index=0,   #デバイスのインデックス番号
      frames_per_buffer=CHUNK)
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
      data = stream.read (CHUNK )
      frames.append (data )
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "録音終了" | aplay', shell=True)
    bezelie.moveHead (0)
    print ("finished recording")
    stream.stop_stream()           # streamを停止
    stream.close()                 # streamを開放
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb') # wavファイルをwbモードで開く
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
# Play
    subprocess.call('aplay "'+ WAVE_OUTPUT_FILENAME +'"', shell=True)
    sleep (4)

except KeyboardInterrupt:
  print " Interrupted by Keyboard"

audio.terminate()              # インスタンスaudioを終了
