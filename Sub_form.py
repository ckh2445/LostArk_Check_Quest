from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QBasicTimer,Qt,QCoreApplication
import sys
import json
from Load_data import Load_data,Save_data
import collections
from PyQt5 import QtGui
import datetime


form_class = uic.loadUiType("ui\Character_Form.ui")[0]
sub_class = uic.loadUiType("ui\sub_form.ui")[0]

stylesheet1 = ("background-color : rgba(0, 0, 0, 250);"
            "border: 2px solid white;"
            "color: white;"
            "border-radius: 10px;")

class Character_Form(QMainWindow, form_class): #design.Ui_mainWindow
    def __init__(self,input):
        super().__init__()
        self.setupUi(self)
        #self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.input = input
        self.PB_Guardian = self.PB_Guardian
        self.PB_Chaos = self.PB_Chaos
        self.PB_Quest = self.PB_Quest
        
        try:
            #가디언토벌 버튼 리스너
            self.BT_1.clicked.connect(lambda: self.Guardian_complete_button(self.BT_1)) #가디언토벌 버튼 1
            self.BT_2.clicked.connect(lambda: self.Guardian_complete_button(self.BT_2)) #가디언토벌 버튼 2
            self.BT_3.clicked.connect(lambda: self.Guardian_complete_button_2(self.BT_3)) #도전가디언토벌 버튼 3
            #주간레이드 버튼 리스너
            self.BT_4.clicked.connect(lambda: self.Raid_complete_button(self.BT_4)) #아르고스
            self.BT_5.clicked.connect(lambda: self.Raid_complete_button(self.BT_5)) #발탄
            self.BT_6.clicked.connect(lambda: self.Raid_complete_button(self.BT_6)) #비아키스
            self.BT_7.clicked.connect(lambda: self.Raid_complete_button(self.BT_7)) #쿠크세이튼
            self.BT_8.clicked.connect(lambda: self.Raid_complete_button(self.BT_8)) #아브렐슈드
            #에포나 버튼 리스너
            self.BT_9.clicked.connect(lambda: self.Quest_complete_button(self.BT_9)) #에포나 1
            self.BT_10.clicked.connect(lambda: self.Quest_complete_button(self.BT_10)) #에포나 2
            self.BT_11.clicked.connect(lambda: self.Quest_complete_button(self.BT_11)) #에포나 3
            #카오스던전 버튼 리스너
            self.BT_12.clicked.connect(lambda: self.Chaos_complete_button(self.BT_12)) #카오스 1
            self.BT_13.clicked.connect(lambda: self.Chaos_complete_button(self.BT_13)) #카오스 2
            #종료 버튼 리스너
            self.BT_Exit.clicked.connect(self.BT_Exit_Clicked)
            
            self.data = Load_data()
            
            self.LB_Character_Name.setText(self.input) #닉네임을 input로 바꾼다
            
            self.Character_Lv = str(self.data[self.input]["Lv"][3:])
            self.Character_Lv = self.Character_Lv.replace(",","")
            self.LB_Character_Lv.setText(self.Character_Lv) #input을 가진 key의 value를 setting [3:]는 LV.를 빼기 위함
            
            # 휴식게이지 불러오기 없으면 except문
            self.Guardian = int(self.data[self.input]['Guardian'])
            self.Chaos = int(self.data[self.input]['Chaos'])
            self.Quest = int(self.data[self.input]['Quest'])

            #휴식게이지 날짜 비교 
            #self.day = datetime.datetime.strptime(self.data[self.input]['day'], '%Y-%m-%d %H:%M:%S')
            
            
            self.my_date = datetime.datetime.strptime(self.data[self.input]['day'], '%Y-%m-%d %H:%M:%S') #데이터 저장 시간을 불러온다 
            self.next_date =  datetime.datetime.strptime(self.data['next_day'], '%Y-%m-%d %H:%M:%S')
            self.next_week = datetime.datetime.strptime(self.data['next_week'], '%Y-%m-%d %H:%M:%S')
            
            #print(int((self.my_date.date() - self.next_date.date()).days) )
            #print(self.my_date.time())
            if self.my_date.date() >= self.next_date.date():
                gob = int((self.my_date.date() - self.next_date.date()).days) 
                
                if gob >= 1:
                    #gob += 1
                    if self.my_date.time() >= self.next_date.time():
                        gob += 1
                    else:
                        pass
                    
                    #print(gob, "는 1보다 크다")
                    #gob += 1
                    self.Guardian = self.Guardian + int(self.data[self.input]["가디언토벌"]) * 10 + (20 * (gob-1 ))
                    self.Quest = self.Quest + int(self.data[self.input]["에포나"]) * 10 + (30 * (gob-1 ))
                    self.Chaos = self.Chaos + int(self.data[self.input]["카오스던전"]) * 10  + (20 * (gob-1 ))
                    
                    #print(gob)
                    self.data["next_day"] = str(self.next_date + datetime.timedelta(days=gob))
                elif gob == 0:
                    if self.my_date.time() >= self.next_date.time():
                        self.Guardian = self.Guardian + int(self.data[self.input]["가디언토벌"])* 10 
                        self.Quest = self.Quest + int(self.data[self.input]["에포나"])* 10
                        self.Chaos = self.Chaos + int(self.data[self.input]["카오스던전"]) * 10
                        self.data["next_day"] = str(self.next_date + datetime.timedelta(days=1))
                    
                    
                if self.Guardian >= 100:
                    self.Guardian = 100
                    
                if self.Quest >= 100:
                    self.Quest = 100
                    
                if self.Chaos >= 100:
                    self.Chaos = 100
                    
                self.data[self.input]["Guardian"] = self.Guardian
                self.data[self.input]["Quest"] = self.Quest
                self.data[self.input]["Chaos"] = self.Chaos
                self.data[self.input]["가디언토벌"] = 2
                self.data[self.input]["카오스던전"] = 2
                self.data[self.input]["에포나"] = 3
                #Save_data(self.data)
                
            if self.my_date >= self.next_week:
                self.data[self.input]["아르고스"] = 0
                self.data[self.input]["발탄"] = 0
                self.data[self.input]["비아키스"] = 0
                self.data[self.input]["아브렐슈드"] = 0
                self.data[self.input]["쿠크세이튼"] = 0
                self.data[self.input]["도전가디언토벌"] = 0
                self.data[self.input]["레이드횟수"] = 0
                self.BT_3.setEnabled(True)
                self.BT_4.setEnabled(False)
                self.BT_5.setEnabled(True)
                self.BT_6.setEnabled(True)
                self.BT_7.setEnabled(True)
                self.BT_8.setEnabled(True)
                
                self.data["next_week"] = str(self.next_week + datetime.timedelta(days=7))
                #Save_data(self.data)
            
            #print(gob)
            
                
            #print(self.my_date)
            #print(self.next_date)
            #print(self.next_week)
            #print(self.data[self.input]['day'])
            #print(self.my_date)
            ##print(Cal_Days.GetWeekLastDate())
            #print(self.next_day)
            #print(self.day)
            
            self.PB_Guardian.setValue(self.Guardian)
            self.PB_Quest.setValue(self.Quest)
            self.PB_Chaos.setValue(self.Chaos)
            
            # character 정보 변수
            self.level = self.data[self.input]["Lv"][3:]
            self.level = self.level.replace(",","")
            self.level = float(self.level)
            self.character_info = {}
            
            
            self.character_info["레이드횟수"] = int(self.data[self.input]["레이드횟수"])
            self.character_info["아르고스"] = int(self.data[self.input]["아르고스"])
            self.character_info["발탄"] = int(self.data[self.input]["발탄"])
            self.character_info["비아키스"] = int(self.data[self.input]["비아키스"])
            self.character_info["쿠크세이튼"] = int(self.data[self.input]["쿠크세이튼"])
            self.character_info["아브렐슈드"] = int(self.data[self.input]["아브렐슈드"])
            self.character_info["도전가디언토벌"] = int(self.data[self.input]["도전가디언토벌"])
            self.character_info["가디언토벌"] = int(self.data[self.input]["가디언토벌"])
            self.character_info["카오스던전"] = int(self.data[self.input]["카오스던전"])
            self.character_info["에포나"] = int(self.data[self.input]["에포나"])
            
            if self.level >= 1490.00:
                pass
            elif self.level >= 1475.00:
                self.complete_button(self.BT_8)
            elif self.level >= 1430.00:
                self.complete_button(self.BT_8)
                self.complete_button(self.BT_7)
            elif self.level >= 1415.00:
                self.complete_button(self.BT_8)
                self.complete_button(self.BT_7)
                self.complete_button(self.BT_6)
            elif self.level >= 1370.00:
                self.complete_button(self.BT_8)
                self.complete_button(self.BT_7)
                self.complete_button(self.BT_6)
                self.complete_button(self.BT_5)
            else:
                self.complete_button(self.BT_8)
                self.complete_button(self.BT_7)
                self.complete_button(self.BT_6)
                self.complete_button(self.BT_5)
                #self.Raid_complete_button(self.BT_4)
            
            if self.character_info["레이드횟수"] >= 3:
                #self.complete_button(self.BT_4)
                self.complete_button(self.BT_5)
                self.complete_button(self.BT_6)
                self.complete_button(self.BT_7)
                self.complete_button(self.BT_8)
            else:
                #if self.character_info["아르고스"] == 1: self.complete_button(self.BT_4)
                if self.character_info["발탄"] == 1 : self.complete_button(self.BT_5)
                if self.character_info["비아키스"] == 1 : self.complete_button(self.BT_6)
                if self.character_info["쿠크세이튼"] == 1: self.complete_button(self.BT_7)
                if self.character_info["아브렐슈드"] == 1: self.complete_button(self.BT_8)
                
            if self.character_info["아르고스"] == 1: self.complete_button(self.BT_4)
            
            if self.character_info["가디언토벌"] == 2 : pass
            elif self.character_info["가디언토벌"] == 1 :  self.complete_button(self.BT_1)
            else:
                self.complete_button(self.BT_1)
                self.complete_button(self.BT_2)
            
            if self.character_info["카오스던전"] == 2 : pass
            elif self.character_info["카오스던전"] == 1 :  self.complete_button(self.BT_1)
            else:
                self.complete_button(self.BT_12)
                self.complete_button(self.BT_13)
                
            if self.character_info["도전가디언토벌"] == 0 : pass
            elif self.character_info["도전가디언토벌"] == 1 : self.complete_button(self.BT_3)
            
            if self.character_info["에포나"] == 3 :
                pass
            elif self.character_info["에포나"] == 2 : 
                self.complete_button(self.BT_9)
                
            elif self.character_info["에포나"] == 1 : 
                self.complete_button(self.BT_9)
                self.complete_button(self.BT_10)
                
            elif self.character_info["에포나"] == 0 :
                self.complete_button(self.BT_9)
                self.complete_button(self.BT_10)
                self.complete_button(self.BT_11)
            self.now = datetime.datetime.now()
            self.data[self.input]['day'] = str(self.now.strftime('%Y-%m-%d %H:%M:%S'))
            Save_data(self.data)
            self.show()
            
        except:
            self.sub_Form = sub_Form(self.input,self)
            self.sub_Form.show()
            
    def BT_Exit_Clicked(self):
        self.close()
    def Guardian_complete_button_2(self,input:QPushButton):
        input.setStyleSheet(stylesheet1)
        input.setEnabled(False)
        
        self.data[self.input]['도전가디언토벌'] += 1
        #시간 저장
        self.now = datetime.datetime.now()
        self.data[self.input]["day"] = str(self.now.strftime('%Y-%m-%d %H:%M:%S'))
        
        Save_data(self.data)
        
    def complete_button(self,input:QPushButton):
        input.setStyleSheet(stylesheet1)
        input.setEnabled(False)
        
        #시간 저장
        self.now = datetime.datetime.now()
        self.data[self.input]["day"] = str(self.now.strftime('%Y-%m-%d %H:%M:%S'))
        
    def Guardian_complete_button(self,input:QPushButton):
        input.setStyleSheet(stylesheet1)
        input.setEnabled(False)
        if self.Guardian >= 20:
            self.Guardian = self.Guardian - 20 #10을 까준다
        else:
            pass
        
        if self.Guardian < 0:
            self.Guardian = 0
        if self.Guardian >= 100:
            self.Guardian = 100
        self.data[self.input]['Guardian'] = self.Guardian
        #PB Set value
        self.PB_Guardian.setValue(self.Guardian)
        self.PB_Quest.setValue(self.Quest)
        self.PB_Chaos.setValue(self.Chaos)
        
        self.data[self.input]['가디언토벌'] -= 1
        #print(self.data[self.input]['Guardian'])
        
        #시간 저장
        self.now = datetime.datetime.now()
        self.data[self.input]["day"] = str(self.now.strftime('%Y-%m-%d %H:%M:%S'))
        
        Save_data(self.data)
        
    def Raid_complete_button(self,input:QPushButton):
        input.setStyleSheet(stylesheet1)
        input.setEnabled(False)
        
        self.data[str(self.input)][str(input.text())] = 1
        
        if input.text() == "아르고스":
            pass
        else:
            self.data[str(self.input)]["레이드횟수"] += 1
        if self.data[str(self.input)]["레이드횟수"] == 3:
            #self.complete_button(self.BT_4)
            self.complete_button(self.BT_5)
            self.complete_button(self.BT_6)
            self.complete_button(self.BT_7)
            self.complete_button(self.BT_8)
            
        #시간 저장
        self.now = datetime.datetime.now()
        self.data[self.input]["day"] = str(self.now.strftime('%Y-%m-%d %H:%M:%S'))

        Save_data(self.data)
        
        #print(input.text())
    
    def keyPressEvent(self, e): #Esc
        if e.key() == Qt.Key_Escape:
                #시간 저장
            self.now = datetime.datetime.now()
            self.data[self.input]["day"] = str(self.now.strftime('%Y-%m-%d %H:%M:%S'))
            self.close()

    def Quest_complete_button(self,input:QPushButton):
        input.setStyleSheet(stylesheet1)
        input.setEnabled(False)
        
        if self.Quest >= 20:
            self.Quest = self.Quest - 20 #10을 까준다 #10을 까준다
        else:
            pass
        
        
        if self.Quest < 0:
            self.Quest = 0
        if self.Quest >= 100:
            self.Quest = 100
            
        self.data[self.input]['Quest'] = self.Quest
        #PB Set value
        self.PB_Guardian.setValue(self.Guardian)
        self.PB_Quest.setValue(self.Quest)
        self.PB_Chaos.setValue(self.Chaos)
        self.data[self.input]['에포나'] -= 1
        
        #시간 저장
        self.now = datetime.datetime.now()
        self.data[self.input]["day"] = str(self.now.strftime('%Y-%m-%d %H:%M:%S'))
        Save_data(self.data)
    
    def Chaos_complete_button(self,input:QPushButton):
        input.setStyleSheet(stylesheet1)
        input.setEnabled(False)
        
        if self.Chaos >= 20:
            self.Chaos = self.Chaos - 20 #10을 까준다
        else:
            pass
        
        if self.Chaos < 0:
            self.Chaos = 0
        if self.Chaos >= 100:
            self.Chaos = 100
        self.data[self.input]['Chaos'] = self.Chaos
        #PB Set value
        self.PB_Guardian.setValue(self.Guardian)
        self.PB_Quest.setValue(self.Quest)
        self.PB_Chaos.setValue(self.Chaos)
        
        self.data[self.input]['카오스던전'] -= 1
        #시간 저장
        self.now = datetime.datetime.now()
        self.data[self.input]["day"] = str(self.now.strftime('%Y-%m-%d %H:%M:%S'))
        Save_data(self.data)
        
