class Store():
    
    def __init__(self):
        self.last_img = None

    def store_img(self, img):
        self.last_img = img

    def get_last_img(self):
        return self.last_img