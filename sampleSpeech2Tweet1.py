#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bezelie demo Code for Raspberry Pi : Voice Tweeter

from time import sleep
import subprocess
import json
import socket #  ソケット通信モジュール
import xml.etree.ElementTree as ET # XMLエレメンタルツリー変換モジュール
from requests_oauthlib import OAuth1Session  # Twitter認証モジュール
import twitterInfo as info  # Twitter情報ファイル
import bezelie

# Variables
bufferSize = 1024 # 受信するデータの最大バイト数。できるだけ小さな２の倍数が望ましい。

# Juliusをサーバモジュールモードで起動＝音声認識サーバーにする
print "Pleas Wait For A While"  # サーバーが起動するまで時間がかかるので待つ
p = subprocess.Popen(["sh /home/pi/bezelie/testpi/julius2.sh"], stdout=subprocess.PIPE, shell=True)
  # julius2.sh = 自然言語認識版設定ファイル「julius2.jconf」による起動。
pid = p.stdout.read()  # 終了時にJuliusのプロセスをkillするためプロセスIDを保存しておく 
print "Julius's Process ID is "+pid

# Juliusサーバーにアクセスするため自分のIPアドレスを取得する 
getIP = subprocess.Popen(["hostname -I | awk -F' ' '{print $1}'"], stdout=subprocess.PIPE, shell=True)
myIP = getIP.stdout.read()
print "My IP is " +myIP

# TCPクライアントを作成しJuliusサーバーに接続する
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # clientオブジェクト生成
client.connect((myIP, 10500))  # Juliusサーバーに接続。portはデフォルトが10500。

# 解説
# Juliusから出力されるXML構造
# <RECOGOUT>
#   <SHYPO RANK="" SCORE="" GRAM="">
#     <WHYPO WORD="" CLASSID="" PHONE="" CM=""/>
#   </SHYPO>
# </RECOGOUT>

# Twitter APIのURL
url = "https://api.twitter.com/1.1/statuses/update.json"
  # [manual](http://westplain.sakuraweb.com/translate/twitter/Documentation/REST-APIs/Public-API/POST-statuses-update.cgi)

# Twitterインスタンスの生成
twitter = OAuth1Session(
  info.CONSUMER_KEY,        # 
  info.CONSUMER_SECRET,     # 
  info.ACCESS_TOKEN,        # 
  info.ACCESS_TOKEN_SECRET) # 

# Get Started
bezelie.initPCA9685()
bezelie.moveCenter()

# Main Loop
try:
  data = ""
  messages = ""
  print "OK. Please Speak"
  while True:
    if "</RECOGOUT>\n." in data:  # RECOGOUTツリーの最終行を見つけたら以下の処理を行う
      root = ET.fromstring('<?xml version="1.0"?>\n' + data[data.find("<RECOGOUT>"):].replace("<s>","").replace("\n.", "").replace("。","eom").replace("</s>",""))
        # ETのfromstringメソッドはXML文字列からコンテナオブジェクトであるElement型に直接取り込む
        # CLASSIDに<s>や</s>が入っているとETがエラーを吐くので削除。
        # WORDの最後の「。」をメッセージのエンコード「eom」に置換。
      for whypo in root.findall("./SHYPO/WHYPO"):
        message = whypo.get("WORD")
        if message != "eom":
          messages = messages + message
        else:
          bezelie.moveHead (20)
          params ={'status' : messages}  # ツイート内容
          response = twitter.post(url, params = params)  # twitterにpost
          if response.status_code == 200:  # status_codeが200なら成功
            print "tweeted ..."+messages
          elif response.status_code == 403:
            print messages
            print "同じメッセージは繰り返しツイートできません"
          else:
            print("ERROR: %d" % response.status_code)  # エラーの場合はメッセージ表示
          bezelie.moveHead (0,1)
          sleep (1)
          print "Please Speak"
          data = ""  # 認識終了したのでデータをリセットする
          messages = ""
    else:
      response = client.recv(bufferSize)
      data = data + response  # Juliusサーバーから受信
        # /RECOGOUTに達するまで受信データを追加していく

except KeyboardInterrupt:
  # CTRL+Cで終了
  print "  ご利用ありがとうございました"
  p.kill()
  subprocess.call(["kill " + pid], shell=True) # juliusのプロセスを終了
  client.close()
