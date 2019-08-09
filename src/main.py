#!/usr/bin/python

"""
    Main module of the photobooth project
"""
import sys
import getopt
import cv2
import numpy as np
import store as st
import camera as cm
from input_controller import InputController
import datetime

PLATFORM_RPICAM = 'rpicam'
PLATFORM_WEBCAM = 'webcam'
PLATFORM_VIDEO = 'video'

CV2_VIEWNAME = 'PhotoBooth-View'
CV2_WINDOW_WIDTH = 640
CV2_WINDOW_HEIGHT = 480

from sys import platform
if platform == "linux" or platform == "linux2" or platform == "darwin":
    OUTPUT_DEFAULT_PATH = '/tmp/photobooth/'    
elif platform == "win32":
    OUTPUT_DEFAULT_PATH = 'c:\\tmp\\photobooth\\'

def main(argv):
    """
        Main function that do the Camera loop on the camera images stream

        parameters
        -------------------
        argv : should contains parameters to configure the broker
                -s : the source (rpicam, webcam, video)
                -i : input path (required if video is selected)
                -o : output path (required if headless)
                -f : fullscreen
    """
    
    #Default parameters value
    source = PLATFORM_WEBCAM
    output_path = OUTPUT_DEFAULT_PATH
    fullscreen = False
  
    try:
        opts, args = getopt.getopt(argv,"s:v:o:f",["source=","in_path=","output_path="])
    except getopt.GetoptError:
        print ('main.py -s <source> -i <input_path> -o <output_path> -f')
        sys.exit(2)

    for opt, arg in opts:
      if opt in ("-s", "--source"):
        source = arg
      elif opt in ("-i", "--input_path"):
        input_path = arg
      elif opt in ("-i", "--output_path"):
        output_path = arg
      elif opt in ("-f", "--fullscreen"):
        fullscreen = True

    store = st.Store(output_path)    
    
    if not fullscreen:
        cv2.namedWindow(CV2_VIEWNAME,cv2.WINDOW_NORMAL)
        cv2.resizeWindow(CV2_VIEWNAME,CV2_WINDOW_WIDTH,CV2_WINDOW_HEIGHT)
        dimension = (CV2_WINDOW_WIDTH,CV2_WINDOW_HEIGHT)
    else:
        cv2.namedWindow(CV2_VIEWNAME,cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(CV2_VIEWNAME,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        
        import Tkinter
        root = Tkinter.Tk()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        dimension = (width,height)

    if source == PLATFORM_RPICAM:
        import picapture as cp
        video_stream = cp.PiCapture(dimension)
        import rpi_controller as ki
        input_controller = ki.RpiController(store)
    elif source == PLATFORM_WEBCAM:
        import webcamcapture as wp
        video_stream = wp.WebcamCapture(dimension)
        import keyboard_controller as ki
        input_controller = ki.KeyboardController(store)
    elif source == PLATFORM_VIDEO:
        import videocapture as vp
        video_stream = vp.VideoCapture(input_path)

    cam = cm.Camera(store, video_stream, input_controller, dimension)
    cam.launch()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main(sys.argv[1:])
