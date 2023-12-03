# This Python file uses the following encoding: utf-8
#-------------------------##NOTE##------------------#
#code lines with '##' are parts of code which will be implemented later on
#code lines with '# are comments(documentation)
#logo courtesy to Lagot Design. Check it out on www.flaticon.com
#logos taken from www.flaticon.com
#-------------------------##NOTE##------------------#
import os
import sys
from datetime import datetime as dt

import numpy as np
from cv2 import IMREAD_GRAYSCALE, Canny, imread, imwrite
from numpy import argwhere as arg
from PIL import Image as im
from PySide6.QtCore import QDateTime, QTimer
from PySide6.QtGui import QIcon, QPixmap, QWindow
from PySide6.QtWidgets import (QApplication, QColorDialog, QFileDialog, QLabel,
                               QMainWindow)

from ui_form import Ui_MainWindow
from ui_secondmainwindow import Ui_SecondMainWindow

#open log file to store data
LOGFile=open("D:\\Intership\\Renovus\\GUI\\GUI_Basic\\LOGFile.txt","a")
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

#------------code beginning----------------#

        self.setIcon()
        self.setWindowTitle("GUI BASIC")
        self.ui.loadFile.clicked.connect(self.loadImage)
        self.ui.squareBox.clicked.connect(self.showProcessedImage)
        self.ui.clearBtn.clicked.connect(self.clear)
        self.ui.rhombusBox.clicked.connect(self.rundiag)
        self.ui.FSOriginal.clicked.connect(self.showFullScreenOriginal)
        self.ui.FSProcessed.clicked.connect(self.showFullScreenProcessed)
        self.ui.cntrBtn.clicked.connect(self.processedCenter)
        self.ui.history.clicked.connect(self.show_history)
        self.timer=QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(100)
        self.updateDateTime()
        self.ui.datetime.setText(self.formatted_date_time)
        self.updateDateTime()

    def setIcon(self):
        appicon=QIcon("D:\\Intership\\Renovus\\GUI\\GUI_Basic\\assets\\Icons\\book.png")
        self.setWindowIcon(appicon)

    def updateDateTime(self):#displays date
        current_date_time = QDateTime.currentDateTime()
        self.formatted_date_time = current_date_time.toString("yyyy-MM-dd")

    def clear(self):#clears the image on main screen
        
        if self.upload==True:
            pixmap=QPixmap("D:\\Intership\\Renovus\\GUI\\GUI_Basic\\assets\\Icons\\noImageAvailable.png")
            self.ui.orgImageDisp.setPixmap(pixmap)
            self.ui.top.setText(" ")
            self.ui.timeDisplay.setText(" ")
            self.ui.bottom.setText(" ")
            self.ui.right.setText(" ")
            self.ui.left.setText(" ")
            self.ui.plainTextEdit.setPlainText(" ")
            self.ui.Radius.setPlainText(" ")
            self.ui.IR.setPlainText(" ")
            self.ui.thick.setPlainText(" ")
            self.ui.ID.setPlainText(" ")
            self.ui.center.setPlainText(" ")

            pixmap=QPixmap("D:\\Intership\\Renovus\\GUI\\GUI_Basic\\assets\\Icons\\noImageAvailable.png")
            self.ui.processedImgDIsplay.setPixmap(pixmap)
            self.ui.top.setText(" ")
            self.ui.timeDisplay.setText(" ")
            self.ui.bottom.setText(" ")
            self.ui.right.setText(" ")
            self.ui.left.setText(" ")
            self.ui.plainTextEdit.setPlainText(" ")
            self.ui.Radius.setPlainText(" ")
            self.ui.IR.setPlainText(" ")
            self.ui.thick.setPlainText(" ")
            self.ui.ID.setPlainText(" ")
            self.ui.center.setPlainText(" ")


    def loadImage(self):# gets the image path
        file_dialog = QFileDialog(self)
        file_path,_ = file_dialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.bmp)")

        if file_path:
            pixmap = QPixmap(file_path)
            self.ui.orgImageDisp.setPixmap(pixmap)
            self.last_loaded_path=file_path
            self.ui.FilePath.setText(f"path:{self.last_loaded_path}")
        self.upload=True
        
    def rundiag(self):
        self.component_diagonal(self.last_loaded_path)

    def showProcessedImage(self):
            self.process_image(self.last_loaded_path)
    
    def processedCenter(self):
        self.find_center(self.last_loaded_path)

    def showFullScreenOriginal(self):
        os.startfile(self.last_loaded_path)
    #     self.window=QMainWindow()
    #     self.ui=Ui_SecondMainWindow()
    #     self.ui.setupUi(self.window)
    #     self.window.showMaximized()
    #     pixmap=QPixmap(self.last_loaded_path)
    #     self.ui.SecondFSO.setPixmap(pixmap)

    def showFullScreenProcessed(self):
        os.startfile(self.file_name)
        # self.window=QMainWindow()
        # self.ui=Ui_SecondMainWindow()
        # self.ui.setupUi(self.window)
        # self.window.showMaximized()
        # pixmap=QPixmap(self.file_name)
        # self.ui.SecondFSO.setPixmap(pixmap)
    
    def displayProcessed(self,path): #displayes the processed image in main window
        pixmap=QPixmap(path)
        self.ui.processedImgDIsplay(pixmap)
    ## def open_second(self):
        ## self.window=QMainWindow()
        ## self.ui=Ui_SecondMainWindow()
        ##self.ui.setupUi(self.window)
        ## self.window.show()
        ## self.ui.realimage.setPixmap(QPixmap(self.last_loaded_path))
        ## self.process_image(self.last_loaded_path)
    
    def show_history(self): #displays the logfile
        self.LOGFile=open("LOGFile.txt","a")
        os.startfile('LOGFile.txt')

    def process_image(self,path): #Processes image,Bounding Box, ID , OD, Thickness
        self.present=False

        #setting up colors Green-OD, Red-ID,Blue-Thickness
        green=(0,255,0)
        blue=(0,0,255)
        red=(255,0,0)
        
        #ROI points
        rx1,ry1,rx2,ry4=174,247,1850,1540
        start=dt.now() #start the time 
        LOGFile=open("LOGFile.txt","a") #open Logfile to store data
        LOGFile.write("Selected Image :"+os.path.basename(path))
        LOGFile.write("\n//Start time ://"+str(start)+"\n")
        gray_image=imread(path,IMREAD_GRAYSCALE) #convert input image to grayscale
        edgedetect=Canny(gray_image,100,200)#perform canny edge detection
        imwrite("detectededge.bmp",edgedetect) #rewrite image with the edge detection
        edge_detected=im.open("detectededge.bmp")#saving the edge detected image

        #------------TOP coordinates extraction---------------#
        edge_array = np.array(edge_detected)
        mask = (edge_array[ry1:ry4-1, rx1:rx2-1] == 255)
        # Find the indices where the mask is True
        indices = np.argwhere(mask)
        if indices.size > 0:
            y1, x1 = indices[0] + np.array([ry1, rx1])
            LOGFile.write(f"Top Coordinate:{x1},{y1}\n")#writing into logfile
        self.ui.top.setText(f"({x1},{y1})")#displaying top coordinates on mainscreen

        #------------BOTTOM coordinates extraction---------------#
        y2, x2 = None, None
        edge_array = np.array(edge_detected)
        for i in range(ry4 - 1, ry1 - 1, -1):
            row_slice = edge_array[i, rx1 - 1:rx2 - 1][::-1]
            if np.any(row_slice == 255):
                x2 = rx1 - 1 + len(row_slice) - 1 - np.argmax(row_slice == 255)
                y2 = i
                break
        LOGFile.write(f"Bottom Coordinate:({x2},{y2})\n")#logging bottom coordinates
        self.ui.bottom.setText(f"({x2},{y2})")#displaying bottom coordinates on mainscreen
        centerX=round((x1+x2)/2) #calculate center of x axis
        centerY=round((y1+y2)/2) #calculate center of y axis
        radius=centerY-y1 #calculate the radius
        #find left and right side of x axis
        # x3=centerX-radius
        # x4=centerX+radius

        #------------LEFT coordinates extraction---------------#
        i = rx1
        while i < centerX:
            color = edge_array[centerY, i]
            if color != 0:
                x3 = i
                break
            i += 1
        LOGFile.write(f"Left Coordinate:{x3},{centerY}\n") #logging the left coordinates
        self.ui.left.setText(f"{x3},{centerY}")#displaying the left coordinates on the main screen

        #------------RIGHT coordinates extraction---------------#
        i = rx2
        while i > centerX:
            color = edge_array[centerY, i]
            if color != 0:
                x4 = i
                break
            i -= 1
        LOGFile.write(f"Right Coordinate:{x4},{centerY}\n")#logging right coordinates
        self.ui.right.setText(f"{x4},{centerY}") #displaying the right coordinates on the main screen
        
        #to get ID and IR
        id=centerX
        while id < x4:
            color = edge_array[centerY, id]
            if color != 0:
                xi4 = id
                break
            id += 1

        jd=centerX
        while jd > x3:
            color = edge_array[centerY, jd]
            if color != 0:
                xj3 = jd
                break
            jd -= 1

        normal_image=im.open(path) #opening the un-modified input image using PIL module
        
        #------------Bounding box operation---------------#
        i=x3
        while(i<x4):
            normal_image.putpixel((i,y1),green)
            normal_image.putpixel((i,y2),green)
            i=i+1

        j=y1
        while(j<y2):
            normal_image.putpixel((x3,j),green)
            normal_image.putpixel((x4,j),green)
            j=j+1

        i=xj3
        while(i<xi4):
            normal_image.putpixel((i,centerY),red)
            i+=1
        
        i=xi4
        while(i<x4):
            normal_image.putpixel((i,centerY),blue)
            i+=1

        normal_image.save("check.bmp")#saving the image
        self.ui.processedImgDIsplay.setPixmap(QPixmap("check.bmp"))#display on main screen
        
        self.file_name="check.bmp"
        
        LOGFile.write(f"Diameter: {self.get_dia(y1, y2)} mm , Radius: {self.get_dia(y1,y2)/2} mm")#getting the OD and OR
        LOGFile.write(f"Internal Diameter: {self.get_dia(xj3, xi4)} mm , Internal Radius: {self.get_dia(xj3,xi4)/2} mm") #getting the ID and IR
        self.ui.plainTextEdit.setPlainText(f"{round(self.get_dia(y1,y2),2)} mm")
        self.ui.ID.setPlainText(f"{round(self.get_dia(xj3,xi4),2)} mm")
        self.ui.thick.setPlainText(f"{round(self.get_dia(xi4,x4),2)} mm")
        self.ui.IR.setPlainText(f"{round(self.get_dia(xj3,xi4)/2,2)} mm")
        self.ui.Radius.setPlainText(f"{round(self.get_dia(y1, y2)/2,2)} mm")
        self.present=True

        endtime=dt.now()
        #getting the total time
        LOGFile.write(f"Total time taken H:{abs((start.hour)-(endtime.hour))} M:{abs((start.minute))-(endtime.minute)} S:{abs((start.second)-(endtime.second))} uS:{abs((start.microsecond)-(endtime.microsecond))}\n")
        self.ui.timeDisplay.setText(f"H:{abs((start.hour)-(endtime.hour))} M:{abs((start.minute))-(endtime.minute)} S:{abs((start.second)-(endtime.second))} uS:{abs((start.microsecond)-(endtime.microsecond))}")
        
        
    
    def get_dia(self,x1,x2):#calculates pixel accuracy and gets Diameter and Radius
        dif=abs((x1-x2))
        pa=0.0664
        dia=(pa*dif)
        return dia
    
    def component_diagonal(self,path): #rhombus bounding box, ID,OD,Thickness,IR,OR
        self.present=False

        #setting up colors Green-OD, Red-ID,Blue-Thickness
        green=(0,255,0)
        blue=(0,0,255)
        red=(255,0,0)
        rxo1,ryo1,rxo2,ryo4=174,247,1850,1540
        start=dt.now() #start the time 
        LOGFile=open("LOGFile.txt","a") #open Logfile to store data
        LOGFile.write("Selected Image :"+os.path.basename(path))
        LOGFile.write("\n//Start time ://"+str(start)+"\n")
        gray_image=imread(path,IMREAD_GRAYSCALE) #convert input image to grayscale
        edgedetect=Canny(gray_image,100,200)#perform canny edge detection
        imwrite("detectededge.bmp",edgedetect) #rewrite image with the edge detection
        edge_detected=im.open("detectededge.bmp")#saving the edge detected image

        #------------TOP coordinates extraction---------------#
        edge_array = np.array(edge_detected)
        mask = (edge_array[ryo1:ryo4-1, rxo1:rxo2-1] == 255)
        # Find the indices where the mask is True
        indices = np.argwhere(mask)
        if indices.size > 0:
            y1, x1 = indices[0] + np.array([ryo1, rxo1])

        #------------BOTTOM coordinates extraction---------------#
        y2, x2 = None, None
        edge_array = np.array(edge_detected)
        for i in range(ryo4 - 1, ryo1 - 1, -1):
            row_slice = edge_array[i, rxo1 - 1:rxo2 - 1][::-1]
            if np.any(row_slice == 255):
                x2 = rxo1 - 1 + len(row_slice) - 1 - np.argmax(row_slice == 255)
                y2 = i
                break

        #------------CENTER coordinates extraction---------------#
        centerX=round((x1+x2)/2) #calculate center of x axis
        centerY=round((y1+y2)/2) #calculate center of y axis

        #------------LEFT coordinates extraction---------------#
        i = rxo1
        while i < centerX:
            color = edge_array[centerY, i]
            if color != 0:
                x3 = i
                y3=centerY
                break
            i += 1

        #------------RIGHT coordinates extraction---------------#
        i = rxo2
        while i > centerX:
            color = edge_array[centerY, i]
            if color != 0:
                x4 = i
                y4=centerY
                break
            i -= 1

        m1=(y2-y1)/(x3-x4)
        #------------BOTTOM LEFT DIAGONAL coordinates extraction---------------#
        i=x3
        while(i<x4):
            y=int((m1*(i-x3))+y2)
            color=edge_detected.getpixel((i,y))
            if color!=0:
                rx1=i
                ry1=int(y)
                break
            i+=1

        #------------TOP RIGHT DIAGONAL coordinates extraction---------------#
        i=x4
        while(i>x3):
            y=int((m1*(i-x3))+y2)
            color=edge_detected.getpixel((i,y))
            if color!=0:
                rx2=i
                ry2=int(y)
                break
            i-=1

        #------------TOP LEFT DIAGONAL coordinates extraction---------------#
        m2=(y1-y2)/(x3-x4)
        i=x3
        while(i<x4):
            y=int((m2*(i-x4))+y2)
            color=edge_detected.getpixel((i,y))
            if color!=0:
                rx3=i
                ry3=int(y)
                break
            i+=1

        #------------BOTTOM RIGHT DIAGONAL coordinates extraction---------------#
        m2=(y1-y2)/(x3-x4)
        i=x4
        while(i>x3):
            y=int((m2*(i-x4))+y2)
            color=edge_detected.getpixel((i,y))
            if color!=0:
                rx4=i
                ry4=int(y)
                break
            i-=1

        #------------Calculation of EXTENDED coordinates---------------#
        x=centerX-rx3
        y=centerY-ry3

        a=centerX-(2*x)
        LOGFile.write(f"Left Coordinate:{a},{centerY}\n") #logging the left coordinates
        self.ui.left.setText(f"{a},{centerY}")#displaying the left coordinates on the main screen
        b=centerY-(2*y)
        LOGFile.write(f"Top Coordinate:{centerX},{b}\n")#writing into logfile
        self.ui.top.setText(f"({centerX},{b})")#displaying top coordinates on mainscreen
        c=centerX+(2*x)
        LOGFile.write(f"Right Coordinate:{c},{centerY}\n")#logging right coordinates
        self.ui.right.setText(f"{c},{centerY}") #displaying the right coordinates on the main screen
        d=centerY+(2*y)
        LOGFile.write(f"Bottom Coordinate:({centerX},{d})\n")#logging bottom coordinates
        self.ui.bottom.setText(f"({centerX},{d})")#displaying bottom coordinates on mainscreen
        p1=centerX #assigning new center values
        p2=centerY #assigning new center values
        
        normal_image=im.open(path) #opening the un-modified input image using PIL module

        aTob=(b-p2)/(p1-a) #slope from left extension to top extension and drawing line 
        i=a
        while(i<round(p1)):
            y=((aTob*(i-round(p1))))+b
            normal_image.putpixel((i,round(y)),green)
            i+=1
        bToc=(p2-b)/(c-p1) #slope from top extension to right extension and drawing line
        i=round(p1)
        while(i<c):
            y=((bToc*(i-c)))+round(p2)
            normal_image.putpixel((i,round(y)),green)
            i+=1
        cTod=(d-p2)/(p1-c) #slope from right extension to bottom extension and drawing line
        i=c
        while(i>round(p1)):
            y=((cTod*(i-round(p1))))+d
            normal_image.putpixel((i,round(y)),green)
            i-=1
        dToa=(p2-d)/(a-p1) #slope from bottom extension to left extension
        i=a
        while(i<round(p1)):
            y=((dToa*(i-round(p1)))+d)
            normal_image.putpixel((i,round(y)),green)
            i+=1

        #get ID OD IR OR Thickness
        id=centerX
        while id < x4:
            color = edge_array[centerY, id]
            if color != 0:
                xi4 = id
                break
            id += 1
        jd=centerX
        while jd > x3:
            color = edge_array[centerY, jd]
            if color != 0:
                xj3 = jd
                break
            jd -= 1
        #---------------ID thickness marking---------------#
        i=xj3
        while(i<xi4):
            normal_image.putpixel((i,centerY),red)
            i+=1
        
        i=xi4
        while(i<x4):
            normal_image.putpixel((i,centerY),blue)
            i+=1
        
        normal_image.save("check.bmp")#saving the image
        self.ui.processedImgDIsplay.setPixmap(QPixmap("check.bmp"))#display on main screen
        self.file_name="check.bmp"

        LOGFile.write(f"Diameter: {self.get_dia(y1, y2)} mm , Radius: {self.get_dia(y1,y2)/2} mm")#getting the OD and OR
        LOGFile.write(f"Internal Diameter: {self.get_dia(xj3, xi4)} mm , Internal Radius: {self.get_dia(xj3,xi4)/2} mm") #getting the ID and IR
        self.ui.plainTextEdit.setPlainText(f"{round(self.get_dia(y1,y2),2)} mm")
        self.ui.ID.setPlainText(f"{round(self.get_dia(xj3,xi4),2)} mm")
        self.ui.thick.setPlainText(f"{round(self.get_dia(xi4,x4),2)} mm")
        self.ui.IR.setPlainText(f"{round(self.get_dia(xj3,xi4)/2,2)} mm")
        self.ui.Radius.setPlainText(f"{round(self.get_dia(y1, y2)/2,2)} mm")
        self.present=True
    
        endtime=dt.now()#saving the end time
        
        #getting the total time
        LOGFile.write(f"Total time taken H:{abs((start.hour)-(endtime.hour))} M:{abs((start.minute))-(endtime.minute)} S:{abs((start.second)-(endtime.second))} uS:{abs((start.microsecond)-(endtime.microsecond))}\n")
        self.ui.timeDisplay.setText(f"H:{abs((start.hour)-(endtime.hour))} M:{abs((start.minute))-(endtime.minute)} S:{abs((start.second)-(endtime.second))} uS:{abs((start.microsecond)-(endtime.microsecond))}")
        
    def find_center(self,path):#finds the center of the component
        self.present=False
        #setting up colors Green-OD, Red-ID,Blue-Thickness
        green=(0,255,0)
        blue=(0,0,255)
        red=(255,0,0)
        #ROI points
        rx1,ry1,rx2,ry4=174,247,1850,1540
        start=dt.now() #start the time 
        LOGFile=open("LOGFile.txt","a") #open Logfile to store data
        LOGFile.write("Selected Image :"+os.path.basename(path))
        LOGFile.write("\n//Start time ://"+str(start)+"\n")
        gray_image=imread(path,IMREAD_GRAYSCALE) #convert input image to grayscale
        edgedetect=Canny(gray_image,100,200)#perform canny edge detection
        imwrite("detectededge.bmp",edgedetect) #rewrite image with the edge detection
        edge_detected=im.open("detectededge.bmp")#saving the edge detected image

        #------------TOP coordinates extraction---------------#
        edge_array = np.array(edge_detected)
        mask = (edge_array[ry1:ry4-1, rx1:rx2-1] == 255)
        # Find the indices where the mask is True
        indices = np.argwhere(mask)
        if indices.size > 0:
            y1, x1 = indices[0] + np.array([ry1, rx1])
            LOGFile.write(f"Top Coordinate:{x1},{y1}\n")#writing into logfile
        self.ui.top.setText(f"({x1},{y1})")#displaying top coordinates on mainscreen

        #------------BOTTOM coordinates extraction---------------#
        y2, x2 = None, None
        edge_array = np.array(edge_detected)
        for i in range(ry4 - 1, ry1 - 1, -1):
            row_slice = edge_array[i, rx1 - 1:rx2 - 1][::-1]
            if np.any(row_slice == 255):
                x2 = rx1 - 1 + len(row_slice) - 1 - np.argmax(row_slice == 255)
                y2 = i
                break
        LOGFile.write(f"Bottom Coordinate:({x2},{y2})\n")#logging bottom coordinates
        self.ui.bottom.setText(f"({x2},{y2})")#displaying bottom coordinates on mainscreen
        centerX=round((x1+x2)/2) #calculate center of x axis
        centerY=round((y1+y2)/2) #calculate center of y axis
        radius=centerY-y1 #calculate the radius
        #find left and right side of x axis
        x3=centerX-radius
        x4=centerX+radius

        #------------LEFT coordinates extraction---------------#
        i = rx1
        while i < centerX:
            color = edge_array[centerY, i]
            if color != 0:
                x3 = i
                break
            i += 1
        LOGFile.write(f"Left Coordinate:{x3},{centerY}\n") #logging the left coordinates
        self.ui.left.setText(f"{x3},{centerY}")#displaying the left coordinates on the main screen

        #------------RIGHT coordinates extraction---------------#
        i = rx2
        while i > centerX:
            color = edge_array[centerY, i]
            if color != 0:
                x4 = i
                break
            i -= 1
        LOGFile.write(f"Right Coordinate:{x4},{centerY}\n")#logging right coordinates
        self.ui.right.setText(f"{x4},{centerY}") #displaying the right coordinates on the main screen

        #to get ID and IR
        id=centerX
        while id < x4:
            color = edge_array[centerY, id]
            if color != 0:
                xi4 = id
                break
            id += 1

        jd=centerX
        while jd > x3:
            color = edge_array[centerY, jd]
            if color != 0:
                xj3 = jd
                break
            jd -= 1

        normal_image=im.open(path) #opening the un-modified input image using PIL module
        i=x3
        while(i<x4):
            normal_image.putpixel((i,centerY),red)
            i+=1

        i=y1
        while(i<y2):
            normal_image.putpixel((centerX,i),blue)
            i+=1
        normal_image.save("check.bmp")
    
        self.ui.processedImgDIsplay.setPixmap(QPixmap("check.bmp"))#display on main screen
        endtime=dt.now()

        #getting the total time
        LOGFile.write(f"Total time taken H:{abs((start.hour)-(endtime.hour))} M:{abs((start.minute))-(endtime.minute)} S:{abs((start.second)-(endtime.second))} uS:{abs((start.microsecond)-(endtime.microsecond))}\n")
        self.ui.timeDisplay.setText(f"H:{abs((start.hour)-(endtime.hour))} M:{abs((start.minute))-(endtime.minute)} S:{abs((start.second)-(endtime.second))} uS:{abs((start.microsecond)-(endtime.microsecond))}")
        self.file_name="check.bmp"
        
        LOGFile.write(f"Diameter: {self.get_dia(y1, y2)} mm , Radius: {self.get_dia(y1,y2)/2} mm")#getting the OD and OR
        LOGFile.write(f"Internal Diameter: {self.get_dia(xj3, xi4)} mm , Internal Radius: {self.get_dia(xj3,xi4)/2} mm") #getting the ID and IR
        self.ui.plainTextEdit.setPlainText(f"{round(self.get_dia(y1,y2),2)} mm")
        self.ui.ID.setPlainText(f"{round(self.get_dia(xj3,xi4),2)} mm")
        self.ui.thick.setPlainText(f"{round(self.get_dia(xi4,x4),2)} mm")
        self.ui.IR.setPlainText(f"{round(self.get_dia(xj3,xi4)/2,2)} mm")
        self.ui.Radius.setPlainText(f"{round(self.get_dia(y1, y2)/2,2)} mm")
        self.ui.center.setPlainText(f"({centerX},{centerY})")
        self.present=True


if __name__=="__main__":#runs the application
    app = QApplication(sys.argv)
    
    widget =MainWindow()
    widget.showMaximized()
    sys.exit(app.exec())
