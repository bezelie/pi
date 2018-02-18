#!/usr/bin/python
# -*- coding: utf-8 -*-
# demo Code for Raspberry Pi : Label Recognition of Google Vision API

from time import sleep
import subprocess
import socket #  ソケット通信モジュール
import xml.etree.ElementTree as ET # XMLエレメンタルツリー変換モジュール
import picamera
import requests
import base64
import json
import bezelie

# Variables
API_KEY = ''  # Google Cloud Platform Consoleで登録したAPIキー
GOOGLE_CLOUD_VISION_API_URL = 'https://vision.googleapis.com/v1/images:annotate?key='
bufferSize = 1024  # 受信するデータの最大バイト数。できるだけ小さな２の倍数が望ましい。
jpgFile = '/home/pi/Pictures/capture.jpg'  # キャプチャー画像ファイル

# Juliusをサーバモジュールモードで起動＝音声認識サーバーにする
print "Please Wait For A While"  # サーバーが起動するまで時間がかかるので待つ
p = subprocess.Popen(["sh julius.sh"], stdout=subprocess.PIPE, shell=True)
  # subprocess.PIPEは標準ストリームに対するパイプを開くことを指定するための特別な値
pid = p.stdout.read()  # 終了時にJuliusのプロセスをkillするためプロセスIDをとっておく 
print "Julius's Process ID =" +pid

# TCPクライアントを作成しJuliusサーバーに接続する
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # clientオブジェクト生成
client.connect(('localhost', 10500))  # Juliusサーバーに接続

# Functions
def request_cloud_vison_api(image_base64):
    api_url = GOOGLE_CLOUD_VISION_API_URL + API_KEY
    req_body = json.dumps({
        'requests': [{
            'image': {
                'content': image_base64.decode('utf-8') # base64でencodeする。
            },
            'features': [{
                'type': 'LABEL_DETECTION',
#                'type': 'TEXT_DETECTION',
#                'type': 'LOGO_DETECTION',
                'maxResults': 3,
            }]
        }]
    })
    res = requests.post(api_url, data=req_body)
    return res.json()

def reAction(keyWord):
  print "You might speak..."+keyWord
  subprocess.call('sudo amixer -q sset Mic 0', shell=True)  # マイクの感度を０にする。
  if keyWord != unicode('画像認識', 'utf-8'):
    message = "何か見せて！"
    print message
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "'+ message +'" | aplay -q', shell=True)
    bezelie.moveHead (-10)
  else:
    message = "どれどれ"
    print message
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "'+ message +'" | aplay -q', shell=True)
    bezelie.moveHead (-10)
    bezelie.moveHead (0)
    camera.stop_preview()
    camera.capture(jpgFile)
    sleep(0.1)
    with open(jpgFile, 'rb') as img:
        img_byte = img.read()
    img_base64 = base64.b64encode(img_byte)
    result = request_cloud_vison_api(img_base64)
    for i in range(3):
      try:
        answer = result['responses'][0]['labelAnnotations'][i]['description'].encode('utf-8')
        print (answer)
        subprocess.call('flite -voice "kal16" -t "'+ answer +'"', shell=True)
      except:
        print ("no answer")
    camera.start_preview()
  bezelie.moveHead (0)
  subprocess.call('sudo amixer -q sset Mic 50', shell=True)  # マイクの感度を元に戻す。

# Get Started
bezelie.initPCA9685()
bezelie.moveCenter()
subprocess.call('sudo amixer -q sset Mic 50', shell=True)  # マイクの感度をONにする

# Main Loop
try:
  data = ""
  print "Please Speak"
  with picamera.PiCamera() as camera:
    camera.resolution = (800, 480)   # Change this number for your display
    camera.rotation = 180            # comment out if your screen upside down
    camera.start_preview()
    sleep(1)
    while True:
      if "</RECOGOUT>\n." in data:  # RECOGOUTツリーの最終行を見つけたら以下の処理を行う
        try:
          root = ET.fromstring('<?xml version="1.0"?>\n' + data[data.find("<RECOGOUT>"):].replace("\n.", ""))
          # fromstringはXML文字列からコンテナオブジェクトであるElement型に直接取り込む
          for whypo in root.findall("./SHYPO/WHYPO"):
            keyWord = whypo.get("WORD")
          if keyWord != unicode("不一致", 'utf-8'):  # 不一致の場合は何もしない。
            reAction(keyWord)
            print "Please Speak"
        except:
          print "error"  # エラーがでても終了しないようにする。
        data = ""  # 認識終了したのでデータをリセットする
      else:
        data = data + client.recv(bufferSize)  # Juliusサーバーから受信
        # /RECOGOUTに達するまで受信データを追加していく

except KeyboardInterrupt:
  # CTRL+Cで終了
  print "  終了しました"
  p.kill()
  subprocess.call(["kill " + pid], shell=True) # juliusのプロセスを終了
  client.close()
