#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bezelie demo Code for Raspberry Pi : NTT Docomo Dialogue API
# NTT docomo 雑談対話APIのページ
# https://dev.smt.docomo.ne.jp/?p=docs.api.page&api_name=dialogue&p_name=api_usage_scenario

from time import sleep
import socket  # ソケット通信モジュール
import xml.etree.ElementTree as ET  # XMLエレメンタルツリー変換モジュール
import json
import requests
import subprocess

# constants
API_URL = 'https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY='  # NTTdocomo雑談対話APIのリクエストURL
API_KEY = ''  # 上記のページから発行されたあなたのAPI KEYを入力してください
url_key = API_URL + API_KEY

# variables
bufferSize = 1024  # 受信するデータの最大バイト数。２の倍数が望ましい。

# functions
def postAPI(message):
  payloadDic = {
    "utt": message,
    "context": "",  # 会話(しりとり)を継続する場合は、レスポンスボディのcontextの値を指定する
    "nickname": "光",
    "nickname_y": "ヒカリ",
    "sex": "女",
    "bloodtype": "B",
    "birthdateY": "1997",
    "birthdateM": "5",
    "birthdateD": "30",
    "age": "16",
    "constellations": "双子座",
    "place": "東京",
    "mode": "dialog",  # dialog＝通常雑談, srtr＝しりとり
    # 会話(しりとり)を継続する場合は、レスポンスボディのmodeの値を指定する
    "t": ""  # 無指定：デフォルトキャラ, 20 : 関西弁キャラ, 30 : 赤ちゃんキャラ
  }
  payloadStr = json.dumps(payloadDic)  # 辞書をstrのJSONにエンコードする
  responseClass = requests.post(url_key, data=payloadStr)  # APIにPOST
  responseDic = responseClass.json()  # APIからのレスポンスを辞書にデコードする
  responseStr = responseDic['utt'].encode('utf-8')  # 辞書からキー「utt」の値を抜き出し、utf-8でエンコードする
  print "The answer is..."+responseStr
  return responseStr

# 参考レスポンスのサンプル
# {
#  "utt":"こんにちは光さん",
#  "yomi":"こんにちはヒカリさん",
#  "mode":"dialog",
#  "da":"0",
#  "context":"aaabbbccc111222333 ",
# }

# Juliusをサーバモジュールモードで起動＝音声認識サーバーにする
print "Pleas Wait For A While"  # サーバーが起動するまで時間がかかるので待つ
p = subprocess.Popen(["sh /home/pi/bezelie/pi/juliusNL.sh"], stdout=subprocess.PIPE, shell=True)
pid = p.stdout.read()  # 終了時にJuliusのプロセスをkillするためプロセスIDをとっておく 
print "Julius's Process ID =" +pid

# TCPクライアントを作成しJuliusサーバーに接続する
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # clientオブジェクト生成
client.connect(('localhost', 10500))  # Juliusサーバーに接続。portはデフォルトが10500。

# Get Started
subprocess.call('sudo amixer -q sset Mic 50', shell=True)  # マイク感度を設定

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
        print "You might said..."+keyWord
        subprocess.call('sudo amixer -q sset Mic 0', shell=True)  # 自分の声を取り込まないようにマイクをオフにする
        response = postAPI(keyWord)
        subprocess.call('/home/pi/bezelie/testpi/openJTalk.sh '+ response, shell=True)
#        subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "'+ response +'" | aplay -q', shell=True)
        subprocess.call('sudo amixer -q sset Mic 50', shell=True)  # マイクの感度を元にもどす
      except:
        print "error"
      data = ""  # 認識終了したのでデータをリセットする
    else:
      response = client.recv(bufferSize)
      data = data + response  # Juliusサーバーから受信
        # /RECOGOUTに達するまで受信データを追加していく

except KeyboardInterrupt:
  # CTRL+Cで終了
  print "  ありがとうございました"
  p.kill()
  subprocess.call(["kill " + pid], shell=True) # juliusのプロセスを終了
  client.close()
