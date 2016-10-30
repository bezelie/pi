# -*- coding: utf-8 -*-

import Tkinter
from PIL import Image, ImageTk  # Python Image Library
import subprocess

mainWindowInstance = Tkinter.Tk() # making an Instance of Tk Object

def run1Function():
  label1Instance.config(text = "ゲーム開始！")
  subprocess.call('python gameDaruma.py', shell=True)

def run2Function():
  label1Instance.config(text = "ゲーム開始！")
  subprocess.call('python gameOnaka.py', shell=True)


image = Image.open('bezeface360.jpg')                       # Opening Image File
im = ImageTk.PhotoImage(image)                        # change jpg into PhotoImage
label0Instance = Tkinter.Label(mainWindowInstance, 
  image = im,
  height = 320,
  width = 520)
#  bd = 20,
#  bg = "white", 
#  fg = "blue",
#  font = "Helvetica",
#  text = "Hello world hello!",
# label0Instance.image = im

label1Instance = Tkinter.Label(mainWindowInstance, 
  height = 1,
  width = 20,
  bd = 20,
  bg = "white", 
  fg = "blue",
  font = "Helvetica",
  text = "ゲームを選んでね")
# label1Instance.image = im

button1Instance = Tkinter.Button(mainWindowInstance,
  bg = "white",
  fg = "blue",
  height = 1,
  width = 20,
  font = "Symbol",
  text = "旗あげゲーム",
  command = run1Function)

button2Instance = Tkinter.Button(mainWindowInstance,
  bg = "white",
  fg = "blue",
  height = 1,
  width = 20,
  font = "Symbol",
  text = "お腹砲",
  command = run2Function)

label0Instance.grid(
  column = 0,
  row = 0
  )
#label1Instance.grid(
#  column = 1,
#  row = 0
#  )
button1Instance.grid(
  column = 0,
  row = 1
  )

button2Instance.grid(
  column = 0,
  row = 2
  )

#button1Instance.bind('<Leave>', offFunction)

mainWindowInstance.mainloop()
