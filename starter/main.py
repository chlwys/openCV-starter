
import logging
import eel
import base64
import cv2
import numpy as py


@eel.expose
def setup():
  print("hello world")

def img_send_to_js(img, id):

 # Algo to show image in html
  ret, jpeg = cv2.imencode(".jpg",img)
  jpeg.tobytes()

  blob = base64.b64encode(jpeg) 
  blob = blob.decode("utf-8")
  eel.updateImageSrc(blob, id)()

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
