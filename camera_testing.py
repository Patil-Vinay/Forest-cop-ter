import picamera
import time
with picamera.PiCamera() as camera:
     camera.start_preview()
     time.sleep(1000)
     camera.stop_preview()