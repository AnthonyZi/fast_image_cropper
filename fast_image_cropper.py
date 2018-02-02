import cv2
import numpy as np
import copy
import skimage.io as skiio

colors = dict()
colors["black"] = (1,1,1)
colors["red"] = (0,1,1)
colors["white"] = (0,0,0)

class Editor(object):
    def __init__(self, image_path=None):
        if not image_path == None:
            self.set_image(image_path)

        self.xy0 = (-1,-1)
        self.button_down = False

        self.pen_size = 5
        self.color = colors["black"]

        cv2.namedWindow('FastImageCropper by Anthony')
        cv2.setMouseCallback('FastImageCropper by Anthony', self.eventhandler)

    def set_image(self, image_path):
        self.save_counter = 0
        self.image_path = image_path
        self.image = np.array(skiio.imread(image_path), dtype=np.uint8)
        self.displayed_image = copy.deepcopy(self.image)
        self.mask = np.zeros_like(self.image, dtype=np.uint8)

    def open(self):
        while(1):
            cv2.imshow('FastImageCropper by Anthony',self.displayed_image[:,:,::-1])
            k = cv2.waitKey(1) & 0xFF
            if k == ord('b'):
                self.mask[:] = 0
                self.update_displayed_image()
            elif k == ord('q'):
                return "quit"
            elif k == 27: # escape
                return "exit"
            elif k == ord('x'):
                self.mask[:] = 0
                self.update_displayed_image()
                self.save_crop()

    def close_window(self):
        cv2.destroyAllWindows()

    def save_crop(self):
        self.save_counter += 1
        fpath = self.image_path
        fpath = fpath.split("/")
        fpath[-1] = "crop_{}_".format(self.save_counter)+fpath[-1]
        fpath = "/".join(fpath)
        x0,y0 = self.xy0
        x1,y1 = self.xy1
        xx = sorted([x0,x1])
        yy = sorted([y0,y1])
        x0,x1 = xx
        y0,y1 = yy

        cropped_img = self.image[y0:y1,x0:x1,:]
        print("saving {}".format(fpath))
        skiio.imsave(fpath, cropped_img)


    def update_displayed_image(self):
        self.displayed_image = copy.deepcopy(self.image)
        idx = (self.mask==1)
        self.displayed_image[idx]=0

    def eventhandler(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.button_down = True
            self.xy0 = (x,y)

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.button_down:
                self.mask[:] = 0
                cv2.rectangle(self.mask, self.xy0, (x,y), self.color, self.pen_size)
                self.update_displayed_image()

        elif event == cv2.EVENT_LBUTTONUP:
            self.button_down = False
            self.xy1 = (x,y)
            self.mask[:] = 0
            cv2.rectangle(self.mask, self.xy0, (x,y), self.color, self.pen_size)
            self.update_displayed_image()
