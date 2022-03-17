import json

def Load_data():
    try:
        with open('data/data.json', 'r',encoding='UTF8') as f:
            json_data = json.load(f)
            return json_data
    except:
        with open('data\data.json', 'w', encoding='utf-8') as make_file:
            json.dump({}, make_file, indent="\t",ensure_ascii=False)
        
def Save_data(dic):
    with open('data\data.json', 'w', encoding='utf-8') as make_file:
            json.dump(dic, make_file, indent="\t",ensure_ascii=False)
            
if __name__ == '__main__':
    json_data = Load_data()
    for key,value in enumerate(json_data):
        print(key,value)
    #print(json_data)