import tkinter as tk
from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button
import socket
import threading
from tkinter import messagebox
import faulthandler; faulthandler.enable()

class Client:

    client_socket = None
    last_received_message = None

    def __init__(self, master):
        self.win = master
        self.chat_transcript_area = None
        self.name_widget = None
        self.enter_text_widget = None
        self.join_button = None
        self.sckt_init()
        self.gui_init()
        self.listen_incoming_msg()

    def sckt_init(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = '127.0.0.1'
        PORT = 1234
        self.client_socket.connect((HOST, PORT))

    def gui_init(self):
        self.chat_box()
        self.username_input_box()
        self.msg_input_box()

    def listen_incoming_msg(self):
        thread = threading.Thread(target=self.receive_msg_server, args=(self.client_socket,))
        thread.start()

    def receive_msg_server(self, sckt):
        while True:
            loading = sckt.recv(256)
            if not loading:
                break
            message = loading.decode('utf-8')
            if "joined" in message:
                user = message.split(":")[1]
                message = "New user has connected to the chat room. Say hi to " + user + "!"
                self.chat_transcript_area.insert('end', message + '\n')
                self.chat_transcript_area.yview(END)
            else:
                self.chat_transcript_area.insert('end', message + '\n')
                self.chat_transcript_area.yview(END)
        sckt.close()

    def username_input_box(self):
        frame = Frame(bg='#cf6a87')
        Label(frame, text='Username:', font=("Helvetica", 16), bg='#cf6a87').pack(side='top', anchor='w')
        self.name_widget = Entry(frame, width=41, borderwidth=2, relief="ridge")
        self.name_widget.pack(side='left', pady=10)
        self.join_button = Button(frame, bg='#cf6a87', text="Join", width=10, command=self.on_join).pack(side='right', fill='x', padx=14)
        frame.pack(side='top')

    def chat_box(self):
        frame = Frame(bg='#cf6a87')
        Label(frame, text='Chat Box:', font=("Serif", 16), bg='#cf6a87').pack(side='top', anchor='w')
        self.chat_transcript_area = Text(frame, width=60, height=10, borderwidth=2, relief="ridge", font=("Serif", 12))
        scrollbar = Scrollbar(frame, command=self.chat_transcript_area.yview, orient=VERTICAL)
        self.chat_transcript_area.config(yscrollcommand=scrollbar.set)
        self.chat_transcript_area.bind('<KeyPress>', lambda e: 'break')
        self.chat_transcript_area.pack(side='left', padx=10)
        scrollbar.pack(side='right', fill='y')
        frame.pack(side='top')

    def msg_input_box(self):
        frame = Frame(bg='#cf6a87')
        Label(frame, text='Enter message:', bg='#cf6a87', font=("Helvetica", 16)).pack(side='top', anchor='w')
        self.enter_text_widget = Text(frame, width=62, height=3, borderwidth=2, relief="ridge", font=("Serif", 12))
        self.enter_text_widget.pack(side='left', pady=15)
        self.enter_text_widget.bind('<Return>', self.on_enter_key_pressed)
        frame.pack(side='top')

    def on_join(self):
        if len(self.name_widget.get()) == 0:
            messagebox.showerror(
                "Enter your username", "Enter your username to send message")
            return
        self.name_widget.config(state='disabled')
        self.client_socket.send(("joined:" + self.name_widget.get()).encode('utf-8'))

    def on_enter_key_pressed(self, event):
        if len(self.name_widget.get()) == 0:
            messagebox.showerror(
                "Username:", "Enter your username to send message")
            return
        self.send_chat()
        self.clear_text()

    def clear_text(self):
        self.enter_text_widget.delete(1.0, 'end')

    def send_chat(self):
        username = self.name_widget.get().strip() + ": "
        data = self.enter_text_widget.get(1.0, 'end').strip()
        message = (username + data).encode('utf-8')
        self.chat_transcript_area.insert('end', message.decode('utf-8') + '\n')
        self.chat_transcript_area.yview(END)
        self.client_socket.send(message)
        self.enter_text_widget.delete(1.0, 'end')
        return 'break'

    def close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.win.destroy()
            self.client_socket.close()
            exit(0)

if __name__ == '__main__':
    win = Tk()
    win.title("Chat Room")
    win.geometry('570x380')
    win.configure(bg='#cf6a87')
    gui = Client(win)
    win.protocol("WM_DELETE_WINDOW", gui.close())
    win.mainloop()
