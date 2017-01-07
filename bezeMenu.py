#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bezelie test code for Raspberry Pi : GUI

import csv
import sys
import Tkinter  # Tk Interface
from PIL import Image, ImageTk  # Python Image Library
import subprocess
import bezelie
import bezeConfig

# csvFile = "bezeConfig.csv"
originalData = []  # Make empty list
configWindow = None

# Read bezeConfig.py
headAdj = bezeConfig.headAdj
backAdj = bezeConfig.backAdj
stageAdj = bezeConfig.stageAdj
awaking = bezeConfig.awakingTime
sleeping = bezeConfig.sleepingTime
interval = bezeConfig.intervalTime

def centeringFunction():
#  titleLabelWidget.config(text = "サーボをセンタリングします")
  bezelie.moveCenter()
  head.set(0)
  back.set(0)
  stage.set(0)

def speakerFunction():
#  titleLabelWidget.config(text = "サウンドチェック")
  subprocess.call('aplay Front_Center.wav', shell=True)

def picturesFunction():
#  titleLabelWidget.config(text = "Picturesディレクトリの中を表示します")
  subprocess.call('gpicview /home/pi/Pictures/', shell=True)

def editorFunction():
#  titleLabelWidget.config(text = "せりふデータを編集します")
  subprocess.call('sudo leafpad bezeTalk.csv', shell=True)

def webFunction():
#  titleLabelWidget.config(text = "オンラインマニュアルを開きます")
  subprocess.call('chromium-browser http://bezelie.com', shell=True)

def addressFunction():
  getIP = subprocess.Popen(["hostname -I | awk -F' ' '{print $1}'"], stdout=subprocess.PIPE, shell=True)
  myIP = getIP.stdout.read()
  addressButtonWidget.config(text = "IPアドレス:" +myIP)

def moveHeadFunction(n):
  bezelie.moveHead(head.get()) 
def moveBackFunction(n):
  bezelie.moveBack(back.get()) 
def moveStageFunction(n):
  bezelie.moveStage(stage.get()) 

