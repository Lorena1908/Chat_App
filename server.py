from socket import AF_INET, socket, SOCK_STREAM, gethostbyname, gethostname
from threading import Thread, activeCount

client_data = {}
addresses = {}

host = gethostbyname(gethostname())
port = 33000
header = 1024
enc_format = 'utf-8'
address = (host, port)

server = socket(AF_INET, SOCK_STREAM)
server.bind(address)

def broadcast(msg, prefix=''): # This function sends the message to all of the clients
    for sock in client_data:
        sock.send(prefix.encode(enc_format) + msg)

def handle_client(connection, address):
    print(f'{address} is connected')
    
    try:
        name = connection.recv(header).decode(enc_format)
        client_data[connection] = name
        broadcast(f'{name} entered the chat'.encode(enc_format))
    except Exception as e:
        print('[EXCEPTION] User didn\'t input name: ', e)

    while True:
        try:
            msg = connection.recv(header)
            
            if msg:
                broadcast(msg, prefix=name + ': ')
            else: 
                break
        except:
            break
    print('Lost connection')
    connection.close()
    if connection in client_data and name:
        del client_data[connection]
        broadcast(f'{name} has left the chat'.encode(enc_format))
    

def start():
    while True:
        connection, address = server.accept()
        addresses[connection] = address
        connection.send('Enter your name!'.encode(enc_format))
        thread = Thread(target=handle_client, args=(connection, address))
        thread.start()
        print(f'[CONNECTIONS]', activeCount() - 1)

if __name__ == '__main__':
    server.listen(5)
    print(f'[LISTENING] Server is listening on {host}')
    i_thread = Thread(target=start)
    i_thread.start()
    i_thread.join()
    server.close()