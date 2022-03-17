import requests
from bs4 import BeautifulSoup
import re
from tkinter import messagebox

class Character_load():
    def __init__(self,character):
        super().__init__()
        self.url = "https://lostark.game.onstove.com/Profile/Character/" + character
        
        self.character = {}
        self.answer = []
        self.level = []
        self.response = requests.get(self.url)
        self.html = self.response.text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        
    def load_level(self):
        self.test = self.soup.select_one('#expand-character-list')
        self.test2 = self.test.find_all('span')
        #print(self.test2)
        
        for index,str in enumerate(self.test2):
            if index == 0:
                pass
            else:
                if index % 2 ==0:
                    self.answer.append(str.get_text())
        for x in range (len(self.answer)):
            self.url = "https://lostark.game.onstove.com/Profile/Character/" + self.answer[x]
            self.response = requests.get(self.url)
            self.html = self.response.text
            self.soup = BeautifulSoup(self.html, 'html.parser')
            self.level = self.soup.select_one('#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__expedition > span:nth-child(2)')
            self.character[self.answer[x]] = self.level.get_text()
            
        print(self.character)
        
input = "쪼커달"
if __name__ == '__main__':
    Character_load = Character_load(input)
    Character_load.load_level()
