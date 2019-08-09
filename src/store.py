import cv2
import glob
import re
import os

IMAGE_PREFIX_PATH = 'picture_'
IMAGE_EXTENSION = '.jpg'

FORMAT_FILENUMBER = '{0:04d}'

class Store():
    
    def __init__(self, output_path):
        self.output_path = output_path
        
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)
            print("Directory " , self.output_path ,  " Created ")
        else:    
            print("Directory " , self.output_path ,  " already exists")
    
        self.nav_index = self.__last_stored_index()
        self.next_photo_index = self.nav_index + 1

    def store_img(self, img):
        
        filename = self.output_path+IMAGE_PREFIX_PATH+FORMAT_FILENUMBER.format(self.next_photo_index)+IMAGE_EXTENSION
        print("Store photo whith filename :",filename)
        
        cv2.imwrite(filename,img)

        self.nav_index = self.next_photo_index
        self.next_photo_index += 1

    def get_previous_img(self):
        img = None

        if(self.nav_index > 1):
            self.nav_index -= 1
        
        img = cv2.imread(self.output_path+IMAGE_PREFIX_PATH+FORMAT_FILENUMBER.format(self.nav_index)+IMAGE_EXTENSION)

        return img, self.nav_index

    def get_next_img(self):
        img = None

        if(self.nav_index < self.next_photo_index-1):
            self.nav_index += 1
        
        img = cv2.imread(self.output_path+IMAGE_PREFIX_PATH+str(self.nav_index)+IMAGE_EXTENSION)
        
        return img, self.nav_index

    def get_last_img(self):
        img = None
        
        img_path = self.output_path+IMAGE_PREFIX_PATH+FORMAT_FILENUMBER.format(self.nav_index)+IMAGE_EXTENSION
        img = cv2.imread(img_path)

        return img, self.nav_index,img_path

    def __last_stored_index(self):

        files = glob.glob(self.output_path+IMAGE_PREFIX_PATH+"*"+IMAGE_EXTENSION)
        
        if not files :
            last_index_stored = 0
        else :
            
            files.sort()   
            last_file = files[-1]

            str_search = re.escape(self.output_path+IMAGE_PREFIX_PATH)+"([0-9]+)"+re.escape(IMAGE_EXTENSION)

            m = re.search(str_search, last_file)

            if m:
                last_index_stored = int(m.group(1))
                print("Last index found : ",last_index_stored)
            else :
                last_index_stored = 0

       
        return last_index_stored
