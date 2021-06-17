import socket
from _thread import (start_new_thread)
import select

HEADER_LENGTH = 10
THREAD_COUNT = 0
HOST = "127.0.0.1"
PORT = 1234

server_socket = socket.socket()


try:
    server_socket.bind((HOST, PORT))
except socket.error as err:
    print(str(err))

print("Waiting to connect")
server_socket.listen(5)

def client_thread(connection):
    connection.send(str.encode("Welcome to the server"))
    while True:
        data = connection.recv(HEADER_LENGTH)
        reply = "Hello! I am server" + data.decode("utf-8")
        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()

while True:
    client, address = server_socket.accept()
    print("Connected to" + address[0] + str(address[1]))
    start_new_thread(client_thread, (client,))
    THREAD_COUNT+=1
    print("Running Thread: " + str(THREAD_COUNT))
server_socket.close()