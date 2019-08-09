from keyboard_controller import KeyboardController
from input_controller import *
import cv2
import time
import RPi.GPIO as GPIO

GPIO_SHOOTBUTTON=25
GPIO_REDLED=12

class RpiController(KeyboardController):
    
    def __init__(self, store):
        super(RpiController, self).__init__(store)
        GPIO.setmode(GPIO.BCM)
        
        # Shoot button
        GPIO.setup(GPIO_SHOOTBUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        #TODO remove when tested
        GPIO.setup(GPIO_REDLED, GPIO.OUT)

    def wait_for_action(self, waitingTime):
        
        time.sleep(waitingTime/1000)
        action = None
        
        button_shoot_state = GPIO.input(GPIO_SHOOTBUTTON)
        
        if button_shoot_state == False:
            GPIO.output(GPIO_REDLED, True)
            time.sleep(0.2)
            GPIO.output(GPIO_REDLED, False)
            
            action = InputController.ACTION_SHOOT
        
        if not action:
            action = super(RpiController,self).wait_for_action(waitingTime)

        return action

    def release(self):
        GPIO.cleanup()
