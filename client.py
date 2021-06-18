import socket
import threading
from tkinter import Tk, Label, Text, Button, simpledialog, scrolledtext
# import tkinter.scrolledtext
import faulthandler; faulthandler.enable()

HOST = '127.0.0.1'
PORT = 1234

class Client:

    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        msg = Tk()
        msg.withdraw()

        self.username = simpledialog.askstring("Username", "Username:", parent=msg)

        self.complete_interface = False
        self.running = True

        interface_thread = threading.Thread(target=self.client_interface)
        receive_thread = threading.Thread(target=self.receive)

        interface_thread.start()
        receive_thread.start()

    def client_interface(self):
        self.win = Tk()
        self.win.configure(bg="lightgray")

        self.chat_label = Label(self.win, text="Chat: ", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.message_label = Label(self.win, text="Message: ", bg="lightgray")
        self.message_label.config(font=("Arial", 12))
        self.message_label.pack(padx=20, pady=5)

        self.input_area = Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.complete_interface = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()


    def write(self):
        message = f"{self.username}: {self.input_area.get('1.0', 'end')}"
        self.client_socket.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.client_socket.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024)
                if message.decode() == 'USERNAME':
                    self.client_socket.send(self.username.encode('utf-8'))
                else:
                    if self.complete_interface:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print('Error')
                self.client_socket.close()
                break

client = Client(HOST, PORT)
