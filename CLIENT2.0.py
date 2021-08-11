import socket 
import threading
import tkinter as tk 
from tkinter import messagebox
from tkinter import *
from tkinter import ttk


HOST = "127.0.0.1"
PORT = 55000
HEADER = 64
FORMAT = "utf8"
DISCONNECT = "x"
BUFSIZE = 1024
LARGE_FONT = ("verdana", 13, "bold")
SECCCOND_FONT = ("times new roman", 10, "bold")

#option
SIGNUP = "signup"
LOGIN = "login"
LOGOUT = "logout"
LOGOUT2 = "logout2"
SEARCH = "search"

#data
data = []

#GUI intialize
class News_App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # icon = PhotoImage(file = "icon.png")
        # self.iconphoto(False, icon)
      
        self.title("TIN TỨC COVID HÔM NAY")
        self.geometry("500x200")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(width=False, height=False)

        container = tk.Frame(self)
        container.pack(side="top", fill = "both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, HomePage):
            frame = F(container, self)

            self.frames[F] = frame 

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(StartPage)
    def showFrame(self, container):
        frame = self.frames[container]
        if container==HomePage:
            self.geometry("700x350")
        else:
            self.geometry("500x200")
        frame.tkraise()

    # close-programe function
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            try:
                option = LOGOUT2
                client.sendall(option.encode(FORMAT))
                client.recv(BUFSIZE)
            except:
                pass

    def logIn(self,curFrame, sck):
        try:
            user = curFrame.entry_user.get()
            pswd = curFrame.entry_pswd.get()

            if user == "" or pswd == "":
                curFrame.label_notice = "Fields cannot be empty"
                return 
       
            #notice server for starting log in
            option = LOGIN
            sck.sendall(option.encode(FORMAT))
            sck.recv(1024)
            #send username and password to server
            sck.sendall(user.encode(FORMAT))
            print("user:", user)

            sck.recv(1024)
            
            sck.sendall(pswd.encode(FORMAT))
            print("pass:", pswd)


            #see if login is accepted:
            accepted = sck.recv(1024).decode(FORMAT)
            print("accepted: "+ accepted)
            if accepted == "1":
                self.showFrame(HomePage)
                curFrame.label_notice["text"] = ""
            elif accepted == "0":
                curFrame.label_notice["text"] = "invalid username or password"

        except:
            curFrame.label_notice["text"] = "Error: Server is not responding"
            print("Error: Server is not responding")

    def signUp(self,curFrame, sck):
        try:
            user = curFrame.entry_user.get()
            pswd = curFrame.entry_pswd.get()

            if pswd == "":
                curFrame.label_notice["text"] = "password cannot be empty"
                return 

            #notice server for starting log in
            option = SIGNUP
            sck.sendall(option.encode(FORMAT))
            sck.recv(1024)
            
            #send username and password to server
            sck.sendall(user.encode(FORMAT))
            print("user:", user)

            sck.recv(1024)

            sck.sendall(pswd.encode(FORMAT))
            print("pass:", pswd)


            # see if login is accepted
            accepted = sck.recv(1024).decode(FORMAT)
            print("accepted: "+ accepted)
            if accepted == "1":
                self.showFrame(HomePage)
                curFrame.label_notice["text"] = ""
            else:
                curFrame.label_notice["text"] = "username already exists"

        except:
            curFrame.label_notice["text"] = "Error 404: Server is not responding"
            print("404")

    def logout(self,curFrame, sck):
        try:
            option = LOGOUT
            sck.sendall(option.encode(FORMAT))
            sck.recv(BUFSIZE)
            self.showFrame(StartPage)
        except:
            curFrame.label_notice["text"] = "Error: Server is not responding"
    
    def send(self, curFrame, sck, tree):
        try:
            country = curFrame.entry_field.get()

            if country == "":
                curFrame.label_notice["text"] = "Fields cannot be empty"
                return

            option = SEARCH
            sck.sendall(option.encode(FORMAT))
            sck.recv(1024)

            sck.sendall(str(country).encode(FORMAT))
            print("Country: ", country) 
            sck.recv(1024)
            sck.sendall("1".encode(FORMAT))

            info1 = sck.recv(BUFSIZE).decode(FORMAT)
            sck.sendall(info1.encode(FORMAT))

            info2 = sck.recv(BUFSIZE).decode(FORMAT)
            sck.sendall(info1.encode(FORMAT))
            
            info3 = sck.recv(BUFSIZE).decode(FORMAT)
            sck.sendall(info1.encode(FORMAT))
            
            info4 = sck.recv(BUFSIZE).decode(FORMAT)
            sck.sendall(info1.encode(FORMAT))
            
            info5 = sck.recv(BUFSIZE).decode(FORMAT)
            sck.sendall(info1.encode(FORMAT))
            
            info6 = sck.recv(BUFSIZE).decode(FORMAT)
            sck.sendall(info1.encode(FORMAT))
            
            sck.recv(BUFSIZE)

            if info1 == "0":
                curFrame.label_notice["text"] = "Error: Country is invalid"
                return
            data.append(info1)
            data.append(info2)
            data.append(info3)
            data.append(info4)
            data.append(info5)
            data.append(info6)
            
            tree.insert('', 'end', value = data)

            data.remove(info1)
            data.remove(info2)
            data.remove(info3)
            data.remove(info4)
            data.remove(info5)
            data.remove(info6)

        except:
            curFrame.label_notice["text"] = "Error: Server is not responding"
            print("Error: Server is not responding")
    def remove_one(self, tree):
        x = tree.selection()[0]
        tree.delete(x)
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")

        label_title = tk.Label(self, text="LOG IN", font=LARGE_FONT,fg='#20639b',bg="bisque2")
        label_user = tk.Label(self, text="username ",fg='#20639b',bg="bisque2",font='verdana 10 ')
        label_pswd = tk.Label(self, text="password ",fg='#20639b',bg="bisque2",font='verdana 10 ')

        self.label_notice = tk.Label(self,text="",bg="bisque2")
        self.entry_user = tk.Entry(self,width=20,bg='light yellow')
        self.entry_pswd = tk.Entry(self,width=20,bg='light yellow')

        button_log = tk.Button(self,text="LOG IN", bg="#20639b",fg='floral white',command=lambda: controller.logIn(self, client)) 
        button_log.configure(width=10)
        button_sign = tk.Button(self,text="SIGN UP",bg="#20639b",fg='floral white', command=lambda: controller.signUp(self, client)) 
        button_sign.configure(width=10)
        
        label_title.pack()
        label_user.pack()
        self.entry_user.pack()
        label_pswd.pack()
        self.entry_pswd.pack()
        self.label_notice.pack()

        button_log.pack()
        button_sign.pack()
       
class HomePage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")
        
        label_title = tk.Label(self, text="COVID NEWS TODAY", font=LARGE_FONT,fg='#20639b',bg="bisque2")
        label_title.pack()

        label_send = tk.Label(self, text="Enter country",fg='#20639b',bg="bisque2",font='verdana 10 ')
        self.entry_field = tk.Entry(self, fg='#20639b',bg="bisque2",font='verdana 10') 
        self.entry_field.configure(width=30)

        self.label_notice = tk.Label(self, text="", bg="bisque2" )
        self.label_notice.pack(pady=4)

        s = ttk.Style()
        s.theme_use('clam')

        tree = ttk.Treeview(self, column=("c1", "c2", "c3", "c4", "c5", "c6"), show='headings', height=7)
        s.configure("Treeview", foreground='#00337f',background="#ffc61e")
        s.configure("Treeview.Heading", background='floral white',foreground='#00337f')
        tree.column("# 1", anchor=CENTER, width="115")
        tree.heading("# 1", text="COUNTRY" )
        tree.column("# 2", anchor=CENTER, width="115")
        tree.heading("# 2", text="CASES")
        tree.column("# 3", anchor=CENTER, width="115")
        tree.heading("# 3", text="TODAY CASES")
        tree.column("# 4", anchor=CENTER, width="115")
        tree.heading("# 4", text="DEATHS")
        tree.column("# 5", anchor=CENTER, width="115")
        tree.heading("# 5", text="TODAY DEATHS")
        tree.column("# 6", anchor=CENTER, width="115")
        tree.heading("# 6", text="RECOVERED")

        send_button = tk.Button(self, bg="#20639b",fg='#f5ea54', text="SEND", activebackground = "green", command=lambda: controller.send(self, client, tree))
        send_button.configure(width=13)
        button_back = tk.Button(self, text="LOG OUT",bg="#20639b",fg='#f5ea54', activebackground = "red",command=lambda: controller.logout(self, client))
        button_back.configure(width=10)
        remove_button = tk.Button(self, text="DELETE",bg="#20639b",fg='#f5ea54', activebackground = "red",command=lambda: controller.remove_one(tree))
        remove_button.configure(width=10)
        tree.pack(pady = 0)
        label_send.pack(side = TOP)   
        self.entry_field.pack()
        send_button.pack(pady = 3)
        button_back.pack(pady = 1)
        remove_button.pack()

    

#GLOBAL socket initialize
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
client.connect(server_address)
 
app = News_App()
#main
try:
    app.mainloop()
except:
    print("Error: server is not responding")
    client.close()
finally:
    client.close()                          