import tkinter as tk
from tkinter import *
import socket
import threading
import datetime
import webbrowser
import dns.resolver
import pygame
import random
from myIP import localIP
from tkinter import messagebox
import time
##############################################################################
# Options
name = "mati"
room_size = 5

servername = "nowy pokoj"
passwdyn = "false"

###
passwdpubkey = ""

##############################################################################
# Server
#HOST = '127.0.0.'+str(random.randint(1,254))
HOST = localIP()
print(HOST)
PORT = 50007              # Arbitrary non-privileged port
clients = []
clients_username = []
clients_addr = []

def sendall(data):
    for i in range(len(clients)):
        try:
            clients[i].sendall(data)
        except:pass
def remove_user(username):
    list_index = clients_username.index(username)
    return clients.pop(list_index), clients_username.pop(list_index), clients_addr.pop(list_index)           
def client_thread(conn, addr):
    print('Connected by', addr)
    print(clients_addr)
    print(clients)
    #User has joind the room
    name = clients_username[clients.index(conn)]
    user_join_msg = ("Użytkownik " +str(name)+ " dołączył do pokoju.")
    sendall(user_join_msg.encode())

    loop = True
    while loop:
        data = conn.recv(1024)
        #print(data)
        ##User has lef the room
        if data.decode() == '#quit':
            name = clients_username[clients.index(conn)]
            quit_msg = ("Użytkownik " +str(name)+ " opuścił pokój.")
            sendall(quit_msg.encode())
            remove_user(name)
            break      
        else: #normal working chat
            if name not in clients_username: break
            else: sendall(data)

# Data socket
socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServer.bind((HOST, PORT))
socketServer.listen(room_size)

def serverLoop():
    while True:
        try:
            conn, addr = socketServer.accept()
            clients.append(conn)
            clients_addr.append(addr)
            username = conn.recv(1024)
            username = username.decode()
            clients_username.append(username)      
            threading.Thread(target=client_thread, args=(conn,addr)).start()
        except:
            socketServer.close()
threading.Thread(target=serverLoop).start()


## Multicast for available lan servers list
import socket
def multicast():
    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5008
    MULTICAST_TTL = 2
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
    msgPart1 = str(servername)
    msgPart2 = str(localIP())
    msgPart3 = str(passwdyn)
    msgPart4 = str(passwdpubkey)
    #msg = msgPart1 + msgPart2 + msgPart3 + msgPart4
    msg = msgPart1 +"#"+ msgPart2
    msg = msg.encode()
    while True:
        sock.sendto(msg, (MCAST_GRP, MCAST_PORT))
        time.sleep(3)

multicastThread = threading.Thread(target=multicast)
multicastThread.name = "MulticastLoopThread"
multicastThread.start()

##############################################################################
# Chat 

#Window
window = tk.Toplevel()
window.geometry("550x550")
window.resizable(False, False)

#MSG sound notification
pygame.mixer.init()
pygame.mixer.music.load("media/bing.wav")
pygame.mixer.music.set_volume(0.3)

##Logo
canvas = Canvas(window, width = 612, height = 588)      
canvas.pack()    
img = PhotoImage(file="media/cli.png")      
canvas.create_image(0,0, anchor=NW, image=img)
#socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(name.encode())

#wiadomosci w czacie
def text(msg):
    #current time
    now = datetime.datetime.now()
    current_time = format(now, '%H:%M')
    #if msg is to long - divide text into smaller parts
    if len(msg) > 40:
        print(msg)
        msg2 = msg
        while len(msg2) > 40:
            T1.insert(tk.END,msg2[:30])
            msg2 = '-'+msg2[30:] 
        T1.insert(tk.END,msg2+"   "+current_time)    
    else:
        T1.insert(tk.END,msg+"   "+current_time)
    if name not in msg:
        pygame.mixer.music.play()
    #autoscroll to the last message
    T1.see(tk.END)
#Send
def send(): 
   input = T2.get("1.0",'end-1c')
   message = name + ": " + input
   return s.sendall(message.encode()), T2.delete('1.0', END)

def bind_enter(void):
    send()
    
def emoticons_place(emot):
    T2.insert(tk.END, emot)
################################################################################
def kickGuest():
    username = str(T3.get(T3.curselection()))
    if username != "Ty: "+name: #to not to kick host
        remove_user(username)
        msg = ("Użytkownik " +username+ " został wyrzucony z pokoju.")
        sendall(msg.encode())


