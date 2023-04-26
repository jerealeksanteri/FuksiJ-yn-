"""
Sähkökilta Fuksijäynä 2023
Made by Jere Niemi :))
25.4.2023
"""

# Imports
from tkinter import *
from customtkinter import *
import cvzone
import cv2
from ultralytics import YOLO
import math
from PIL import Image, ImageTk
from dataclasses import dataclass
import time
from math import sqrt
import random
import asyncio
import psutil
import decouple

CAMERA = decouple.config("CAMERA")

# YOLO classes
CLASS_NAMES = ["person","bicycle","car","motorbike","aeroplane","bus","train","truck","boat","traffic light",
               "fire hydrant","stop sign","parking meter","bench","bird","cat","dog","horse","sheep","cow",
               "elephant","bear","zebra","giraffe","backpack","umbrella","handbag","tie","suitcase","frisbee",
               "skis","snowboard","sports ball","kite","baseball bat","baseball glove","skateboard","surfboard",
               "tennis racket","bottle","wine glass","cup","fork","knife","spoon","bowl","banana","apple","sandwich",
               "orange","broccoli","carrot","hot dog","pizza","donut","cake","chair","sofa","pottedplant","bed","diningtable",
               "toilet","tvmonitor","laptop","mouse","remote","keyboard","cell phone","microwave","oven","toaster","sink",
               "refrigerator","book","clock","vase","scissors","teddy bear","hair dier","toothbrush"]

# ?
"""
BOX_DATA = list()


def add_to_data(box):
    BOX_DATA.append(box)
    if len(BOX_DATA) > 100:
        BOX_DATA.pop(0)

"""
class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.title("ThunderVision Radar Systems")
        self.geometry("1920x1080")
        self.bind("<F11>", self.fullscreen)
        self.bind("<Escape>", self.windowed)

        self._top_bar = CTkFrame(self, width=1920, height=100)
        self._top_bar.grid(row=0, column=0)

        logo = Image.open("logo.png").resize((300, 150), Image.LANCZOS)
        logo_img = ImageTk.PhotoImage(logo)
        
        self._logo = Label(self._top_bar, image=logo_img)
        self._logo.grid(row=0, column=0, columnspan=1)


        self.radar_info = RadarInfoLeft(master=self)
        self.radar_info.grid(row=1, column=0, columnspan=2, sticky=W, padx=15)

        self.radar_info2 = RadarInfoRight(master=self)
        self.radar_info2.grid(row=1, column=3, columnspan=2, sticky=E, padx=15)



        self.radar = Radar(master=self, width=1280, height=720, radar_info1=self.radar_info, radar_info2=self.radar_info2)
        self.radar.grid(row=1, column=2, padx=0, pady=50)


        self.after(2, self.radar.show_frames)

        self.mainloop()

    def fullscreen(self, event=None):
        """ F11 key to fullscreen """
        
        self.attributes("-fullscreen", True)
        return "break"
    
    def windowed(self, event=None):
        """ Esc key to windowed mode """
        self.attributes("-fullscreen", False)
        return "break"