# Make A Config Menu
def configFunction():
  global configWindow
  if configWindow is None or not configWindow.winfo_exists():
    # コンフィグウィンドウが複数開くことを防ぐため。
    configWindow = Tkinter.Toplevel()
    configWindow.title("Config Menu")
    configWindow.geometry("470x300+320+50")

    configFrame = Tkinter.Frame(configWindow,
      background = "white")

    titleConfigLabel = Tkinter.Label(configFrame, text = "コンフィグメニュー",
      background = "blue", foreground = "white",
      height = 1, width = 20,
      font = ("Times", 16, "normal"))

    headAdjLabel = Tkinter.Label(configFrame, text = "HEADセンタリング調整",
      background = "white", foreground = "blue",
      height = 1, width = 18,
      font = ("Times", 16, "normal"))

    headPlusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "+",
      command = headPlusFunction)

    headMinusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "-",
      command = headMinusFunction)

    global headAdjDisp
    headAdjDisp = Tkinter.Label(configFrame,
      height = 1, width = 4,
      font = ("Times", 16, "normal"),
      text = " ")

    backAdjLabel = Tkinter.Label(configFrame, text = "BACKセンタリング調整",
      background = "white", foreground = "blue",
      height = 1, width = 18,
      font = ("Times", 16, "normal"))

    backPlusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "+",
      command = backPlusFunction)

    backMinusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "-",
      command = backMinusFunction)

    global backAdjDisp
    backAdjDisp = Tkinter.Label(configFrame,
      height = 1, width = 4,
      font = ("Times", 16, "normal"),
      text = " ")

    stageAdjLabel = Tkinter.Label(configFrame, text = "STAGEセンタリング調整",
      background = "white", foreground = "blue",
      height = 1, width = 18,
      font = ("Times", 16, "normal"))

    stagePlusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "+",
      command = stagePlusFunction)

    stageMinusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "-",
      command = stageMinusFunction)

    global stageAdjDisp
    stageAdjDisp = Tkinter.Label(configFrame,
      height = 1, width = 4,
      font = ("Times", 16, "normal"),
      text = " ")

    awakingAdjLabel = Tkinter.Label(configFrame, text = "起床時間設定",
      background = "white", foreground = "blue",
      height = 1, width = 18,
      font = ("Times", 16, "normal"))

    awakingPlusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "+",
      command = awakingPlusFunction)

    awakingMinusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "-",
      command = awakingMinusFunction)

    global awakingAdjDisp
    awakingAdjDisp = Tkinter.Label(configFrame,
      height = 1, width = 4,
      font = ("Times", 16, "normal"),
      text = " ")

    sleepingAdjLabel = Tkinter.Label(configFrame, text = "就寝時間設定",
      background = "white", foreground = "blue",
      height = 1, width = 18,
      font = ("Times", 16, "normal"))

    sleepingPlusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "+",
      command = sleepingPlusFunction)

    sleepingMinusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "-",
      command = sleepingMinusFunction)

    global sleepingAdjDisp
    sleepingAdjDisp = Tkinter.Label(configFrame,
      height = 1, width = 4,
      font = ("Times", 16, "normal"),
      text = " ")

    intervalAdjLabel = Tkinter.Label(configFrame, text = "発話間隔設定",
      background = "white", foreground = "blue",
      height = 1, width = 18,
      font = ("Times", 16, "normal"))

    intervalPlusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "+",
      command = intervalPlusFunction)

    intervalMinusButton = Tkinter.Button(configFrame,
      height = 1, width = 2,
      font = ("Times", 16, "normal"),
      text = "-",
      command = intervalMinusFunction)

    global intervalAdjDisp
    intervalAdjDisp = Tkinter.Label(configFrame,
      height = 1, width = 4,
      font = ("Times", 16, "normal"),
      text = " ")

    doneConfigButton = Tkinter.Button(configFrame, text = "決定",
      height = 1, width = 4,
      font = ("Times", 16, "normal"),
      command = doneConfigFunction)

    cancelConfigButton = Tkinter.Button(configFrame, text = "閉じる",
      height = 1, width = 4,
      font = ("Times", 16, "normal"),
      command = cancelConfigFunction)

    # Place widgets on the ConfigWindow
    configFrame.pack()
    titleConfigLabel.grid(column = 0, row = 0)
    headAdjLabel.grid(column = 0, row = 1)
    headPlusButton.grid(column = 3, row = 1)
    headAdjDisp.grid(column = 2, row = 1)
    headMinusButton.grid(column = 1, row = 1)
    backAdjLabel.grid(column = 0, row = 2)
    backPlusButton.grid(column = 3, row = 2)
    backAdjDisp.grid(column = 2, row = 2)
    backMinusButton.grid(column = 1, row = 2)
    stageAdjLabel.grid(column = 0, row = 3)
    stagePlusButton.grid(column = 3, row = 3)
    stageAdjDisp.grid(column = 2, row = 3)
    stageMinusButton.grid(column = 1, row = 3)
    awakingAdjLabel.grid(column = 0, row = 4)
    awakingPlusButton.grid(column = 3, row = 4)
    awakingAdjDisp.grid(column = 2, row = 4)
    awakingMinusButton.grid(column = 1, row = 4)
    sleepingAdjLabel.grid(column = 0, row = 5)
    sleepingPlusButton.grid(column = 3, row = 5)
    sleepingAdjDisp.grid(column = 2, row = 5)
    sleepingMinusButton.grid(column = 1, row = 5)
    intervalAdjLabel.grid(column = 0, row = 6)
    intervalPlusButton.grid(column = 3, row = 6)
    intervalAdjDisp.grid(column = 2, row = 6)
    intervalMinusButton.grid(column = 1, row = 6)
    doneConfigButton.grid(column = 2, row = 7)
    cancelConfigButton.grid(column = 0, row = 7)

    # Read data from csv file
    headAdjDisp.config(text = headAdj)
    backAdjDisp.config(text = backAdj)
    stageAdjDisp.config(text = stageAdj)
    awakingAdjDisp.config(text = awaking)
    sleepingAdjDisp.config(text = sleeping)
    intervalAdjDisp.config(text = interval)

