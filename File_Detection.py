import cv2
import pandas as pd

class ColorDetection:
    
    def __init__(self, image):
        img_path = image
        self.img = cv2.imread(img_path)
        # declaring global variables (are used later on)
        self.clicked = False
        self.r = self.g = self.b = self.x_pos = self.y_pos = 0
        
        # Reading csv file with pandas and giving names to each column
        self.index = ["color", "color_name", "hex", "R", "G", "B"]
        self.csv = pd.read_csv('colors.csv', names=self.index, header=None)
    
    
    # function to calculate minimum distance from all colors and get the most matching color
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
            self.clicked = True
            self.x_pos = x
            self.y_pos = y
            self.b, self.g, self.r = self.img[y, x]
            self.b = int(self.b)
            self.g = int(self.g)
            self.r = int(self.r)
    
    def start_color_detection(self):
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.draw_function)
        
        while True:
            
            try:
                cv2.imshow("image", self.img)
                if self.clicked:
            
                    # cv2.rectangle(image, start point, endpoint, color, thickness)-1 fills entire rectangle
                    cv2.rectangle(self.img, (20, 20), (750, 60), (self.b, self.g, self.r), -1)
            
                    # Creating text string to display( Color name and RGB values )
                    text = self.get_color_name(self.r, self.g, self.b) + ' R=' + str(self.r) + ' G=' + str(self.g) + ' B=' + str(self.b)
            
                    # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
                    cv2.putText(self.img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
            
                    # For very light colours we will display text in black colour
                    if self.r + self.g + self.b >= 600:
                        cv2.putText(self.img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
            
                    self.clicked = False
            
                # Break the loop when user hits 'esc' key
                if cv2.waitKey(20) & 0xFF == 27:
                    break
            except:
                break
    
        cv2.destroyAllWindows()
