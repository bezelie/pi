#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : Tweet Talker

from time import sleep
import subprocess
import json
import twitterInfo as info  # Twitter情報ファイル
from requests_oauthlib import OAuth1Session  # Twitter認証モジュール
import bezelie

# variables
talkSpeed = 140  # AquesTalk Piの発話速度。50〜300で大きいほど速くなる。デフォルトは100。
interval = 30  # 新しいツイートがあるかどうかをチェックする間隔。（秒）

# APIのURL
url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
  # [manual](http://westplain.sakuraweb.com/translate/twitter/Documentation/REST-APIs/Public-API/GET-statuses-user_timeline.cgi)

# APIに渡すパラメータ
params ={
  'screen_name' : info.SCREEN_NAME,  # 取得したいユーザーのツイッター名。@〜。
  'count' : 1}  # 取得するツイート数。指定しなかった場合のデフォは２０。

# インスタンスの生成
twitter = OAuth1Session(
  info.CONSUMER_KEY,        # 
  info.CONSUMER_SECRET,     # 
  info.ACCESS_TOKEN,        # 
  info.ACCESS_TOKEN_SECRET) # 

# Get Started
bezelie.initPCA9685()
bezelie.moveCenter()

# main loop
while True:
  response = twitter.get(url, params = params)  # getメソッドでtwitterからレスポンスを取得。
  if response.status_code == 200:  # status_codeが200だと取得成功。
    body = response.text  # textメソッドによってボディ部分だけを抽出。
    dic = json.loads(body)  # jsonモジュールのloadsメソッドによってPythonの辞書形式に変換。
    for i in dic:
      message = i['text']  # キー'text'に対応する値を取得。
      print message
      bezelie.moveHead (20)
      subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s "'+str(talkSpeed)+'" "'+ message +'" | aplay', shell=True)
      sleep(0.5)
      bezelie.moveHead (0, 1)
      params ={
        'screen_name' : info.SCREEN_NAME,
        'since_id' : i['id_str'], # 新規のツイートだけを取得するためにIDを保存しておく。
        'count' : 1}  # 取得するツイート数。指定しなかった場合のデフォは２０。
  else:
    print("ERROR: %d" % response.status_code)  # エラーが発生した場合。
  print "waiting untill "+info.SCREEN_NAME+" would say something new"
  sleep (interval)