def doneConfigFunction():
#  headAdj = headAdjDisp.cget("text")
#  backAdj = backAdjDisp.cget("text")
#  stageAdj = stageAdjDisp.cget("text")
#  awaking = awakingAdjDisp.cget("text")
#  sleeping = sleepingAdjDisp.cget("text")
#  interval = intervalAdjDisp.cget("text")
  line = ["headAdj = "+str(headAdjDisp.cget("text"))+"\n"]
  line.append("backAdj = "+str(backAdjDisp.cget("text"))+"\n")
  line.append("stageAdj = "+str(stageAdjDisp.cget("text"))+"\n")
  line.append("awakingTime = "+str(awakingAdjDisp.cget("text"))+"\n")
  line.append("sleepingTime = "+str(sleepingAdjDisp.cget("text"))+"\n")
  line.append("intervalTime = "+str(intervalAdjDisp.cget("text"))+"\n")

  with open('bezeConfig.py', 'w') as f:
    f.writelines(line)

  cancelConfigFunction()

def cancelConfigFunction():
  global configWindow
  configWindow.withdraw()
  configWindow = None

def headPlusFunction():
  s = headAdjDisp.cget("text")
  i = int(s)+1
  if i > 10: i=10
  headAdjDisp.config(text = i)
  bezelie.moveHead(i)

def headMinusFunction():
  s = headAdjDisp.cget("text")
  i = int(s)-1
  if i < -10: i=-10
  headAdjDisp.config(text = i)
  bezelie.moveHead(i)

def backPlusFunction():
  s = backAdjDisp.cget("text")
  i = int(s)+1
  if i > 10: i=10
  backAdjDisp.config(text = i)
  bezelie.moveBack(i)

def backMinusFunction():
  s = backAdjDisp.cget("text")
  i = int(s)-1
  if i < -10: i=-10
  backAdjDisp.config(text = i)
  bezelie.moveBack(i)

def stagePlusFunction():
  s = stageAdjDisp.cget("text")
  i = int(s)+1
  if i > 10: i=10
  stageAdjDisp.config(text = i)
  bezelie.moveStage(i)

def stageMinusFunction():
  s = stageAdjDisp.cget("text")
  i = int(s)-1
  if i < -10: i=-10
  stageAdjDisp.config(text = i)
  bezelie.moveStage(i)

def awakingPlusFunction():
  s = awakingAdjDisp.cget("text")
  i = int(s)+1
  if i > 10: i=10
  awakingAdjDisp.config(text = i)

def awakingMinusFunction():
  s = awakingAdjDisp.cget("text")
  i = int(s)-1
  if i < 1: i=1
  awakingAdjDisp.config(text = i)

def sleepingPlusFunction():
  s = sleepingAdjDisp.cget("text")
  i = int(s)+1
  if i > 24: i=24
  sleepingAdjDisp.config(text = i)

def sleepingMinusFunction():
  s = sleepingAdjDisp.cget("text")
  i = int(s)-1
  if i < 20: i=20
  sleepingAdjDisp.config(text = i)

def intervalPlusFunction():
  s = intervalAdjDisp.cget("text")
  i = int(s)+1
  if i > 100: i=100
  intervalAdjDisp.config(text = i)

def intervalMinusFunction():
  s = intervalAdjDisp.cget("text")
  i = int(s)-1
  if i < 1: i=1
  intervalAdjDisp.config(text = i)

# メインウィンドウ
mainWindow = Tkinter.Tk() # Tk Objectのインスタンスを生成
mainWindow.title("Bezelie Menu")
mainWindow.geometry("300x520+10+50")

