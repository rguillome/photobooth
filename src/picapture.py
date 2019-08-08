import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import io
import numpy as np
#from PIL import Image

class PiCapture(object):
    
    def __init__(self, display_resolution):
        print("Initialize Pi Camera")
        self.display_resolution = display_resolution
        self.camera = PiCamera()
        self.camera.resolution = (1920,1080)
        self.camera.framerate = 32
        self.stream  = io.BytesIO()
        time.sleep(2)

    def next_img(self):

        while True:
   
            self.camera.capture(self.stream, format='jpeg', resize = self.display_resolution)
            self.stream.seek(0)

            img = cv2.imdecode(np.fromstring(self.stream.getvalue(), dtype=np.uint8),1)

            self.__clean_iteration()
            yield img
            
    def take_picture(self) :
        self.camera.capture(self.stream, format='jpeg')
        self.stream.seek(0)
        img = cv2.imdecode(np.fromstring(self.stream.getvalue(), dtype=np.uint8),1)
        self.__clean_iteration()
        
        return img
        
    def __clean_iteration(self):
        self.stream.truncate(0)
