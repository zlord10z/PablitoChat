import tkinter as tk
from tkinter import *
import socket
import threading
import datetime
import webbrowser
import dns.resolver
import pygame
from myIP import localIP


def joinRoom(uname, host):
    name = uname
    #Window
    window = tk.Toplevel()
    window.geometry("450x550")
    window.configure(background='blue')
    window.resizable(False, False)

    # New MSG Sound Notification
    pygame.mixer.init()
    pygame.mixer.music.load("media/bing.wav")
    pygame.mixer.music.set_volume(0.3)

    #Logo
    canvas = Canvas(window, width = 612, height = 588)      
    canvas.pack()    
    img = PhotoImage(file="media/cli.png")      
    canvas.create_image(0,0, anchor=NW, image=img)

    #Socket
    HOST = host       # The remote host
    PORT = 50007              # The same port as used by the server
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
    #GUI - Send
    def send(): 
       input = T2.get("1.0",'end-1c')
       message = name + ": " + input
       return s.sendall(message.encode()), T2.delete('1.0', END)

    def bind_enter(void):
        send()
        
    def emoticons_place(emot):
        T2.insert(tk.END, emot)


    ################################################################################
    # Emoticons window
    def emoticons():
        global selected
        window = tk.Toplevel()    #########
        window.geometry("125x390")

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
    #scrolling
    T1.config(yscrollcommand = scrollbar.set)
    scrollbar.config(command = T1.yview)
    ##writing text for sending
    T2 = Text(window, height = 2, width = 40)
    T2.place(x=20,y=460)
    #Send button
    B1 = tk.Button(window, text ="Wyslij", command = send)
    B1.place(x=364, y=466)
    #return button bind (enter)
    window.bind('<Return>', bind_enter)
    ##focus on textbox
    T2.focus_set()
    #emoticon button
    B2 = tk.Button(window, text =":-(", command = emoticons)
    B2.place(x=20, y=508)

    # Sounds Volume Button
    B4 = tk.Button(window, text ="Vol +/-", command = volume_window)
    B4.place(x=70, y=508)

    # Local IP address label
    label1 = Label(window,text = "IP: "+localIP())
    label1.place(x=330,y=516)

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
        value = str(T1.get(T1.curselection()))
        value = value.replace(",", " ")
        value = value.split()
        for i in range(len(value)):
            if "." in value[i]: #if its url
                try:
                    dns.resolver.resolve(value[i]) #if its not a link, theresgonna be error
                    webbrowser.open_new_tab(value[i])
                except:pass           
    T1.bind('<<ListboxSelect>>',CurSelect_HyperlinkOpen)


    ##mainloop
    tk.mainloop()

    message = '#quit'
    s.sendall(message.encode())
    s.close()