class RadarInfoLeft(CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.time = time.time()


        self.avg_speed_title = CTkLabel(self, text="AvgS: ").grid(sticky=W, row=0, column=0, pady=20, padx=15)
        self.x_speed_title = CTkLabel(self, text="xS: ").grid(sticky=W, row=1, column=0, pady=20, padx=15)
        self.x_gs_title = CTkLabel(self, text="xGS: ").grid(sticky=W, row=2, column=0, pady=20, padx=15)
        self.x_odr_title = CTkLabel(self, text="xODR: ").grid(sticky=W, row=3, column=0, pady=20, padx=15)
        self.xod_rating_title = CTkLabel(self, text="xOD-Rating: ").grid(sticky=W, row=4, column=0, pady=20, padx=15)
        self.xod_time_title = CTkLabel(self, text="xOD-time: ").grid(sticky=W, row=5, column=0, pady=20, padx=15)
        self.pur_x_ra_title = CTkLabel(self, text="PurXRA: ").grid(sticky=W, row=6, column=0, pady=20, padx=15)


        self.avg_speed = CTkLabel(self, text="0", width=35)
        self.avg_speed.grid(row=0, column=1, pady=20, padx=30)
        self.x_speed = CTkLabel(self, text="0", width=35)
        self.x_speed.grid(row=1, column=1, pady=20, padx=30)
        self.x_gs = CTkLabel(self, text="0", width=35)
        self.x_gs.grid(row=2, column=1, pady=20, padx=30)
        self.x_odr = CTkLabel(self, text="0", width=35)
        self.x_odr.grid(row=3, column=1, pady=20, padx=30)
        self.xod_rating = CTkLabel(self, text="0", width=35)
        self.xod_rating.grid(row=4, column=1, pady=20, padx=30)
        self.xod_time = CTkLabel(self, text="0", width=35)
        self.xod_time.grid(row=5, column=1, pady=20, padx=30)
        self.pur_x_ra = CTkLabel(self, text="0", width=35)
        self.pur_x_ra.grid(row=6, column=1, pady=20, padx=30)


class RadarInfoRight(CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.time = time.time()


        self.xZ_rating_title = CTkLabel(self, text="xZ Rating: ").grid(sticky=W, row=0, column=0, pady=20, padx=15)
        self.xd_ratio_title = CTkLabel(self, text="xD ratio: ").grid(sticky=W, row=1, column=0, pady=20, padx=15)
        self.FJ_2023_title = CTkLabel(self, text="FJ 23: ").grid(sticky=W, row=2, column=0, pady=20, padx=15)
        self.in_mar_title = CTkLabel(self, text="In Mar: ").grid(sticky=W, row=3, column=0, pady=20, padx=15)
        self.po_or_title = CTkLabel(self, text="Po-Or: ").grid(sticky=W, row=4, column=0, pady=20, padx=15)
        self.soi_ni_title = CTkLabel(self, text="sOI Ni rating: ").grid(sticky=W, row=5, column=0, pady=20, padx=15)
        self.saa_x_rik_co_title = CTkLabel(self, text="SaA rI-cKO: ").grid(sticky=W, row=6, column=0, pady=20, padx=15)


        self.xZ_rating = CTkLabel(self, text="0", width=35)
        self.xZ_rating.grid(sticky=W, row=0, column=1, pady=20, padx=15)
        self.xd_ratio = CTkLabel(self, text="0", width=35)
        self.xd_ratio.grid(sticky=W, row=1, column=1, pady=20, padx=15)
        self.FJ_2023 = CTkLabel(self, text="0", width=35)
        self.FJ_2023.grid(sticky=W, row=2, column=1, pady=20, padx=15)
        self.in_mar = CTkLabel(self, text="0", width=35)
        self.in_mar.grid(sticky=W, row=3, column=1, pady=20, padx=15)
        self.po_or = CTkLabel(self, text="0", width=35)
        self.po_or.grid(sticky=W, row=4, column=1, pady=20, padx=15)
        self.soi_ni = CTkLabel(self, text="0", width=35)
        self.soi_ni.grid(sticky=W, row=5, column=1, pady=20, padx=15)
        self.saa_x_rik_co = CTkLabel(self, text="0", width=35)
        self.saa_x_rik_co.grid(sticky=W, row=6, column=1, pady=20, padx=15)


class Radar(Label):
    def __init__(self, master, width, height, radar_info1, radar_info2):
        super().__init__(master=master, text="")

        self.cap = cv2.VideoCapture(int(CAMERA))
        self.cap.set(3, width)
        self.cap.set(4, height)
        self.model = YOLO("..yolo_weights/yolov8n.pt")
        self.radar_info1 = radar_info1
        self.radar_info2 = radar_info2
        
    def show_stats(self, box):
        """ Show "stats"
        :param box: box data in the picture
        """
        info1 = self.radar_info1
        info2 = self.radar_info2
        x1, y1, x2, y2 = box.xyxy[0]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        info1.avg_speed.configure(text=round(sqrt(y2),2))
        info1.x_gs.configure(text=str(round(random.random()*100,2)))
        info1.x_odr.configure(text=str(random.randint(9,100)))
        info1.x_speed.configure(text=str(round(psutil.cpu_freq().current,2)))
        info1.xod_rating.configure(text=str(psutil.cpu_percent()))
        info1.xod_time.configure(text=str(round(psutil.boot_time()/1000000,2)))
        info1.pur_x_ra.configure(text=str(round(random.randrange(0,100,2),2)))


        info2.xZ_rating.configure(text=str(random.randbytes(1)))
        info2.xd_ratio.configure(text="5/5")
        info2.FJ_2023.configure(text=str(math.ceil((box.conf[0]*100)))+"%")
        info2.in_mar.configure(text=str(psutil.net_connections()[1].pid))
        info2.po_or.configure(text=str(psutil.net_connections()[1].status))
        info2.soi_ni.configure(text=str(psutil.net_connections()[1].family))
        info2.saa_x_rik_co.configure(text=str(psutil.net_connections()[1].type))


    def show_frames(self):
        """ Running loop which loops the camera view and handles the "stats" shown in the view
        """
        while 1:
            success, img = self.cap.read()
            results = self.model(img, stream=True)
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    
                    # Class Name
                    cls = box.cls[0]

                    if CLASS_NAMES[int(cls)] in ["person","cell phone"]:

                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                        w, h = x2-x1, y2-y1
                        # Rectangle
                        rect = cvzone.cornerRect(img,(x1,y1,w,h), l=15)
                        
                        # Confidence
                        conf = math.ceil((box.conf[0]*100))/100
                        
                        #add_to_data({ "time": time.time(), "box": box })
                        
                        self.show_stats(box)
                        
                        # Udate frames
                        self.radar_info1.update()
                        self.radar_info2.update()

                        cvzone.putTextRect(img, f"{CLASS_NAMES[int(cls)]} {conf}",(max(0, x1), max(35, y1-20)), scale=2)

            # To "Label"
            image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            tkimg = ImageTk.PhotoImage(image)
            self.config(image=tkimg)
            self["image"] = tkimg
            
            # Update radar view
            self.master.update()


class Application():
    def __init__(self) -> None:
        self.win = MainWindow()





def main():
    Application()

if __name__ == "__main__":
    main()