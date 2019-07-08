import time

WAIT_TIME_UNIT_SECONDS=1000

class InputController(object):
    ACTION_EXIT = 0
    ACTION_SHOOT = 1
    ACTION_LAST = 2
    ACTION_PRINT = 3

    def __init__(self, store):
        print("Initialize InputController")
        self.store = store

    def wait_for_action(self, time):
        """
        Wait "time" milliseconds before selecting and action

        parameters
        -------------------
        time : time in milliseconds it'll wait for a new action
        """
        
        time.sleep(time/WAIT_TIME_UNIT_SECONDS)


        return None
        
   
    def get_action(self):
        return None
        

        

