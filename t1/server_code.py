import threading
import socket
import argparse
import os


class Server(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.connections = []  
        self.host = host
        self.port = port

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(5) 

        print(f"Listening on {self.host}:{self.port}")

        while True:
            sc, sockname = sock.accept()
            print(f"Accepted a new connection from {sc.getpeername()} to {sc.getsockname()}")

            server_socket = Server_Socket(sc, sockname, self)
            server_socket.start()

            self.connections.append(server_socket)
            print("Ready to receive messages...")

    def broadcast(self, message, source):
        for connection in self.connections:
            if connection.sockname != source:
                connection.send(message)

    def remove_connection(self, connection):
        self.connections.remove(connection)


class Server_Socket(threading.Thread):
    def __init__(self, sc, sockname, server):
        super().__init__()
        self.sc = sc
        self.sockname = sockname
        self.server = server

    def run(self):
        while True:
            message = self.sc.recv(1024).decode('ascii')

            if message:
                print(f"{self.sockname} : {message}")
                self.server.broadcast(message, self.sockname)
            else:
                print(f"{self.sockname} has closed the connection")
                self.sc.close()
                self.server.remove_connection(self)
                return

    def send(self, message):
        self.sc.sendall(message.encode("ascii"))


def exit_program(server):
    while True:
        ipt = input("")
        if ipt.lower() == "q":
            print("Closing all connections...")
            for connection in server.connections:
                connection.sc.close()
            os._exit(0)  


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Chatroom Server")
    parser.add_argument('-host', default="0.0.0.0", help="Interface the server listens on (default: 0.0.0.0)")
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP port (default: 1060)')

    args = parser.parse_args()

    server = Server(args.host, args.p)
    server.start()

    exit_thread = threading.Thread(target=exit_program, args=(server,))
    exit_thread.start()
