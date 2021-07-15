from tkinter import *
import tkinter
from socket import socket, AF_INET, SOCK_STREAM, gethostbyname, gethostname
from threading import Thread

# ! If you are running the server n a different machine than the client, you should set the server_ip 
# ! to be the local ip address of the server machine

# ? The Blue messages with numbers are the connections between the client and the server code

root = Tk()
root.title('Chat App')
root.geometry('400x380')

header = 1024
enc_format = 'utf-8'
port = 33000
server_ip = gethostbyname(gethostname())
address = (server_ip, port)

client = socket(AF_INET, SOCK_STREAM) # Create client socket
client.connect(address) # ?1

msg_list = Listbox(root, width=50, height=15, bd=0, bg='#F0F0F0')
msg_frame = Frame(root)
msg_entry = Entry(msg_frame, width=45)

def receive():
    # This function runs with the mainloop because of the thread: it makes it possible to receive a 
    # message at any time
    while True:
        try:
            msg = client.recv(header).decode(enc_format) # ?2, 5
            msg_list.insert(END, msg) # Show the message on the screen
        except OSError:
            break

def send(event=None):
    msg = msg_entry.get()
    msg_entry.delete(0, END)
    client.send(msg.encode(enc_format)) # ?3, 4

send_btn = Button(msg_frame, text='Send', command=send)
msg_entry.bind('<Return>', send) # Send the message on enter

msg_list.pack(pady=20, padx=10)
msg_frame.pack()
msg_entry.grid(row=0, column=0, ipady=5, pady=10, padx=10)
send_btn.grid(row=0, column=1)

thread = Thread(target=receive)
thread.start()
root.mainloop()
client.close()
