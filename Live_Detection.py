from tkinter import *
from tkinter import filedialog
import eel
import cv2
import pandas as pd


class VideoColorDetection:

    def __init__(self):
        self.clicked = False
        self.r = self.g = self.b = self.x_pos = self.y_pos = 0
        self.index = ["color", "color_name", "hex", "R", "G", "B"]
        self.csv = pd.read_csv('colors.csv', names=self.index, header=None)
        self.img=None
    
    def get_color_name(self, R, G, B):
        minimum = 10000
        for i in range(len(self.csv)):
            d = abs(R - int(self.csv.loc[i, "R"])) + abs(G - int(self.csv.loc[i, "G"])) + abs(B - int(self.csv.loc[i, "B"]))
            if d <= minimum:
                minimum = d
                cname = self.csv.loc[i, "color_name"]
        return cname
    
    
    # function to get x,y coordinates of mouse double click
    def draw_function(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            #global b, g, r, x_pos, y_pos, clicked
            clicked = True
            self.x_pos = x
            self.y_pos = y
            self.b, self.g, self.r = self.img[y, x]
            self.b = int(self.b)
            self.g = int(self.g)
            self.r = int(self.r)
            print(self.get_color_name(self.r, self.g, self.b))
    
    def start_live_detection(self):
        cap = cv2.VideoCapture(0)
        while True:
            _, self.img = cap.read()
            cv2.namedWindow('image')
            cv2.setMouseCallback('image', self.draw_function)
            
            cv2.rectangle(self.img, (20, 20), (750, 60), (self.b, self.g, self.r), -1)
            text = self.get_color_name(self.r, self.g, self.b) + ' R=' + str(self.r) + ' G=' + str(self.g) + ' B=' + str(self.b)
            cv2.putText(self.img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
            
            if self.r + self.g + self.b >= 600:
                cv2.putText(self.img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
            
            cv2.imshow("image", self.img)                                          
            
            if cv2.waitKey(1) & 0xFF == ord('q'):                               #Press q to exit
                  break
        
        cap.release()
        cv2.destroyAllWindows()
        
    