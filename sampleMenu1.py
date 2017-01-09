#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bezelie test code for Raspberry Pi : Launcher Menu

import sys
import Tkinter  # Tk Interface
import subprocess
import bezelie

mainWindow = Tkinter.Tk() # Tk Objectのインスタンスを生成
mainWindow.title("Sample Menu1")  # ウィンドウ上端のバーに表示される文字
mainWindow.geometry("320x280+100+50")  # ウィンドウサイズと画面内の表示位置を指定
  # フォーマットは("幅x高"+横座標+縦座標)

# X Windowアプリの起動
def picturesFunction():
  subprocess.call('gpicview /home/pi/Pictures/', shell=True)

# サウンドテスト
def speakerFunction():
  subprocess.call('aplay Front_Center.wav', shell=True)

# Webページを開く
def webFunction():
  subprocess.call('chromium-browser http://bezelie.com', shell=True)

# pythonプログラムの実行
def centeringFunction():
  subprocess.call('python bezelie.py', shell=True)

# タイトル表示
titleLabelWidget = Tkinter.Label(mainWindow, 
  height = 1, width = 30,
  background = "blue", foreground = "white",
  font = ("Times", 16, "normal"),
  text = "サンプルメニュー")

# pythonプログラムの実行
centeringButtonWidget = Tkinter.Button(mainWindow,
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  text = "サーボのセンタリング",
  command = centeringFunction)

# サウンドテスト
speakerButtonWidget = Tkinter.Button(mainWindow,
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  text = "スピーカーテスト",
  command = speakerFunction)

# X Windowアプリの実行
picturesButtonWidget = Tkinter.Button(mainWindow,
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  text = "画像ディレクトリの表示",
  command = picturesFunction)

# Webページの表示
webButtonWidget = Tkinter.Button(mainWindow,
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  text = "ベゼリーwebページ",
  command = webFunction)

# 閉じるボタン
exitButtonWidget = Tkinter.Button(mainWindow,
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  text = "ウィンドウを閉じる",
  command = sys.exit)

# widgetの配置
titleLabelWidget.pack()
centeringButtonWidget.pack()
speakerButtonWidget.pack()
picturesButtonWidget.pack()
webButtonWidget.pack()
exitButtonWidget.pack()

# Mail Loop
mainWindow.mainloop()  # このメインループを実行することで初めて画像が表示される。
