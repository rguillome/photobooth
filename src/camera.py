from input_controller import InputController
from main import CV2_VIEWNAME, CV2_WINDOW_WIDTH, CV2_WINDOW_HEIGHT
import time
import cv2
import numpy as np
import os
from threading import Thread

MODE_SHOOT = 0
MODE_PLAY = 1
MIN_MODE = 0
MAX_MODE = 1

PAUSE_LENGTH = 10

CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080

########################################
### Classes
########################################
class ShootRun(Thread):

    """This Thread will run a function with args ."""

    def __init__(self, camera):
        Thread.__init__(self)
        self.camera = camera

    def run(self):
        """Code to execute while thread is running : 
            - each second, print the descending counter
            - at the end, take a picture
        """
        print("Start counter")
        for count in range(1,-1,-1) :
            self.camera.counter = count
            time.sleep(1)
        
        self.camera.counter = None
        self.camera.shoot = True

class Camera():
    
    def __init__(self, store, video_stream, input_controller, display_resolution):
        self.store = store
        self.current_mode = MODE_SHOOT
        self.video_stream = video_stream
        self.input_controller = input_controller
        self.camera_resolution_x,self.camera_resolution_y = display_resolution
        self.counter = None
        self.shoot = False
        self.display_resolution = display_resolution

    def launch(self):

        # Loop over actions :s
         while True :
            action = self.input_controller.wait_for_action(10)

            if action==InputController.ACTION_EXIT:
                os._exit(1)
            else:                
                if self.current_mode == MODE_SHOOT:
                    self.process_shoot(action)
                elif self.current_mode == MODE_PLAY:
                    self.process_play(action)

    def print_mode(self, img):

        mode = None

        if self.current_mode == MODE_PLAY:
            mode="Lecture"
        elif self.current_mode == MODE_SHOOT:
            mode="Photo"
            
        x = self.camera_resolution_x
        cv2.rectangle(img, (int(x-x*0.25),10), (int(x-x*0.05+x*0.01),50), (255,255,255), thickness=-1, lineType=8, shift=0) 
        cv2.putText(img,mode,(int(x-x*0.25+x*0.01),45), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),2,cv2.LINE_AA)  


    def process_play(self, action):

        if action is not None:
            self.process_action_play(action)

    def process_shoot(self, action):

        img = next(self.video_stream.next_img())
        
        if self.counter is not None:

            if self.counter > 0 :
                cv2.rectangle(img, (int(self.camera_resolution_x/2)-30,self.camera_resolution_y-50), 
                    (int(self.camera_resolution_x/2)+30,self.camera_resolution_y-10), (255,255,255), 
                    thickness=-1, lineType=8, shift=0) 
                cv2.putText(img,str(self.counter),(int(self.camera_resolution_x/2)-17,
                    self.camera_resolution_y-18), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),2,cv2.LINE_AA)
            elif self.counter == 0 :
                cv2.rectangle(img, (int(self.camera_resolution_x/2)-50,self.camera_resolution_y-50), 
                    (int(self.camera_resolution_x/2)+120,self.camera_resolution_y-10), (255,255,255), 
                    thickness=-1, lineType=8, shift=0) 
                cv2.putText(img,"Ouistiti !",(int(self.camera_resolution_x/2)-28,
                    self.camera_resolution_y-18), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),2,cv2.LINE_AA)
        
        if self.shoot:
            self.shoot_action()
            self.shoot = False
        else:
            self.print_mode(img)
            cv2.imshow(CV2_VIEWNAME, img)  

        if action is not None:
            self.process_action_shoot(action)   

    def process_action_shoot(self, action):
        if action == InputController.ACTION_SHOOT :
            thread_shoot = ShootRun(self)
            thread_shoot.start()
        elif action == InputController.ACTION_MODE :
            self.__change_mode()
        else :
            self.__show_msg('Action non autorisee dans ce mode')

    def process_action_play(self, action):

        if action == InputController.ACTION_SHOOT :
            self.__change_mode()
            thread_shoot = ShootRun(self)
            thread_shoot.start()
        elif action == InputController.ACTION_NEXT :
            self.__next_action()
        elif action == InputController.ACTION_PREVIOUS :
            self.__previous_action()
        elif action == InputController.ACTION_PRINT :
            self.__print_action()
        elif action == InputController.ACTION_MODE :
            self.__change_mode()
        else :
            self.__show_msg('Action non autorisee dans ce mode')
            
        
    def __change_mode(self):
        self.current_mode += 1

        if self.current_mode > MAX_MODE:
           self.current_mode = MIN_MODE
        
        if self.current_mode == MODE_PLAY:
            self.last_action()
        

    def __next_action(self):
      
        # Here we show the next picture 
        img, index = self.store.get_next_img()

        self.__show_img(img, index)

    def __previous_action(self):

        # Here we show the previous picture 
        img, index = self.store.get_previous_img()

        self.__show_img(img, index)

    def last_action(self):

        # Here we show the previous picture 
        img, index = self.store.get_last_img()

        self.__show_img(img, index)

    def __show_img(self, img, index):
        
        img = cv2.resize(img, (self.camera_resolution_x, self.camera_resolution_y)) 

        self.print_mode(img)

        if img is None:
            self.__show_msg('Pas encore d\'historique')
        else :
            cv2.rectangle(img, (int(self.camera_resolution_x/2)-50,self.camera_resolution_y-50), 
                (int(self.camera_resolution_x/2)+120,self.camera_resolution_y-10), (255,255,255), 
                thickness=-1, lineType=8, shift=0) 
            cv2.putText(img,"Photo "+str(index),(int(self.camera_resolution_x/2)-28,
                self.camera_resolution_y-18), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),2,cv2.LINE_AA)
            cv2.imshow(CV2_VIEWNAME, img)

    def __show_msg(self, msg):
        width = self.camera_resolution_x
        height = self.camera_resolution_y
        img = np.zeros((height, width,3), np.uint8)
        cv2.rectangle(img, (0,int(height/2-height/8)), (width,int(height/2+height/8)), (255,255,255), thickness=-1, lineType=8, shift=0) 
        cv2.putText(img,msg,(int(width*0.01),int(height/2-height/16)), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),2,cv2.LINE_AA)
        cv2.imshow(CV2_VIEWNAME, img)


    def shoot_action(self):
        print("Shoot !")

        img = self.video_stream.take_picture()

        #Store in memory
        self.store.store_img(img)

        # Passage en mode play
        # TODO : seulement pour 10/20 secondes ?
        self.current_mode = MODE_PLAY
        self.last_action()
        

    def __print_action(self):
        print("Print !")
        #Retrieve from memory

        #Print call
