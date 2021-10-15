import tkinter as tk
from tkinter import *
import socket
import threading
import struct
import time
from tkinter import messagebox

        
window = tk.Tk()
window.geometry("450x590")
window.resizable(False, False) 

##graphics
canvas = Canvas(window, width = 612, height = 588)      
canvas.pack()    
img = PhotoImage(file="media/cli.png")      
canvas.create_image(0,0, anchor=NW, image=img)

##list - favorited servers
##frame
frame = Frame(window)
frame.pack()
frame.place(x=20,y=150)

label = Label(window,text = "Zapisane pokoje")
label.place(x=50,y=100)

##listbox + scrollbar in frame
listbox = Listbox(frame, height = 20, width = 20)
listbox.pack(side="left", fill="y")
listbox.pack()
scrollbar = Scrollbar(frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

#scrolling
listbox.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = listbox.yview)


##list - available lan servers
##frame
frame1 = Frame(window)
frame1.pack()
frame1.place(x=200,y=150)

label1 = Label(window,text = "Dostępne pokoje (Lan)")
label1.place(x=210,y=100)

##listbox + scrollbar in frame
listbox1 = Listbox(frame1, height = 20, width = 20)
listbox1.pack(side="left", fill="y")
listbox1.pack()
scrollbar1 = Scrollbar(frame1, orient="vertical")
scrollbar1.pack(side="right", fill="y")

#scrolling
listbox1.config(yscrollcommand = scrollbar1.set)
scrollbar1.config(command = listbox1.yview)

#load preferences
preferences_list = []
try:
    file = open('preferences.txt','r')
    fileread = file.read()
    preferences_list = fileread.split("#")
except: pass

# Insert elements into the listbox
for values in range(10):
    listbox.insert(END, values)

available_servers = []

# Lan Avialable Servers Multicast

mark = 0
def searchServers():
    available_servers.clear()
    listbox1.delete(0,'end') #czysczenie listy
    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5008
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if sys.platform ==  'win32': sock.bind(('',MCAST_PORT)) ##zmiana
    else: sock.bind((MCAST_GRP, MCAST_PORT))  
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def receive():
        prev_data = ""
        global mark
        mark = 1
        try:
            while True:
              # For Python 3, change next line to "print(sock.recv(10240))"
              data = sock.recv(1024)
              if data in available_servers: pass
              if prev_data == data: break
              if data == "":break
              else:
                  available_servers.append(data.decode())
                  listbox1.insert(END, data)

              for thread in threading.enumerate(): 
                  print(thread.name)
              prev_data = data
              
        except: pass
        mark = 0
        
    receiveThread = threading.Thread(target=receive)
    receiveThread.name = "receiveThread"
    if mark == 0: receiveThread.start()

searchServers()
      
##functions
def room_connect():
    for thread in threading.enumerate(): 
        print(thread.name)


selected = ""
def CurSelect(evt):
    value = str(listbox1.get(listbox1.curselection()))
    global selected
    selected = value    
listbox1.bind('<<ListboxSelect>>',CurSelect)
def room_connect2():
    global selected
    selected = selected.split("#")
    roomIP = selected[1]
    roomIP = roomIP.replace("'", "")
    if preferences_list == []: messagebox.showerror(title="Brak konfiguracji", message="Najpierw musisz skonfigurować w opcjach nazwę użytkownika")
    else:
        from chatGuest import joinRoom
        joinRoom(preferences_list[0],roomIP)

roomIP_dircon = ""
def connect(roomIP_dircon):
    print(roomIP_dircon)
    print("d")
    """
    if preferences_list == []: messagebox.showerror(title="Brak konfiguracji", message="Najpierw musisz skonfigurować w opcjach nazwę użytkownika")
    else:
        try:
            from chatGuest import joinRoom
            print(roomIP)
            joinRoom(preferences_list[0],roomIP)
        except: pass
    """

