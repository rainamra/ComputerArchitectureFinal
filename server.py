import socket
from _thread import *

HEADER_LENGTH = 2048
THREAD_COUNT = 0
HOST = "127.0.0.1"
PORT = 1234

server_socket = socket.socket()

print("Waiting to connect")
try:
    server_socket.bind((HOST, PORT))
except socket.error as err:
    print(str(err))
server_socket.listen(5)

def client_thread(client, connection):
    client.send(str.encode("Welcome to the server"))
    print("The new connection was made from IP: " + connection[0] + " and port: " + str(connection[1]))
    while True:
        data = client.recv(HEADER_LENGTH)
        print(data.decode())
        reply = data.decode("utf-8")
        if not data:
            break
        client.sendall(str.encode(reply))
    client.close()

while True:
    client, address = server_socket.accept()
    start_new_thread(client_thread, (client, address))
    THREAD_COUNT+=1
    print("Running Thread: " + str(THREAD_COUNT))
server_socket.close()
