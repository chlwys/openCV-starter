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
import face_recognition


# Set name of Video file to open. Leave name "" to open camera
video_name = ""

vidName = cv2.VideoCapture(video_name)

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("./web/image/obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
 
# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("./web/image/biden.png")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
 
# Load a 3rd sample picture and learn how to recognize it.
hillary_image = face_recognition.load_image_file("./web/image/hillary.png")
hillary_face_encoding = face_recognition.face_encodings(hillary_image)[0]

known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    hillary_face_encoding,
]

known_face_names = [
    "Barack Obama",
    "Joe Biden",
    "Hillary Clinton"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
 
process_this_frame = True

# Read Images
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
 global process_this_frame, known_face_encodings, known_face_names, face_names
 
 while True:

  success, frame = camera.get_frame()
  
  # Resize frame of video to 1/4 size for faster face recognition processing
  small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
 
  # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
  rgb_small_frame = small_frame[:, :, ::-1]
 
  # Only process every other frame of video to save time
  if process_this_frame:
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    face_names = []
    
    for face_encoding in face_encodings:
      # See if the face is a match for the known face(s)
      matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
      name = "Unknown"
 
      # Matches the known face with the smallest distance to the new face
      face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
      best_match_index = np.argmin(face_distances)
      if matches[best_match_index]:
        name = known_face_names[best_match_index]
 
      face_names.append(name)
    
  process_this_frame = not process_this_frame
 
  # Display the results
  for (top, right, bottom, left), name in zip(face_locations, face_names):
    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
    top *= 4
    right *= 4
    bottom *= 4
    left *= 4
 
    # Draw a box around the face
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
 
    # Draw a label with a name below the face
    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
  yield frame



# Stop Video Caturing
# Do not touch
@eel.expose
def stop_video_feed():
  x.stop_capturing()
  nametext = ""
  for i in range(len(face_names)):
    if (i==0):
      nametext = face_names[0]
    else:
      nametext = nametext + ", " + face_names[i]
    
  text_send_to_js("Video Stopped", "p2")
  text_send_to_js("The following people are detected: " + str(nametext), "p3")

  
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