import requests
from bs4 import BeautifulSoup
import json
from Load_data import Load_data

class Character_load():
    def __init__(self):
        super().__init__()
        self.url = "https://lostark.game.onstove.com/Profile/Character/"
        
        self.answer = []
        self.level = []
        
    def load_characters(self, character): #캐릭터를 검색하는 함수
        self.url = self.url + character
        
        self.response = requests.get(self.url)
        self.html = self.response.text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.character_list = self.soup.select_one('#expand-character-list')
        self.character_list2 = self.character_list.find_all('span')
        
        for index,str in enumerate(self.character_list2):
            if index == 0:
                pass
            else:
                if index % 2 ==0:
                    self.answer.append(str.get_text())
        
        return self.answer
    
    def load_level(self, character):
        self.json_data = Load_data()
        if character in self.json_data:
            return self.json_data[str(character)]["Lv"]
        else:
            self.url = "https://lostark.game.onstove.com/Profile/Character/" + character
            self.response = requests.get(self.url)
            self.html = self.response.text
            self.soup = BeautifulSoup(self.html, 'html.parser')
            self.level = self.soup.select_one('#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__expedition > span:nth-child(2)')
            #self.characters_info[characters[x]] = self.level.get_text()
            return self.level.get_text()
        
input = "쪼커달"
if __name__ == '__main__':
    dic = {}
    Character_load = Character_load()
    Characters = Character_load.load_characters(input)
    #print("보유캐릭터: " + "  ".join(Characters))
    print(Character_load.load_level(input))
    #Character_load.load_level(input)
    #print(dic)
    
    #print(level)
