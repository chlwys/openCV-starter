import logging
import sys
from tkinter import Tk, messagebox
import eel
import base64
import time
import os
import json
import cv2
import numpy as np
from camera import VideoCamera

# Read Images
video_name = "./web/image/justin.mp4"
img = cv2.imread("./web/image/empty.png",cv2.IMREAD_GRAYSCALE)

# Setup the images to display in html file
@eel.expose
def setup():
   img_send_to_js(img, "output")
 
#  Your code depend on image processing
# This is a sample code to change 
# and send processed image to JavaScript  
@eel.expose
def video_feed():
  y = process(x)
  text_send_to_js("Video Started", "p2")
  for frame in y:
  #    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    img_send_to_js(frame, "output")


def process(camera):
 
  while True:
 
    success, frame = camera.get_frame()

    yield frame



# Stop Video Caturing
# Do not touch
@eel.expose
def stop_video_feed():
  x.stop_capturing()

  
# Restart Video Caturing
# Do not touch
@eel.expose
def restart_video_feed():
  x.restart_capturing()
  text_send_to_js("Video Started", "p2")
  
# Send text from python to Javascript 
# Do not touch
def text_send_to_js(val,id):
  eel.updateTextSrc(val,id)()

# Send image from python to Javascript 
# Do not touch
def img_send_to_js(img, id):
  if np.shape(img) == () :
    
    eel.updateImageSrc("", id)()
  else:
    ret, jpeg = cv2.imencode(".jpg",img)
    jpeg.tobytes()
    blob = base64.b64encode(jpeg) 
    blob = blob.decode("utf-8")
    eel.updateImageSrc(blob, id)()

# Start function for app
# Do not touch
def start_app():
  try:
    start_html_page = 'index.html'
    eel.init('web')
    logging.info("App Started")

    eel.start('index.html', size=(1000, 800))

  except Exception as e:
    err_msg = 'Could not launch a local server'
    logging.error('{}\n{}'.format(err_msg, e.args))
    show_error(title='Failed to initialise server', msg=err_msg)
    logging.info('Closing App')
    sys.exit()

if __name__ == "__main__":
  x = VideoCamera(video_name)
  start_app()