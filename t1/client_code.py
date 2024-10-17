import threading
import socket
import argparse
import os
import sys
import customtkinter as ctk  # CustomTkinter used here

class Send(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):
        while True:
            print(f'{self.name}: ', end=' ')
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]

            if message == "QUIT":
                self.sock.sendall(f'Server: {self.name} has left the chat'.encode('ascii'))
                break
            else:
                self.sock.sendall(f'{self.name}: {message}'.encode('ascii'))

        print('Quitting...')
        self.sock.close()
        os._exit(0)


class Receive(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
        self.message = None

    def run(self):
        while True:
            message = self.sock.recv(1024).decode('ascii')
            if message:
                if self.message:
                    self.message.insert(ctk.END, message + "\n")
                    print(f"\r{message}\n{self.name}: ", end='')
                else:
                    print(f"\r{message}\n{self.name}: ", end='')
            else:
                print('\nError. Lost connection to server')
                print("Quitting...")
                self.sock.close()
                os._exit(0)


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.message = None

    def start_connection(self, name):
        self.name = name
        print(f"Trying to connect to {self.host}:{self.port}")
        self.sock.connect((self.host, self.port))
        print(f"Successfully connected to {self.host}:{self.port}")

        print(f"Welcome {self.name}! Getting ready to send and receive messages!")

        send = Send(self.sock, self.name)
        receive = Receive(self.sock, self.name)

        send.start()
        receive.start()

        self.sock.sendall(f'Server: {self.name} has joined the chat!'.encode('ascii'))
        print("\rReady... (Leave anytime by typing QUIT!)")
        return receive

    def send_message(self, text_input):
        message = text_input.get()
        text_input.delete(0, ctk.END)

        self.message.insert(ctk.END, f'{self.name}: {message}\n')
        

        if message == "QUIT":
            self.sock.sendall(f'Goodbye! {self.name}'.encode('ascii'))
            print("Quitting...")
            self.sock.close()
            os._exit(0)
        else:
            self.sock.sendall(f'{self.name}: {message}'.encode('ascii'))


def open_chat_window(client, receive):
    """Creates the chat window after username input."""
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    window = ctk.CTk()
    window.title("The Yappers")

    from_message = ctk.CTkFrame(master=window)
    scroll_bar = ctk.CTkScrollbar(master=from_message)

    messages = ctk.CTkTextbox(master=from_message, yscrollcommand=scroll_bar.set)
    scroll_bar.pack(side=ctk.RIGHT, fill=ctk.Y)
    messages.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
    client.message = messages
    receive.message = messages

    from_message.grid(row=0, column=0, columnspan=2, sticky="nsew")

    from_entry = ctk.CTkFrame(master=window)
    text_input = ctk.CTkEntry(master=from_entry, placeholder_text="Type a message...")
    text_input.pack(fill=ctk.BOTH, expand=True)
    text_input.bind("<Return>", lambda x: client.send_message(text_input))

    btn_send = ctk.CTkButton(master=window, text="Send", command=lambda: client.send_message(text_input))
    from_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    btn_send.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    window.rowconfigure(0, minsize=500, weight=1)
    window.columnconfigure(0, minsize=500, weight=1)
    window.columnconfigure(1, minsize=200, weight=0)

    window.mainloop()


def username_window(client):
    """Opens a window to ask for the username before starting the chat."""
    def on_submit():
        name = name_entry.get()
        if name:
            username_win.destroy() 
            receive = client.start_connection(name) 
            open_chat_window(client, receive) 

    username_win = ctk.CTk()
    username_win.title("Enter Username")

    username_frame = ctk.CTkFrame(master=username_win)
    username_frame.pack(padx=20, pady=20)

    label = ctk.CTkLabel(master=username_frame, text="Enter your username:")
    label.pack(pady=10)

    name_entry = ctk.CTkEntry(master=username_frame, placeholder_text="Your username")
    name_entry.pack(pady=10)

    submit_btn = ctk.CTkButton(master=username_frame, text="Submit", command=on_submit)
    submit_btn.pack(pady=10)

    username_win.mainloop()


def main(host, port):
    client = Client(host, port)
    username_window(client)  

file_path = os.path.abspath(__file__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Chatroom Client")
    parser.add_argument('-host', default="0.0.0.0", help="Interface to connect (default: 0.0.0.0)")
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP port (default: 1060)')

    args = parser.parse_args()
    main(args.host, args.p)
