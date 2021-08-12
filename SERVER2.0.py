import socket
import json
import tkinter as tk
from tkinter import messagebox
import threading
import datetime
from urllib.request import urlopen
import json


FONT1 = ("verdana", 13,"bold")
FONT2 = ("times new roman", 12, "bold")
FONT3 = ("verdana", 10,"bold")

username = []
password = []
client_addresses = []
username = ""
password = ""

BUFSIZE = 1024
FORMAT = 'utf8'
HEADER = 64
DISCONNECT = "x"

#option
SIGNUP = "signup"
LOGIN = "login"
LOGOUT = "logout"
SEARCH = "search"
LOGOUT2 = "logout2"


HOST =  "127.0.0.1"
PORT = 55000
ADDR = (HOST, PORT)
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
SERVER.bind(ADDR)
SERVER.listen(5)

def getDataFromWebsite():
    url = "https://coronavirus-19-api.herokuapp.com/countries"
    response = urlopen(url)
    data_json = json.loads(response.read())
    with open ("CovidNews.json", "w+") as f:
        json.dump(data_json, f, indent = 3)
    
def signupToServer(client):
    username = client.recv(BUFSIZE).decode(FORMAT)
    client.sendall("0".encode(FORMAT))
    password = client.recv(BUFSIZE).decode(FORMAT)
    if createAccount(username, password) == 1:
        client.sendall("1".encode(FORMAT))
        return 1
    else:
        client.sendall("0".encode(FORMAT))
        return 0
def loginToServer(client):
    username = client.recv(BUFSIZE).decode(FORMAT)
    client.sendall("0".encode(FORMAT))
    password = client.recv(BUFSIZE).decode(FORMAT)
    if checkAccount(username,password) == 1:
        client.sendall("1".encode(FORMAT))
        return 1
    else:
        client.sendall("0".encode(FORMAT))
        return 0        
def createAccount(username, password):
    if checkAccount(username, password) == 0:
        with open ("data.json", "r+") as f:
            data = json.load(f)
            data["username"].append(username)
            data["password"].append(password)
            f.seek(0)
            json.dump(data, f, indent = 3)
            return 1
    else:
        return 0
def checkAccount(username, password):
    with open ("data.json", "r") as f:
        data = json.load(f)
    if username in data['username']:
        index1 = data['username'].index(username)
        if password in data['password']:
            index2 = data['password'].index(password)
            if index1 == index2:
                return 1
            else:
                return 0
        else:
            return 0
    else:
        return 0
def searchInfo(country):
    with open ("CovidNews.json", "r") as f:
        data = json.load(f) 
        for e in data:
            if e["country"] == country:
                msg1 =  e["country"] 
                msg2 = str(e["cases"])
                msg3 = str(e["todayCases"]) 
                msg4 = str(e["deaths"])
                msg5 = str(e["todayDeaths"]) 
                msg6 = str(e["recovered"]) 
                return msg1, msg2, msg3, msg4, msg5, msg6
        return "0","0","0","0","0","0"

def handle_client(client, client_address):  # Takes client socket as argument.
    is_login = False
    while True:
        try:
            option = client.recv(BUFSIZE).decode(FORMAT)
            client.sendall(option.encode(FORMAT))
            if is_login == True:
                    if option == SEARCH:
                        country = client.recv(BUFSIZE).decode(FORMAT)
                        client.sendall(option.encode(FORMAT))
                        print(country)
                        client.recv(BUFSIZE)
                        msg1,msg2, msg3, msg4, msg5, msg6 = searchInfo(country)
                        if msg1 == "0":
                                client.sendall("0".encode(FORMAT))
                                client.recv(BUFSIZE) 
                                client.sendall("0".encode(FORMAT))
                                client.recv(BUFSIZE)
                                client.sendall("0".encode(FORMAT))
                                client.recv(BUFSIZE)
                                client.sendall("0".encode(FORMAT))
                                client.recv(BUFSIZE)
                                client.sendall("0".encode(FORMAT))
                                client.recv(BUFSIZE)
                                client.sendall("0".encode(FORMAT))
                                client.recv(BUFSIZE)
                                client.sendall("0".encode(FORMAT))
                        else:
                                client.sendall(str(msg1).encode(FORMAT))
                                client.recv(BUFSIZE)
                                client.sendall(str(msg2).encode(FORMAT))
                                client.recv(BUFSIZE)
                                client.sendall(str(msg3).encode(FORMAT))
                                client.recv(BUFSIZE)
                                client.sendall(str(msg4).encode(FORMAT))
                                client.recv(BUFSIZE)
                                client.sendall(str(msg5).encode(FORMAT))
                                client.recv(BUFSIZE)
                                client.sendall(str(msg6).encode(FORMAT))
                                client.recv(BUFSIZE)
                                client.sendall(str(msg6).encode(FORMAT))
                    elif option == LOGOUT:
                        is_login = False
                    elif option == LOGOUT2:
                        break
                    else:
                        continue
            elif is_login == False:
                if option == LOGIN:
                    acp = loginToServer(client)
                    if acp == 1:
                        is_login = True
                    else:
                        continue
                elif option == SIGNUP:
                    acp = signupToServer(client)
                    if acp == 1:
                        is_login = True
                    else:
                        continue
                elif option == LOGOUT:
                    break
                elif option == LOGOUT2:
                    break
                else:
                        continue
        except socket.error:
            break
       
    client_addresses.remove(client_address)
    print("%s:%s has disconnected." % client_address)
    client.close()  

def handle_server():
    try:
        while True:
            client, client_address = SERVER.accept()
            print("%s:%s has connected." % client_address)
            client_addresses.append(client_address)
            sThread = threading.Thread(target = handle_client, args =(client, client_address))
            sThread.daemon = True
            sThread.start()
    except:
        SERVER.close()
class News_App(tk.Tk):
    def __init__(self, *args, **kwargs):
        getDataFromWebsite()
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Covid News Server")
        self.geometry("400x350")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(width=False, height=False)

        self.configure(bg="bisque2")
        label_title = tk.Label(self, text="SERVER", font=FONT1,fg='#20639b',bg="bisque2")
        messages_frame = tk.Frame(self)
        scrollbar = tk.Scrollbar(messages_frame)  # To navigate through past messages.
        self.msg_list = tk.Listbox(messages_frame, height=13, width=100,
                            bg='floral white', activestyle = 'dotbox', font = FONT2,
                            fg='#20639b', yscrollcommand=scrollbar.set)

        reset_button = tk.Button(self, text = "refresh", font=FONT3,fg='#20639b',bg="bisque2", command = self.reset)
        reset_button.configure(width = 8)
        self.msg_list.insert(0, "Server is listening...")
        self.reset_data()
        label_title.pack()
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.msg_list.pack(pady = 4)
        messages_frame.pack(pady = 4)
        reset_button.pack()
        
    # close-programe function
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            SERVER.close()
    def reset(self):
        datetime_object = datetime.datetime.now()
        self.msg_list.insert(0, datetime_object)
        i = 0
        for client_address in client_addresses:
            i += 1
            self.msg_list.insert(i, "%s:%s has connected." % client_address)
        if i == 0:
            i += 1
            self.msg_list.insert(i, "No client connected.")
        i += 1
        self.msg_list.insert(i, "__________________________")

    def reset_data(self):
        self.after(3600000, self.reset_data)
  
if __name__ == '__main__':
    app = News_App()
    sThread = threading.Thread(target = handle_server)
    sThread.daemon = True
    sThread.start()
    app.mainloop()

