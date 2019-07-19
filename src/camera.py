from input_controller import InputController
from main import CV2_VIEWNAME
import time
import cv2
import numpy as np

MODE_SHOOT = 0
MODE_PLAY = 1
MIN_MODE = 0
MAX_MODE = 1

PAUSE_LENGTH = 10

class Camera():
    
    def __init__(self, store):
        self.store = store
        self.img = None
        self.current_mode = MODE_SHOOT

    def process_loop_img(self, video_stream, input_controller):
        pause = False
        start_pause = None

        for img in video_stream.next_img():

            action = input_controller.wait_for_action(10)
            
            if action==InputController.ACTION_EXIT:
                break
            elif action is not None:
                pause = self.process_action(action, img)

            if not pause:
                cv2.imshow(CV2_VIEWNAME, img)  
                video_stream.clean_iteration()
            elif self.current_mode == MODE_SHOOT:
                if start_pause is None :
                    start_pause = time.time()
                if time.time() == start + PAUSE_LENGTH*1000:
                    start_pause = None
                    start_pause = False
        

    def process_action(self, action, img):

        pause = None

        if action == InputController.ACTION_SHOOT :
            pause =  self.__shoot_action(img)
        elif action == InputController.ACTION_NEXT :
            pause = self.__next_action()
        elif action == InputController.ACTION_PREVIOUS :
            pause = self.__previous_action()
        elif action == InputController.ACTION_PRINT :
            pause = self.__print_action()
        elif action == InputController.ACTION_MODE :
            pause = self.__change_mode()

        return pause

    def __change_mode(self):
        self.current_mode += 1

        if self.current_mode > MAX_MODE:
           self.current_mode = MIN_MODE 

    def __next_action(self):
      
        # Here we show the next picture 
        img = self.store.get_next_img()

        if img is None:
            # Simple message : there is no history yet
            img = np.zeros((1024,1280,3), np.uint8)
            cv2.rectangle(img, (0,560), (1280,660), (255,255,255), thickness=-1, lineType=8, shift=0) 
            cv2.putText(img,'Pas encore d\'historique',(30,620), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,0),2,cv2.LINE_AA)
            cv2.imshow(CV2_VIEWNAME, img)
        else :
            #Show and ask for printing ?
            #cv2.rectangle(img, (0,560), (1280,660), (255,255,255), thickness=-1, lineType=8, shift=0) 
            #cv2.putText(img,'Voulez-vous lancer l\'impression ?',(30,620), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,0),2,cv2.LINE_AA)
            cv2.imshow(CV2_VIEWNAME, img)

        return True

    def __previous_action(self):

        # Here we show the previous picture 
        img = self.store.get_previous_img()

        if img is None:
            # Simple message : there is no history yet
            img = np.zeros((1024,1280,3), np.uint8)
            cv2.rectangle(img, (0,560), (1280,660), (255,255,255), thickness=-1, lineType=8, shift=0) 
            cv2.putText(img,'Pas encore d\'historique',(30,620), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,0),2,cv2.LINE_AA)
            cv2.imshow(CV2_VIEWNAME, img)
        else :
            #Show and ask for printing ?
            #cv2.rectangle(img, (0,560), (1280,660), (255,255,255), thickness=-1, lineType=8, shift=0) 
            #cv2.putText(img,'Voulez-vous lancer l\'impression ?',(30,620), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,0),2,cv2.LINE_AA)
            cv2.imshow(CV2_VIEWNAME, img)

        return True

    def __shoot_action(self, img):
        print("Shoot !")

        #Store in memory
        self.store.store_img(img)

        #Show and ask for printing ?
        #cv2.rectangle(img, (0,560), (1280,660), (255,255,255), thickness=-1, lineType=8, shift=0) 
        #cv2.putText(img,'Voulez-vous lancer l\'impression ?',(30,620), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,0),2,cv2.LINE_AA)
        cv2.imshow(CV2_VIEWNAME, img)
        
        return True


    def __print_action(self):
        print("Print !")
        #Retrieve from memory

        #Print call
        return False