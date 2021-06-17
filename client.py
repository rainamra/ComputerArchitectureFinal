import socket

client_socket = socket.socket()

HEADER_LENGTH = 1024
HOST = "127.0.0.1"
PORT = 1234

print("Waiting to connect")
try:
    client_socket.connect((HOST, PORT))
except socket.error as err:
    print(str(err))

Response = client_socket.recv(HEADER_LENGTH)
print(Response.decode("utf-8"))
input_name = input("What's your name? ")

while True:
    input_text = input(input_name+ ": ")
    client_socket.send(str.encode(input_name + ": "+ input_text))
    response = client_socket.recv(HEADER_LENGTH)
    print(response.decode("utf-8"))
client_socket.close()