import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtCore import QObject, Qt, QThread, pyqtSignal
import pygetwindow as gw
import cv2
from PIL import ImageGrab
import numpy as np
import time
import serial
import random
import pyautogui

form_class = uic.loadUiType("LostArk_Design.ui")[0]

#My_Capture_Position
Capture_X = 0
Capture_Y = 0
Capture_W = 0
Capture_H  = 0
Capture_Image = 0

#serial
ser = ""
class My_Window(QMainWindow, form_class): #design.Ui_mainWindow
    stop_signal = pyqtSignal()  #make a stop signal to communicate with the worker in another thread
    def __init__(self):
        self.Log_Count = 1
        super().__init__()
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        self.setupUi(self)

        self.Capture_Array_Rule()

        self.BT_Capture_Apply.clicked.connect(self.Capture_Apply_Clicked)
        self.BT_Capture_Exclamation_Capture.clicked.connect(self.Capture_Exclamation_Capture_Clicked)
        self.BT_Capture_JJI_Capture.clicked.connect(self.Capture_JJI_Capture_Clicked)
        self.BT_Stop_Auto.clicked.connect(self.Stop_Auto_Clicked)
        self.BT_Start_Auto.clicked.connect(self.Start_Auto_Clicked)
        self.BT_ArduinoPort_Apply.clicked.connect(self.ArdunoPot_Apply_Clicked)


    def ArduinoPort_Check(self): #ArduinoPort Check 
        if self.CB_ArduinoPort.currentText() == "":
            return False
        else:
            return True

    def ArdunoPot_Apply_Clicked(self):
        global ser
        if self.ArduinoPort_Check():
            try:
                ser = serial.Serial(self.CB_ArduinoPort.currentText(),9600) #serial 통신
            except:
                self.Log.append(str(self.Log_Count) + ": " + "Select Comport No Detect !!!!!")
                self.Log_Count += 1

            self.Log.append(str(self.Log_Count) + ": " + "Arduino Comport = " + self.CB_ArduinoPort.currentText())
            self.Log_Count += 1
        else:
            self.Log.append(str(self.Log_Count) + ": " + "Select Arduino Comport !!!!!")
            self.Log_Count += 1
        
    def Start_Auto_Clicked(self): # Start_Auto_Button clicked Event
        ##### Thread Create and Start
        if self.ArduinoPort_Check() == False:
            self.Log.append(str(self.Log_Count) + ": " + "Select Arduino Comport")
            self.Log_Count += 1

        else:
            if Capture_X == 0  or Capture_Y == 0 or Capture_W == 0 or Capture_H == 0:
                self.Log.append(str(self.Log_Count) + ": " + "Capture Array Apply !!!!!")
                self.Log_Count += 1
            else:
                self.thread = QThread()
                self.auto = Auto()
                self.stop_signal.connect(self.auto.stop)  # connect stop signal to worker stop method
                self.auto.moveToThread(self.thread)

                self.auto.finished.connect(self.thread.quit)  # connect the workers finished signal to stop thread
                self.auto.finished.connect(self.auto.deleteLater) # connect the workers finished signal to clean up worker
                self.thread.finished.connect(self.thread.deleteLater) # connect threads finished signal to clean up thread

                self.thread.started.connect(self.auto.Start_Auto)
                self.thread.finished.connect(self.auto.stop)
                self.auto.Auto_running.connect(self.Update_Log)
                self.thread.start()

                ##### thread finish and Button Setting 
                self.thread.finished.connect(
                    lambda: self.BT_Start_Auto.setEnabled(True)
                )
                self.thread.finished.connect(
                    lambda: self.BT_Start_Auto.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 80); border: 2px solid white; color: white; border-radius: 20px;}')
                )

                ##### Log Append 
                self.Log.append(str(self.Log_Count) + ": " + "Start Auto")
                self.Log_Count += 1

                ##### Start Auto Button Setting 
                self.BT_Start_Auto.setEnabled(False)
                self.BT_Start_Auto.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 200); border: 2px solid white; color: white; border-radius: 20px;}')

    def Stop_Auto_Clicked(self): #Stop Auto Button Event
        self.stop_signal.emit()  # emit the finished signal on stop

        ##### Log Append
        self.Log.append(str(self.Log_Count) + ": " + "Stop Auto")
        self.Log_Count += 1

    def Capture_Apply_Clicked(self): #Capture Apply Clicked Event
        global Capture_H,Capture_W,Capture_X,Capture_Y

        if str(self.LE_X.text()) == "" or str(self.LE_Y.text()) == "" or str(self.LE_W.text()) == "" or str(self.LE_H.text()) == "":
            self.Log.append(str(self.Log_Count) + ": " + "Input All Capture Array")
            self.Log_Count += 1
        else:
            Capture_X = int(self.LE_X.text())
            Capture_Y = int(self.LE_Y.text())
            Capture_W = int(self.LE_W.text())
            Capture_H = int(self.LE_H.text())
            self.Log.append(str(self.Log_Count) + ": " + "Capture Array OK")
            self.Log_Count += 1

    def Capture_Array_Rule(self): #Capture Array Rule 
        self.LE_X.setValidator(QtGui.QIntValidator(1,2000,self))
        self.LE_Y.setValidator(QtGui.QIntValidator(1,2000,self))
        self.LE_H.setValidator(QtGui.QIntValidator(1,2000,self))
        self.LE_W.setValidator(QtGui.QIntValidator(1,2000,self))

    def Capture_Exclamation_Capture_Clicked(self): #CApture Capture Clicked Event
        try:
            global Capture_Image
            self.box = (Capture_X,Capture_Y,Capture_W,Capture_H)

            Capture_Image = np.array(ImageGrab.grab(self.box))
            My_Capture_Image = cv2.cvtColor(Capture_Image, cv2.COLOR_RGB2BGR)
            #cv2.imshow("image",self.image)
            self.image= cv2.resize(Capture_Image, dsize=(301, 170), interpolation=cv2.INTER_AREA)

            h,w,c = self.image.shape
            qImg = QtGui.QImage(self.image.data, w, h, w*c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            self.Image_Start_Viewer.setPixmap(pixmap)

            ##### Log Append
            self.Log.append(str(self.Log_Count) + ": " + "Capture OK")
            self.Log_Count += 1

            ##### write (Save)
            cv2.imwrite("Exclamation Image.png",My_Capture_Image)
        except:
            self.Log.append(str(self.Log_Count) + ": " + "Capture Array Check!!!!!")
            self.Log_Count += 1
    
    def Capture_JJI_Capture_Clicked(self):
        try:
            global Capture_Image
            self.box = (Capture_X,Capture_Y,Capture_W,Capture_H)

            Capture_Image = np.array(ImageGrab.grab(self.box))
            My_Capture_Image = cv2.cvtColor(Capture_Image, cv2.COLOR_RGB2BGR)
            #cv2.imshow("image",self.image)
            self.image= cv2.resize(Capture_Image, dsize=(301, 170), interpolation=cv2.INTER_AREA)

            h,w,c = self.image.shape
            qImg = QtGui.QImage(self.image.data, w, h, w*c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            self.Image_Start_Viewer.setPixmap(pixmap)

            ##### Log Append
            self.Log.append(str(self.Log_Count) + ": " + "Capture OK")
            self.Log_Count += 1

            ##### write (Save)
            cv2.imwrite("JJI Image.png",My_Capture_Image)
        except:
            self.Log.append(str(self.Log_Count) + ": " + "Capture Array Check!!!!!")
            self.Log_Count += 1

    def Update_Log(self, s):   # Log Append 
        self.Log.append(str(self.Log_Count) + ": " + str(s))
        self.Log_Count += 1
        
class Auto(QObject): #Auto Thread
    finished = pyqtSignal() # give worker class a finished signal
    Auto_running = pyqtSignal(str) # 
    

    def __init__(self, parent = None):
        QObject.__init__(self, parent = parent)
        self.continue_run = True     ##### provide a bool run condition for the class
        #self.JJI_detect = None
        #self.Exclamation_detect = None
    def stop(self):
        self.continue_run = False # set the run condition to false on stop

    def Start_Auto(self):
        self.i = 3
        while self.continue_run:     ##### give the loop a stoppable condition
            if self.i > 0: # wating 3Second and Run
                self.Auto_running.emit("Run after " + str(self.i) + " Seconds") #I의 값을 Emit
                QThread.sleep(1) 
                self.i -= 1

            elif self.i == 0: # wating 3Second and Run
                self.Auto_running.emit("Auto Start") # Auto Start Emit
                self.i -= 1        

            else:
                #self.Auto_running.emit("Auto") # Auto Start Emit
                try:
                    self.JJI_detect = None
                    self.Exclamation_detect = None
                    self.JJI_detect =  pyautogui.locateOnScreen("JJI Image.png" ,region = (Capture_X,Capture_Y,Capture_W,Capture_H), confidence = 0.9)
                    self.Exclamation_detect = pyautogui.locateOnScreen("Exclamation Image.png" ,region = (Capture_X,Capture_Y,Capture_W,Capture_H), confidence = 0.9)

                    if self.JJI_detect == None and  self.Exclamation_detect == None:
                        self.Auto_running.emit("No Detect") 

                    #elif self.JJI_detect != None and  self.Exclamation_detect != None:
                    #    self.Auto_running.emit("Same Image Detect (Image Checking) !!!!!")

                    elif self.JJI_detect != None : #찌 발견 
                        self.Auto_running.emit("JJI Detect: " + str(Capture_W)) 
                        #self.Auto_running.emit("Push e") 
                        #KeyboardInput("KW_e")
                        #MouseClick()

                    elif self.Exclamation_detect != None: #느낌표 발견 
                        self.Auto_running.emit("Exclamation Detect") 

                except:
                    self.Auto_running.emit("Can't Open Image File !!!!!") # Auto Start Emit
                    
                QThread.sleep(1) 

            self.finished.emit()    ##### emit the finished signal when the loop is done

def KeyboardInput(Keyinput): #serial Connet Event
    ser.write(str.encode(Keyinput))

def MouseClick():
    ser.write(str.encode(0))
def main():
    app = QApplication(sys.argv)
    window = My_Window()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()