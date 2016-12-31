# -*- coding: utf-8 -*-
# Bezelie demo Code for Raspberry Pi : Simple Conversation

import csv
from time import sleep
from random import randint
import socket
import subprocess
import xml.etree.ElementTree as ET
import bezelie

csvFile = "bezeDialog.csv"

# Variables
muteTime = 0.8     # 音声入力を無視する時間（の半分の秒数）
bufferSize = 16384 # 受信するデータの最大バイト数。できるだけ小さな２の倍数が望ましい。

# Juliusをサーバモジュールモードで起動＝音声認識サーバーにする
print "Pleas Wait For A While"  # サーバーが起動するまで時間がかかるので待つ
p = subprocess.Popen(["sh julius.sh"], stdout=subprocess.PIPE, shell=True)
  # subprocess.PIPEは標準ストリームに対するパイプを開くことを指定するための特別な値
pid = p.stdout.read()  # 終了時にJuliusのプロセスをkillするためプロセスIDをとっておく 
print "Julius's Process ID =" +pid

# Juliusサーバーにアクセスするため自分のIPアドレスを取得する 
getIP = subprocess.Popen(["hostname -I | awk -F' ' '{print $1}'"], stdout=subprocess.PIPE, shell=True)
myIP = getIP.stdout.read()
print "My IP is " +myIP

# TCPクライアントを作成しJuliusサーバーに接続する
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # clientオブジェクト生成
client.connect((myIP, 10500))  # Juliusサーバーに接続

# Functions
def replyMessage(keyWord):
  data = []
  with open(csvFile, 'rb') as f:  # opening the datafile to read as utf_8
    for i in csv.reader(f):
      data.append(i)              # raw data

  data1 = []
  for index,i in enumerate(data): # making a candidate list
    if unicode(i[0], 'utf-8')==keyWord:  # i[0]はstrなのでutf-8に変換して比較する必要がある
      j = randint(1,100)          # Adding random value to probability
      data1.append(i+[j]+[index]) # Candidates data

  if data1 == []:
    for index,i in enumerate(data): # making a candidate list
      if i[0]=='不一致':  # 該当するキーワードが見つからなかった場合は、「不一致」から返答する
        j = randint(1,100)          # Adding random value to probability
        data1.append(i+[j]+[index]) # Candidates data

  maxNum = 0
  for i in data1:                 # decision
    if i[2] > maxNum:             # Whitch is the max probability.
      maxNum = i[2]               # Max probability
      ansNum = i[3]               # Index of answer

  # AquesTalk
  print "The reply is..."+data[ansNum][1]
  subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "'+ data[ansNum ][1] +'" | aplay -q', shell=True)

# Get Started
bezelie.initPCA9685()
bezelie.moveCenter()

# Main Loop
try:
  data = ""
  print "Please Speak"
  while True:
    if "</RECOGOUT>\n." in data:  # RECOGOUTツリーの最終行を見つけたら以下の処理を行う
      root = ET.fromstring('<?xml version="1.0"?>\n' + data[data.find("<RECOGOUT>"):].replace("\n.", ""))
        # fromstringはXML文字列からコンテナオブジェクトであるElement型に直接取り込む
      for whypo in root.findall("./SHYPO/WHYPO"):
        # 認識した語に対する返答を探しランダムで返答する。
        keyWord = whypo.get("WORD")
        print "You might speak..."+keyWord
        bezelie.moveHead (20)
        replyMessage(keyWord)
        # 本来は発話中にJuliusを一時停止すべきですが、このプログラムでは簡易的にウェイトだけで処理しています。
        bezelie.moveHead (0, 1)
        for var in range (0,2):  # 音声合成音を入力してしまわないように受信データを２秒弱の間無視する
          sleep (0.8)
            # 0.8秒のwaitを２回ループ入れてみたところ丁度よかったが、環境によっては調整が必要と思われる。
          data = client.recv(bufferSize)
      data = ""  # 認識終了したのでデータをリセットする
    else:
      data = data + client.recv(bufferSize)  # Juliusサーバーから受信
        # /RECOGOUTに達するまで受信データを追加していく

except KeyboardInterrupt:
  # CTRL+Cで終了
  print "KeyboardInterrupt occured."
  p.kill()
  subprocess.call(["kill " + pid], shell=True) # juliusのプロセスを終了
  client.close()
