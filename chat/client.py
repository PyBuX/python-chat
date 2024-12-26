import socket
import threading
from client_gui import ChatClientGUI

class ChatClient:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.name = "Anonymous"
        self.client_socket = None
        self.is_connected = False

        def connect_to_server(self):
            if self.is_connected:
                return
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.client_socket.connect((self.host, self.port))
                self.client_socket.sendall(self.name.encode())
                self.gui.display_message(f"Connected to server as {self.name}")
                self.is_connected = True
                self.gui.update_buttons(connected=True)
                threading.Thread(target=self.listen_to_server, daemon=True).start()
            except ConnectionRefusedError:
                self.gui.display_message("Connection failed. Server might be unavailable.")

    def disconnect_from_server(self):
        if not self.is_connected:
            return
        self.client_socket.close()
        self.is_connected = False
        self.gui.display_message("Disconnected from server.")
        self.gui.update_buttons(connected=False)

    def listen_to_server(self):
        try:
            while True:
                message = self.client_socket.recv(1024).decode()
                if not message:
                    break
                self.gui.display_message(message)
        except (ConnectionResetError, OSError):
            self.gui.display_message("Server disconnected.")
        finally:
            self.disconnect_from_server()

    def send_message(self, message):
        if self.is_connected:
            self.client_socket.sendall(message.encode())

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    client = ChatClient()
    gui = ChatClientGUI(client)
    gui.show()
    app.exec()
