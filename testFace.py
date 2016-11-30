# -*- coding: utf-8 -*-
# Bezelie Face Recognition Test
# カメラで顔を認識したら喋る

import picamera
import picamera.array
import cv2              # Open CV 2
import pygame
import sys              # for sys.exit()
import subprocess
import bezelie
from time import sleep

pygame.init()
size=(800,480)
screen = pygame.display.set_mode(size)

def pygame_imshow(array):
  b,g,r = cv2.split(array)
  rgb = cv2.merge([r,g,b])
  surface1 = pygame.surfarray.make_surface(rgb)       
  surface2 = pygame.transform.rotate(surface1, -90)
  surface3 = pygame.transform.flip(surface2, True, False)
  screen.blit(surface3, (0,0))
  pygame.display.flip()

cascade_path =  "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml"
cascade = cv2.CascadeClassifier(cascade_path)

# Get Started
bezelie.centering()

# Main Loop
with picamera.PiCamera() as camera:
  with picamera.array.PiRGBArray(camera) as stream:
    camera.resolution = (800, 480) # ディスプレイの解像度に合わせてください。
    camera.hflip = True            # 上下反転。不要なら削除してください。
    camera.vflip = True            # 左右反転。不要なら削除してください。
    sleep (1)

    while True:
      # stream.arrayにBGRの順で映像データを格納
      camera.capture(stream, 'bgr', use_video_port=True)
      # グレースケール画像に変換しgrayに代入
      gray = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY)
      # grayから顔を探す
      facerect = cascade.detectMultiScale(gray, scaleFactor=1.9, minNeighbors=1, minSize=(200,200), maxSize=(400,400))
      # scaleFactor 大きな値にすると速度が早くなり、精度が落ちる。1.1〜1.9ぐらい。
      # minNeighbors 小さな値にするほど顔が検出されやすくなる。通常は3〜6。
      # minSize 検出する顔の最小サイズ。解像度に合わせて修正してください。
      # maxSize 検出する顔の最大サイズ。解像度に合わせて修正してください。
      if len(facerect) > 0:   # 顔が検出された場合の処理
        for rect in facerect: # 顔の場所に四角を表示 
          # rect[0:2]:長方形の左上の座標, rect[2:4]:長方形の横と高さ
          # rect[0:2]+rect[2:4]:長方形の右下の座標
          cv2.rectangle(stream.array, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), (0,255,0), thickness=4)

        bezelie.movePit (-15) # 背伸びをさせる
        sleep (0.2)
        bezelie.moveRot ( 10)
        sleep (0.2)
        bezelie.moveRot (-10)
        sleep (0.4)
        bezelie.moveRot ( 0)
        subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "こんにちわー" | aplay', shell=True)
        sleep(0.5)
        bezelie.movePit (0, 1)
        sleep(0.2)

      # pygameで画像を表示
      pygame_imshow(stream.array)

      # "q"を入力でアプリケーション終了
      for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
          if e.key == pygame.K_q:
            pygame.quit()
            sys.exit()

      # streamをリセット
      stream.seek(0)
      stream.truncate()
