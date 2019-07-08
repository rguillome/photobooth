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

PLATFORM_RPICAM = 'rpicam'
PLATFORM_WEBCAM = 'webcam'
PLATFORM_VIDEO = 'video'

CV2_VIEWNAME = 'PhotoBooth-View'

OUTPUT_DEFAULT_PATH = '/tmp/camera-out.jpg'

def main(argv):
    """
        Main function that do the Camera loop on the camera images stream

        parameters
        -------------------
        argv : should contains parameters to configure the broker
                -s : the source (rpicam, webcam, video)
                -i : input path (required if video is selected)
                -o : output path (required if headless)
                -d : headless (no feedback)
    """
    
    #Default parameters value
    source = PLATFORM_WEBCAM
    headless = False
    output_path = OUTPUT_DEFAULT_PATH
  
    try:
        opts, args = getopt.getopt(argv,"s:v:o",["source=","in_path=","output_path="])
    except getopt.GetoptError:
        print ('main.py -s <source> -i <input_path> -o <output_path>')
        sys.exit(2)

    for opt, arg in opts:
      if opt in ("-s", "--source"):
        source = arg
      elif opt in ("-i", "--input_path"):
        input_path = arg
      elif opt in ("-i", "--output_path"):
        output_path = arg

    store = st.Store()
    cam = cm.Camera(store)

    if source == PLATFORM_RPICAM:
        import picapture as cp
        video_stream = cp.PiCapture()
    elif source == PLATFORM_WEBCAM:
        import webcamcapture as wp
        video_stream = wp.WebcamCapture()
        import keyboard_controller as ki
        input_controler = ki.KeyboardController(store)
    elif source == PLATFORM_VIDEO:
        import videocapture as vp
        video_stream = vp.VideoCapture(input_path)

    
    cv2.namedWindow(CV2_VIEWNAME,cv2.WINDOW_NORMAL)

    pause = False

    for img in video_stream.next_img():

        action = input_controler.wait_for_action(10)
        
        if action==InputController.ACTION_EXIT:
            break
        elif action is not None:
            pause = cam.process_action(action, img)

        if not pause:
            cv2.imshow(CV2_VIEWNAME, img)  
            video_stream.clean_iteration()
        else:
            #PAUSE TEN SECONDS MAX if action is shoot !
            print("on pause")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main(sys.argv[1:])