def direct_connect():
    window = tk.Toplevel()
    window.geometry("350x150")
    window.configure(background='blue')
    window.title("Dołącz do pokoju")
    label1 = Label(window,text = "Wpisz adres IP:")
    label1.place(x=20,y=50)
    TextIP = Text(window, height = 1, width = 15)
    TextIP.place(x=200,y=50)
    def c():
        address_ip = TextIP.get("1.0",'end-1c')
        address_ip = address_ip.replace("\n","")
        if preferences_list == []: messagebox.showerror(title="Brak konfiguracji", message="Najpierw musisz skonfigurować w opcjach nazwę użytkownika")
        else:
            window.destroy()
            from chatGuest import joinRoom
            joinRoom(preferences_list[0],address_ip)
            
        
    Button5 = Button(window, text = "Połącz", command = c)
    Button5.place(x=250,y=100)
    # Return button bind (enter)
    def bind_enter(void): c()
    window.bind('<Return>', bind_enter)
    window.mainloop()


def add_room():
    print("x")

def preferences():
    window = tk.Toplevel()
    window.geometry("350x400")
    window.configure(background='blue')
    window.title("Opcje")
    label1 = Label(window,text = "Nazwa użytkownika:")
    label1.place(x=20,y=50)
    TextName = Text(window, height = 1, width = 15)
    TextName.place(x=200,y=50)
    def insert_values():
        TextName.delete('1.0', END)
        file = open('preferences.txt','r')
        fileread = file.read()
        fileread = fileread.split("#")
        print(fileread)
        TextName.insert(tk.END,fileread[0])
        file.close()
    try: insert_values()
    except: pass
    def save_preferences():
        open('preferences.txt', 'w').close()
        file = open('preferences.txt','w')   
        file.write(TextName.get("1.0",'end-1c')+"#")
        file.close()
        insert_values()
    def bind_enter(void): save_preferences()
    # Return button bind (enter)
    window.bind('<Return>', bind_enter)
        
    Button1 = Button(window, text = "Zapisz", command = save_preferences)
    Button1.place(x=250,y=340)

    #mainloop
    window.mainloop()

def help_window():
    print("help")

def author_info():
    print("a")

def host_room():
    import chatHost

def close_app():
    window.destroy()

#Create Room Button
nameZ = "Utwórz własny pokój"
horizontalName = ""
for i in range(len("Utwórz własny pokój")):
    horizontalName += nameZ[i] + "\n"

Button1 = Button(window, text = "Połącz", command = room_connect)
Button1.place(x=20,y=530)
Button2 = Button(window, text = horizontalName , command = host_room)
Button2.place(x=385,y= 160)
Button3 = Button(window, text = "Połącz", command = room_connect2)
Button3.place(x=202,y=530)
Button4 = Button(window, text = "Odświerz", command = searchServers)
Button4.place(x=283,y=530)

##menubar
menubar = Menu(window,background='lightblue', foreground='black',
               activebackground='#004c99', activeforeground='white')
#filemenu
filemenu = Menu(menubar, tearoff=0,background='lightblue', foreground='black')
filemenu.add_command(label="Utwórz własny pokój", command=host_room)
filemenu.add_command(label="Połącz z pokojem", command=direct_connect)
filemenu.add_command(label="Dodaj pokój do zapisanych", command=add_room)
filemenu.add_command(label="Opcje", command=preferences)
filemenu.add_separator()
filemenu.add_command(label="Zamknij program", command=close_app)
menubar.add_cascade(label="PablitoCHAT", menu=filemenu)

#helpmenu
helpmenu = Menu(menubar, tearoff=0,background='lightblue', foreground='black')
helpmenu.add_command(label="Instrukcja", command=help_window)
helpmenu.add_command(label="Autor", command=author_info)
menubar.add_cascade(label="Pomoc", menu=helpmenu)

window.config(menu=menubar)

##mainloop
window.mainloop()
