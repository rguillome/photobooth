from input_controller import *
from main import CV2_VIEWNAME
import time
import cv2
import numpy as np

class Camera():
    
    def __init__(self, store):
        self.store = store
        self.img = None

    def process_action(self, action, img):

        pause = None

        if action == InputController.ACTION_SHOOT :
            pause =  self.__shoot_action(img)
        elif action == InputController.ACTION_LAST :
            pause = self.__last_action()
        elif action == InputController.ACTION_PRINT :
            pause = self.__print_action()

        return pause

    def __last_action(self):
        print("Back to the bac !")
        # Here we show the last picture 
        img = self.store.get_last_img()

        if img is None:
            # Simple message : there is no history yet
            img = np.zeros((1024,1280,3), np.uint8)
            cv2.rectangle(img, (0,560), (1280,660), (255,255,255), thickness=-1, lineType=8, shift=0) 
            cv2.putText(img,'Pas encore d\'historique',(30,620), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,0),2,cv2.LINE_AA)
            cv2.imshow(CV2_VIEWNAME, img)
        else :
            #Show and ask for printing ?
            cv2.rectangle(img, (0,560), (1280,660), (255,255,255), thickness=-1, lineType=8, shift=0) 
            cv2.putText(img,'Voulez-vous lancer l\'impression ?',(30,620), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,0),2,cv2.LINE_AA)
            cv2.imshow(CV2_VIEWNAME, img)

        return True

    def __shoot_action(self, img):
        print("Shoot !")

        #Store in memory
        self.store.store_img(img)

        #Show and ask for printing ?
        cv2.rectangle(img, (0,560), (1280,660), (255,255,255), thickness=-1, lineType=8, shift=0) 
        cv2.putText(img,'Voulez-vous lancer l\'impression ?',(30,620), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,0),2,cv2.LINE_AA)
        cv2.imshow(CV2_VIEWNAME, img)
        
        return True


    def __print_action(self):
        print("Print !")
        #Retrieve from memory

        #Print call
        return False