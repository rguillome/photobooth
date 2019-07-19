import cv2

IMAGE_PREFIX_PATH = '/photobooth_'
IMAGE_EXTENSION = '.jpg'

class Store():
    
    def __init__(self, output_path):
        self.next_photo_index = self.__last_stored_index() + 1
        self.nav_index = self.next_photo_index
        self.output_path = output_path

    def store_img(self, img):
        cv2.imwrite(self.output_path+IMAGE_PREFIX_PATH+str(self.next_photo_index)+IMAGE_EXTENSION,img) 
        self.next_photo_index += 1
        self.nav_index = self.next_photo_index

    def get_previous_img(self):
        img = None

        if(self.nav_index > 0 and self.next_photo_index > 0):
            self.nav_index -= 1
            img = cv2.imread(self.output_path+IMAGE_PREFIX_PATH+str(self.nav_index)+IMAGE_EXTENSION)

        return img

    def get_next_img(self):
        img = None

        if(self.nav_index < self.next_photo_index-1):
            self.nav_index += 1
            img =  cv2.imread(self.output_path+IMAGE_PREFIX_PATH+str(self.nav_index)+IMAGE_EXTENSION)

        return img
        
    def __last_stored_index(self):
        last_index_stored = 0
        return last_index_stored