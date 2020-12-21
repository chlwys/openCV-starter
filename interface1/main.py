# import dependencies 
import logging
import eel
import base64
import cv2
import numpy as py

img1 = cv2.imread("./web/image/img1.jpg", cv2.IMREAD_COLOR)
img2 = cv2.imread("./web/image/img2.jpg", cv2.IMREAD_COLOR)
img3 = cv2.imread("./web/image/img3.jpg", cv2.IMREAD_COLOR)

imgs = [img1, img2, img3]
count = 0

#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,1))

# set up EEL
@eel.expose
def setup():
  changeImage()


# changing photo
@eel.expose
def changeImage():
  global count 
  output = imgs[count%3]
#  blurred = cv2.bilateralFilter(imgs[count%3], 7, 100, 100)
#  edge = cv2.Canny(blurred, 200, 200, apertureSize=3, L2gradient=True)
#  opening = cv2.morphologyEx(edge, cv2.MORPH_OPEN, kernel)
#  output = opening
  img_send_to_js(output, "center")
  count = count + 1

# send image to html - do not touch
def img_send_to_js(img, id):

 # Algo to show image in html
  ret, jpeg = cv2.imencode(".jpg",img)
  jpeg.tobytes()

  blob = base64.b64encode(jpeg)
  blob = blob.decode("utf-8")
  eel.updateImageSrc(blob, id)()

# send text to html - do not touch
def text_send_to_js(val,id):
  eel.updateTextSrc(val,id)()

# start html
def start_app():
  try:
    start_html_page = 'index.html'
    eel.init('web')
    logging.info("App Started")

    eel.start('index.html', size=(1000, 700))

  except Exception as e:
    err_msg = 'Could not launch a local server'
    logging.error('{}\n{}'.format(err_msg, e.args))
    show_error(title='Failed to initialise server', msg=err_msg)
    logging.info('Closing App')
    sys.exit()

if __name__ == "__main__":
  start_app()
