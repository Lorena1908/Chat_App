from socket import AF_INET, socket, SOCK_STREAM, gethostbyname, gethostname
from threading import Thread, activeCount

# ? The Blue messages with numbers are the connections between the client and the server code

client_data = [] # This holds the clients for sending the messages

host = gethostbyname(gethostname())
port = 33000
header = 1024
enc_format = 'utf-8'
address = (host, port)

server = socket(AF_INET, SOCK_STREAM) # Creates the server
server.bind(address)

def broadcast(msg, prefix=''): # This function sends the message to all of the clients
    for sock in client_data:
        sock.send(prefix.encode(enc_format) + msg) # ?5

def handle_client(connection, address):
    print(f'{address} is connected')
    # ! The first message sent must be the user name
    
    # The try-except below makes it possible to close the window before inputing the name and not 
    # getting an ugly error message in the server
    try:
        name = connection.recv(header).decode(enc_format) # ?3
        client_data.append(connection)
        broadcast(f'{name} entered the chat'.encode(enc_format))
    except Exception as e:
        print('[EXCEPTION] User didn\'t input name: ', e)

    while True:
        try:
            msg = connection.recv(header) # ?4
            # There will be no message when the client is closed on the client side so it'll exit 
            # this loop and close the connection from the server side
            
            if msg: # If there is a message it'll send it for all users
                broadcast(msg, prefix=name + ': ') # ?5
            else: 
                break
        except:
            break
    print('Lost connection')
    connection.close()

    # This is needed because of the first try-except clause from this function
    if connection in client_data and name:
        client_data.remove(connection)
        broadcast(f'{name} has left the chat'.encode(enc_format))
    

def start():
    server.listen(5)
    print(f'[LISTENING] Server is listening on {host}')

    while True:
        # Accept the connection
        connection, address = server.accept() # ?1
        connection.send('Enter your name!'.encode(enc_format)) # ?2
        # This is sent to the client to show up on the screen
        thread = Thread(target=handle_client, args=(connection, address))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {activeCount() - 1}')

start()