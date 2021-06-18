import socket
import threading
import faulthandler; faulthandler.enable()
class Server:

    clients = []
    usernames = []

    last_received_msg= ""

    def __init__(self):
        self.server_socket = None
        self.server_listen_init()

    def server_listen_init(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = '127.0.0.1'
        PORT = 1234
        # self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((HOST, PORT))
        print("Server is running and listening ...")
        self.server_socket.listen(5)
        self.new_client()

    def receive_messages(self, sckt):
        while True:
            incoming_load = sckt.recv(256)
            if not incoming_load:
                break
            self.last_received_msg = incoming_load.decode('utf-8')
            self.broadcast(sckt)  # send to all clients
        sckt.close()

    def broadcast(self, client_sockets):
        for client in self.clients:
            socket, (ip, port) = client
            if socket is not client_sockets:
                socket.sendall(self.last_received_msg.encode('utf-8'))

    def new_client(self):
        while True:
            client = sckt, (ip, port) = self.server_socket.accept()
            self.add_new_client(client)
            print('Connected to ', ip, ':', str(port))
            thread = threading.Thread(target=self.receive_messages, args=(sckt,))
            thread.start()

    def add_new_client(self, client):
        if client not in self.clients:
            self.clients.append(client)

if __name__ == "__main__":
    Server()