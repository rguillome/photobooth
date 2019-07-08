from input_controller import *
import cv2

class KeyboardController(InputController):
    
    def __init__(self, store):
        super(KeyboardController, self).__init__(store)

    def wait_for_action(self, time):
        key = cv2.waitKey(time)

        action = None

        if key % 256 == ord('s'):
            action = InputController.ACTION_SHOOT
        elif key % 256 == ord('b'):
            action = InputController.ACTION_LAST
        elif key % 256 == ord('p'):
            action = InputController.ACTION_PRINT
        elif key == 27:
            action = InputController.ACTION_EXIT

        return action