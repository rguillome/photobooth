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
        self.camera.resolution = (2592,1944)
        self.camera.framerate = 5
        self.stream  = io.BytesIO()
        time.sleep(0.1)

    def next_img(self):
        
        for frame in self.camera.capture_continuous(self.stream, format='jpeg', resize = self.display_resolution, use_video_port = True):
   
            #self.camera.capture(self.stream, format='jpeg')
            self.stream.truncate()
            self.stream.seek(0)
        
            img = cv2.imdecode(np.fromstring(self.stream.getvalue(), dtype=np.uint8),1)
            #self.__clean_iteration()
            yield img
            
    def take_picture(self) :
        self.camera.capture(self.stream, format='jpeg')
        self.stream.seek(0)
        img = cv2.imdecode(np.fromstring(self.stream.getvalue(), dtype=np.uint8),1)
        self.__clean_iteration()
        
        return img
        
    def __clean_iteration(self):
        self.stream.truncate(0)
