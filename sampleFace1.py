# -*- coding: utf-8 -*-
# Bezelie Sample Code : Face Recognition Test
import picamera
import picamera.array
import cv2
import bezelie

cascade_path =  "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml"
cascade = cv2.CascadeClassifier(cascade_path)

# Get Started
bezelie.initPCA9685()
bezelie.moveCenter()

# Main Loop
with picamera.PiCamera() as camera:                         # Open Pi-Camera as camera
  with picamera.array.PiRGBArray(camera) as stream:         # Open Video Stream from Pi-Camera as stream
    camera.resolution = (600, 400)                          # Display Resolution
    camera.hflip = True                                     # Vertical Flip 
    camera.vflip = True                                     # Horizontal Flip

    while True:
      camera.capture(stream, 'bgr', use_video_port=True)    # Capture the Video Stream
      gray = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY) # Convert BGR to Grayscale
      facerect = cascade.detectMultiScale(gray,             # Find face from gray
        scaleFactor=1.9,                                    # 1.1 - 1.9 :the bigger the quicker & less acurate 
        minNeighbors=1,                                     # 3 - 6 : the smaller the more easy to detect
        minSize=(100,200),                                  # Minimam face size 
        maxSize=(300,400))                                  # Maximam face size

      if len(facerect) > 0:
        bezelie.moveHead (20)
        for rect in facerect:
          cv2.rectangle(stream.array,                       # Draw a red rectangle at face place 
            tuple(rect[0:2]),                               # Upper Left
            tuple(rect[0:2]+rect[2:4]),                     # Lower Right
            (0,0,255), thickness=2)                         # Color and thickness

      cv2.imshow('frame', stream.array)                     # Display the stream
      bezelie.moveHead (0)

      if cv2.waitKey(1) & 0xFF == ord('q'):                 # Quit operation
        break

      stream.seek(0)                                        # Reset the stream
      stream.truncate()

    cv2.destroyAllWindows()
