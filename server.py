import socket
import threading
import faulthandler; faulthandler.enable()

HOST = '127.0.0.1'
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

clients = []
usernames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{usernames[clients.index(client)]} says {message.decode()}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f"{username} has left the chat room!".encode('utf-8'))
            usernames.remove(username)
            break

def receive():
        while True:
            print("Server is running and listening ...")
            client, address = server_socket.accept()
            print(f"Connected with {str(address)}")

            client.send("USERNAME".encode('utf-8'))
            username = client.recv(1024)

            usernames.append(username)
            clients.append(client)

            print(f"The username of this client is {username}")
            broadcast(f"New user has connected to the chat room. Say hi to {username}!".encode('utf-8'))
            client.send("you are now connected!".encode('utf-8'))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()


receive()