################################################################################
# Emoticons window
def emoticons():
    global selected
    window = tk.Toplevel()    
    window.geometry("125x390")
    window.resizable(False, False)

    ##graphics
    canvas = Canvas(window, width = 500, height = 350)      
    canvas.pack()    
    img = PhotoImage(file="media/2.png")      
    canvas.create_image(0,0, anchor=NW, image=img)

    ##frame
    frame_emoticons = Frame(window)
    frame_emoticons.pack()
    frame_emoticons.place(x=10,y=120)

    label_emoticons = Label(window,text = "Emotikony")
    label_emoticons.place(x=10,y=85)

    ##listbox + scrollbar in frame
    listbox_emoticons = Listbox(frame_emoticons, height = 10, width = 10)
    listbox_emoticons.pack(side="left", fill="y")
    listbox_emoticons.pack()
    scrollbar_emoticons = Scrollbar(frame_emoticons, orient="vertical")
    scrollbar_emoticons.pack(side="right", fill="y")

    #scrolling
    listbox_emoticons.config(yscrollcommand = scrollbar_emoticons.set)
    scrollbar_emoticons.config(command = listbox_emoticons.yview)

    #emotikons from text file
    text_file = open('emoticons.txt','r',encoding="utf-8")
    text_file = text_file.read()
    text_file = text_file.split("#")
    for i in range(len(text_file)):
        listbox_emoticons.insert(END, text_file[i])

    selected = ""
    def CurSelect(evt):
        value = str(listbox_emoticons.get(listbox_emoticons.curselection()))
        global selected
        selected = value    
    listbox_emoticons.bind('<<ListboxSelect>>',CurSelect)

    def put_emoticon():
        emoticons_place(selected)
        window.destroy()

    def put_emoticon_return_button(void):
        emoticons_place(selected)
        window.destroy()

    window.bind('<Return>', put_emoticon_return_button)
    #focus on list
    listbox_emoticons.focus_set()
    Button1 = Button(window, text ="wybierz", command = put_emoticon)
    Button1.place(x=13,y=315)
    #mainloop
    window.mainloop()
###############################################################################
# Volume Window
def volume_window():
    window = tk.Tk()
    window.geometry("150x40")
    window.title("Sounds Volume")
    window.resizable(False, False)
    window.configure(background='blue')
    volumeSlider = Scale(window, from_=0, to=100, orient=HORIZONTAL)
    volumeSlider.pack()
    volumeSlider.set(pygame.mixer.music.get_volume()*100) #Set slider on actual volume lvl
    vola = volumeSlider.get()
    def getvol():
        while True:
            try:
                vola = float(volumeSlider.get())/100
                pygame.mixer.music.set_volume(vola)
            except: break
    threadVolume = threading.Thread(target=getvol)
    threadVolume.name = "threadVolume"
    threadVolume.start()
    window.mainloop()
     
################################################################################    
##chat
#frame
frame = Frame(window)
frame.pack()
frame.place(x=20,y=80)
#textbox
T1 = Listbox(frame, height = 20, width = 40)
#T1.pack()
T1.pack(side="left", fill="y")
#scrollbar
scrollbar = Scrollbar(frame, orient="vertical",width=16)
scrollbar.pack(side="right", fill="y")
# Scrolling
T1.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = T1.yview)
## Writing text to sending
T2 = Text(window, height = 2, width = 33)
T2.place(x=20,y=460)
# Send button
B1 = tk.Button(window, text ="Wyslij", command = send)
B1.place(x=300, y=466)
# Return button bind (enter)
window.bind('<Return>', bind_enter)
## Focus on textbox
T2.focus_set()
# Emoticon button
B2 = tk.Button(window, text =":-(", command = emoticons)
B2.place(x=20, y=508)

## Userlist
frame1 = Frame(window)
frame1.pack()
frame1.place(x=390,y=110)
T3 = Listbox(frame1, height = 16, width = 14)
T3.pack(side="left", fill="y")
# Scrollbar 
scrollbar = Scrollbar(frame1, orient="vertical",width=14)
scrollbar.pack(side="right", fill="y")
# Scrolling
T3.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = T3.yview)
# Label
label = Label(window,text = "Goście")
label.place(x=430,y=80)
# Kick Guest Button
B3 = tk.Button(window, text ="Wyrzuć", command = kickGuest)
B3.place(x=410, y=410)

# Sounds Volume Button
B4 = tk.Button(window, text ="Vol +/-", command = volume_window)
B4.place(x=70, y=508)

# Local IP address label
label1 = Label(window,text = "IP: "+localIP())
label1.place(x=430,y=516)

##########################tread test
def test():
    for thread in threading.enumerate(): 
        print(thread.name)
        print(pygame.mixer.music.get_volume())

B5 = tk.Button(window, text ="tt-", command = test)
B5.place(x=150, y=508)


###################################
def user_list():
    while True:
        try:
            if T3.size() != len(clients_username):
                T3.delete(0,'end') #czysczenie listy
                for i in range(len(clients)):
                    if clients_username[i] == name: T3.insert(END, "Ty: "+name)
                    else:T3.insert(END, clients_username[i])
        except: pass

threading.Thread(target=user_list).start()

def receive():
    while True:
        try:
            data = s.recv(1024)
            text(data.decode().replace("\n",""))
        except:
            pass

##start thread for receive
threading.Thread(target=receive).start()
################################################################################
# Open hyperlinks in new tab
def CurSelect_HyperlinkOpen(evt):
    try:
        value = str(T1.get(T1.curselection()))
        value = value.replace(",", " ")
        value = value.split()
        for i in range(len(value)):
            if "." in value[i]: #if its url
                try:
                    dns.resolver.resolve(value[i]) #if its not a link, there's gonna be an error
                    webbrowser.open_new_tab(value[i])
                except:pass
    except: pass
T1.bind('<<ListboxSelect>>',CurSelect_HyperlinkOpen)

"""
def on_closing():
    if messagebox.askokcancel("Wyjście", "Czy napewno chcesz wyjść? Spowoduje to zamknięcie pokoju."):
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
"""
##mainloop
tk.mainloop()

message = '#quit'
s.sendall(message.encode())
s.close()
socketServer.close()
