# -*- coding: utf-8 -*-
# Bezelie demo Code for Raspberry Pi : Voice Recognition

from time import sleep
import socket
import subprocess
import xml.etree.ElementTree as ET

# Variables
muteTime = 0.8     # 音声入力を無視する時間（の半分の秒数）
bufferSize = 16384 # 受信するデータの最大バイト数。できるだけ小さな２の倍数が望ましい。

# Juliusをモジュールモードで起動＝音声認識サーバーにする
print "Pleas Wait For A While"  # サーバーが起動するまで時間がかかるので待つ
p = subprocess.Popen(["sh julius.sh"], stdout=subprocess.PIPE, shell=True)
pid = p.stdout.read()  # 終了時にJuliusのプロセスをkillするためプロセスIDをとっておく 
print "Julius'S Process ID =" +pid

# Juliusサーバーにアクセスするため自分のIPアドレスを取得する 
getIP = subprocess.Popen(["hostname -I | awk -F' ' '{print $1}'"], stdout=subprocess.PIPE, shell=True)
myIP = getIP.stdout.read()
print "My IP is " +myIP

# TCPクライアントを作成しJuliusサーバーに接続する
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # clientオブジェクト生成
client.connect((myIP, 10500))  # Juliusサーバーに接続

# 解説
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
      root = ET.fromstring('<?xml version="1.0"?>\n' + data[data.find("<RECOGOUT>"):].replace("\n.", ""))
        # fromstringはXML文字列からコンテナオブジェクトであるElement型に直接取り込む
      for whypo in root.findall("./SHYPO/WHYPO"):
        print (whypo.get("WORD"))
        subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "'+ whypo.get("WORD") +'" | aplay -q', shell=True)
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
