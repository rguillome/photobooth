import cv2

class WebcamCapture(object):
    def __init__(self):
        print("Initialize WebCam")
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

    def next_img(self):
        while True:
            ret, img = self.camera.read()
            yield img

    def get_img_size(self):
        return (int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    def clean_iteration(self):
        None

