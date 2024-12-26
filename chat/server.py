import socket
import threading

class ChatServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.message_history = []

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")
        threading.Thread(target=self.accept_clients, daemon=True).start()

    def accept_clients(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"New connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

    def handle_client(self, client_socket):
        try:
            client_name = client_socket.recv(1024).decode()
            self.clients[client_socket] = client_name
            join_message = f"{client_name} has joined the chat."
            self.message_history.append(join_message)
            print(join_message)
            self.broadcast(join_message, client_socket)
            while True:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                full_message = f"{client_name}: {message}"
                self.message_history.append(full_message)
                print(full_message)
                self.broadcast(full_message, client_socket)
        except ConnectionResetError:
            pass
        finally:
            client_name = self.clients.pop(client_socket, "A client")
            leave_message = f"{client_name} has left the chat."
            self.message_history.append(leave_message)
            print(leave_message)
            self.broadcast(leave_message, client_socket)
            client_socket.close()

    def broadcast(self, message, sender_socket):
        for client in self.clients.keys():
            if client != sender_socket:
                client.sendall(message.encode())

if __name__ == "__main__":
    server = ChatServer()
    server.start()
    input("Press Enter to stop the server...\n")
