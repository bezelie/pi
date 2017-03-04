#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bezelie demo Code for Raspberry Pi : Voice Recognition

from time import sleep
import subprocess
import socket  # ソケット通信モジュール
import xml.etree.ElementTree as ET  # XMLエレメンタルツリー変換モジュール

# Variables
bufferSize = 1024  # 受信するデータの最大バイト数。できるだけ小さな２の倍数が望ましい。

# Juliusをサーバモジュールモードで起動＝音声認識サーバーにする
print "Pleas Wait For A While"  # サーバーが起動するまで時間がかかるので待つ
p = subprocess.Popen(["sh /home/pi/bezelie/testpi/juliusNL.sh"], stdout=subprocess.PIPE, shell=True)
pid = p.stdout.read()  # 終了時にJuliusのプロセスをkillするためプロセスIDをとっておく 
print "Julius's Process ID =" +pid

# TCPクライアントを作成しJuliusサーバーに接続する
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # clientオブジェクト生成
client.connect(('localhost', 10500))  # Juliusサーバーに接続。portはデフォルトが10500。

# Get Started
subprocess.call('sudo amixer -q sset Mic 50', shell=True)  # マイク感度を設定

# 参考
# Juliusから出力されるXML構造
# <RECOGOUT>
#   <SHYPO RANK="" SCORE="">
#     <WHYPO WORD="" CLASSID="" PHONE="" CM=""/>
#   </SHYPO>
# </RECOGOUT>

# Main Loop
try:
  data = ""
  print "Please Speak"
  while True:
    if "</RECOGOUT>\n." in data:  # RECOGOUTツリーの最終行を見つけたら以下の処理を行う
      try:
        # dataから必要部分だけ抽出し、かつエラーの原因になる文字列を削除する。
        data = data[data.find("<RECOGOUT>"):].replace("\n.", "").replace("</s>","").replace("<s>","")
        # fromstringはXML文字列からコンテナオブジェクトであるElement型に直接取り込む
        root = ET.fromstring('<?xml version="1.0"?>\n' + data)
        keyWord = ""
        for whypo in root.findall("./SHYPO/WHYPO"):
          keyWord = keyWord + whypo.get("WORD")
        print "You might speak..."+keyWord
        subprocess.call('sudo amixer -q sset Mic 0', shell=True)  # 自分の声を取り込まないようにマイクをオフにする
        subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "'+ keyWord +'" | aplay -q', shell=True)
        subprocess.call('sudo amixer -q sset Mic 50', shell=True)  # マイクの感度を元に戻す
      except:
        print "error"
      data = ""  # 認識終了したのでデータをリセットする
    else:
      # Juliusから出力データを受信する
      response = client.recv(bufferSize)
      # /RECOGOUTに達するまで受信データを追加していく
      data = data + response

except KeyboardInterrupt:
  # CTRL+Cで終了
  print "  ありがとうございました"
  p.kill()
  subprocess.call(["kill " + pid], shell=True) # juliusのプロセスを終了
  client.close()