head = Tkinter.IntVar()
back = Tkinter.IntVar()
stage = Tkinter.IntVar()
head.set(0)
back.set(0)
stage.set(0)

# メインフレーム
mainFrame=Tkinter.Frame(mainWindow,
  borderwidth = 2,
  background = "orange")

# タイトル
titleLabelWidget = Tkinter.Label(mainFrame, text = "ベゼリーメニュー",
  background = "blue", foreground = "white",
  height = 1, width = 22,
  font = ("Times", 16, "normal"))

addressButtonWidget = Tkinter.Button(mainFrame, text = "IPアドレス",
  background = "blue", foreground = "white",
  height = 2, width = 20,
  font = ("Times", 16, "normal"),
  command = addressFunction)

centeringButtonWidget = Tkinter.Button(mainFrame, text = "サーボのセンタリング",
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  command = centeringFunction)

# タイトルグラフィック
#image = Image.open('header.jpg')  # Open Image File
#im = ImageTk.PhotoImage(image)  # Convert jpg into PhotoImage
#logoLabelWidget = Tkinter.Label(mainFrame, 
#  image = im,
#  height = 60, width = 640)

headScaleWidget = Tkinter.Scale(mainFrame, label = "HEAD サーボ",
  showvalue = "True", digits = 2,
  from_ = -20, to = 20,
  length = 280, width = 15,
  sliderlength = 50, orient = "horizontal", resolution = 1,
  variable = head, command = moveHeadFunction)

backScaleWidget = Tkinter.Scale(mainFrame, label = "BACK サーボ",
  showvalue = "True", digits = 2,
  from_ = -30, to = 30,
  length = 280, width = 15,
  sliderlength = 50, orient = "horizontal", resolution = 1,
  variable = back, command = moveBackFunction)

stageScaleWidget = Tkinter.Scale(mainFrame, label = "STAGE サーボ",
  showvalue = "True", digits = 2,
  from_ = -50, to = 50,
  length = 280, width = 15,
  sliderlength = 50, orient = "horizontal", resolution = 1,
  variable = stage, command = moveStageFunction)

speakerButtonWidget = Tkinter.Button(mainFrame, text = "スピーカーテスト",
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  command = speakerFunction)

picturesButtonWidget = Tkinter.Button(mainFrame, text = "画像ディレクトリの表示",
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  command = picturesFunction)

editorButtonWidget = Tkinter.Button(mainFrame, text = "発話リストの編集",
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  command = editorFunction)

webButtonWidget = Tkinter.Button(mainFrame, text = "ベゼリーwebページ",
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  command = webFunction)

configButtonWidget = Tkinter.Button(mainFrame, text = "コンフィグ画面を開く",
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  command = configFunction)

exitButtonWidget = Tkinter.Button(mainFrame, text = "ウィンドウを閉じる",
  background = "white", foreground = "blue",
  height = 1, width = 20,
  font = ("Times", 16, "normal"),
  command = sys.exit)

# Place widgets on the mainWindow
mainFrame.pack()
titleLabelWidget.grid(column = 0, row = 0)
addressButtonWidget.grid(column = 0, row = 13)
#logoLabelWidget.grid(column = 0, row = 1)
centeringButtonWidget.grid(column = 0, row = 3)
headScaleWidget.grid(column = 0, row = 4)
backScaleWidget.grid(column = 0, row = 5)
stageScaleWidget.grid(column = 0, row = 6)
speakerButtonWidget.grid(column = 0, row = 7)
picturesButtonWidget.grid(column = 0, row = 8)
editorButtonWidget.grid(column = 0, row = 9)
webButtonWidget.grid(column = 0, row = 10)
configButtonWidget.grid(column = 0, row = 11)
exitButtonWidget.grid(column = 0, row = 12)

# Get Started
bezelie.initPCA9685()

# Mail Loop
addressFunction()
mainWindow.mainloop()  # このメインループを実行することで初めて画像が表示される。
