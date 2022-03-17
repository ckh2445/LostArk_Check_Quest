import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import socket
import threading
import json


PORT = 5050 #Port 번호 현재 나는 5050의 port를 열어줌 
HEADER = 64 
SERVER = socket.gethostbyname(socket.gethostname()) #나의 ip를 hostname을 이용하여 받아온다
ADDR = (SERVER,PORT) # 
FORMAT = 'utf-8' #서버 통신을 할 땐 보통 utf-8로 decode해줘야함 
DISCONNECTED_MESSAGE = "!DISCONNECT" #연결을 끊고 싶을 때 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
server.bind(ADDR) #Bind

cred = credentials.Certificate("yolo_lostark.json")

firebase_admin.initialize_app(cred, {
    'databaseURL':'https://yolo-lostark-269c8-default-rtdb.firebaseio.com/'
    })


def handle_client(conn,addr):
    connected = True
    b = b''
    while connected:
        try:
            while 1:
                tmp = conn.recv(1024)
                b += tmp
            d = json.loads(b.decode('utf-8'))
            db.update(d)
            

                
                        
        except: #예외 발생 시 처리문 
            conn.shutdown(2)    # 0 = done receiving, 1 = done sending, 2 = both
            conn.close()
            break

def start():
    server.listen()
    while True: #연결을 서버측에서 계속 기다릴 수 있게끔 while
        conn, addr = server.accept() #socket 연결을 기다림 
        thread = threading.Thread(target=handle_client,args = (conn, addr)) #socket 연결된 후 handle_cleint 함수에 conn, addr 변수를 인자로 절달한 후 Thread 생성
        thread.start() #thread 시작
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}") #thread 갯수 count

if __name__ == "__main__":
    print("[STARTING] server is starting...")
    #print(SERVER)
    start() #start 함수 실행