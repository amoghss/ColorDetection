from File_Detection import *
from Live_Detection import *
from tkinter import *
from tkinter import filedialog
import eel
import IPython
import cv2

eel.init('web')

try:
    @eel.expose
    def localFiles():
        
        r=Tk()
        
        filename=filedialog.askopenfilename()
        r.destroy()
        obj=ColorDetection(filename)
        obj.start_color_detection()
        
    @eel.expose
    def livePrediction():
        
        obj=VideoColorDetection()
        obj.start_live_detection()

except:
    print("Ignoring the expose as already exposed to JS")

eel.start('index.html', size=(1000, 600))


