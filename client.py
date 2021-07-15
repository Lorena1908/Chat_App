from tkinter import *
import tkinter
from socket import socket, AF_INET, SOCK_STREAM, gethostbyname, gethostname
from threading import Thread

root = Tk()
root.title('Chat App')
root.geometry('400x380')

header = 1024
enc_format = 'utf-8'
port = 33000
server_ip = gethostbyname(gethostname())
address = (server_ip, port)

client = socket(AF_INET, SOCK_STREAM)
client.connect(address)

def receive():
    while True:
        try:
            msg = client.recv(header).decode(enc_format)
            msg_list.insert(END, msg)
        except OSError:
            break

msg_list = Listbox(root, width=50, height=15, bd=0, bg='#F0F0F0')
msg_frame = Frame(root)
msg_entry = Entry(msg_frame, width=45)

def send(event=None):
    msg = msg_entry.get()
    msg_entry.delete(0, END)
    client.send(msg.encode(enc_format))

send_btn = Button(msg_frame, text='Send', command=send)
msg_entry.bind('<Return>', send)

msg_list.pack(pady=20, padx=10)
msg_frame.pack()
msg_entry.grid(row=0, column=0, ipady=5, pady=10, padx=10)
send_btn.grid(row=0, column=1)

thread = Thread(target=receive)
thread.start()
root.mainloop()
client.close()