class sub_Form(QMainWindow,sub_class):
    def __init__(self,input,Character_Form:QMainWindow):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        
        self.input = input
        self.data = Load_data()
        #Text에서 숫자만 칠 수 있게끔 한다
        self.LE_guardian.setValidator(QtGui.QIntValidator(0,100,self))
        self.LE_Quest.setValidator(QtGui.QIntValidator(0,100,self))
        self.LE_Chaos.setValidator(QtGui.QIntValidator(0,100,self))
        
        #버틀 리스너 연결
        self.BT_Ok.clicked.connect(self.BT_Ok_Clicked)
        
    def BT_Ok_Clicked(self):
        try:
            self.Guardian = int(self.LE_guardian.text())
            self.Quest = int(self.LE_Quest.text())
            self.Chaos = int(self.LE_Chaos.text())
            if self.Guardian > 100 or self.Quest > 100 or self.Chaos > 100:
                QMessageBox.warning(self,"Warning","100 이상은 입력하지말아 주세요.")
                #self.warning.close()
            else:
                self.data[self.input]["Guardian"] = self.Guardian
                self.data[self.input]["Quest"] = self.Quest
                self.data[self.input]["Chaos"] = self.Chaos
                self.data[self.input]["아르고스"] = 0
                self.data[self.input]["발탄"] = 0
                self.data[self.input]["비아키스"] = 0
                self.data[self.input]["아브렐슈드"] = 0
                self.data[self.input]["쿠크세이튼"] = 0
                self.data[self.input]["레이드횟수"] = 0
                self.data[self.input]["도전가디언토벌"] = 0
                self.data[self.input]["가디언토벌"] = 2
                self.data[self.input]["카오스던전"] = 2
                self.data[self.input]["에포나"] = 3
                self.now = datetime.datetime.now()
                self.data[self.input]["day"] = str(self.now.strftime('%Y-%m-%d %H:%M:%S'))
                
                
                Save_data(self.data)
                self.close()
                self.form = Character_Form(self.input)
                self.form.show()
        except:
            QMessageBox.warning(self,"Warning","공백을 채워주세요.")
            #self.warning.close()
            
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
            
class Warning(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)

input = "쪼커달"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Character_Form(input)
    #window.show()
    app.exec_()