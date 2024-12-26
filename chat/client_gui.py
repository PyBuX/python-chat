from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QListWidget, QApplication, QInputDialog
)
from PyQt6.QtGui import QFont

class ChatClientGUI(QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.client.gui = self
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Chat Client")
        self.setGeometry(100, 100, 700, 500)

        # Title
        title = QLabel("Chat Client")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #2980b9; margin-bottom: 10px;")

        # Chat display
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet(
            "background-color: #ecf0f1; color: #2c3e50; border: 1px solid #bdc3c7; padding: 5px;"
        )

        # Message input
        self.message_input = QLineEdit(self)
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.setStyleSheet(
            "border: 1px solid #bdc3c7; padding: 10px; border-radius: 5px;"
        )

        # Send and Connect buttons
        self.send_button = QPushButton("Send", self)
        self.send_button.setStyleSheet(
            "background-color: #3498db; color: white; padding: 10px; border-radius: 5px;"
        )
        self.send_button.clicked.connect(self.send_message)

        self.connect_button = QPushButton("Connect", self)
        self.connect_button.setStyleSheet(
            "background-color: #2ecc71; color: white; padding: 10px; border-radius: 5px;"
        )
        self.connect_button.clicked.connect(self.request_name_and_connect)

        self.disconnect_button = QPushButton("Disconnect", self)
        self.disconnect_button.setStyleSheet(
            "background-color: #e74c3c; color: white; padding: 10px; border-radius: 5px;"
        )
        self.disconnect_button.clicked.connect(self.client.disconnect_from_server)

        # User list
        self.user_list = QListWidget()
        self.user_list.addItem("Connected Users")
        self.user_list.setStyleSheet(
            "background-color: #ecf0f1; color: #2c3e50; border: 1px solid #bdc3c7; padding: 5px;"
        )

        # Layouts
        layout = QVBoxLayout()
        layout.addWidget(title)

        layout.addWidget(QLabel("Chat Messages:"))
        layout.addWidget(self.chat_display)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.connect_button)
        button_layout.addWidget(self.disconnect_button)

        layout.addWidget(QLabel("Users:"))
        layout.addWidget(self.user_list)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Initialize button states
        self.update_buttons(connected=False)

    def send_message(self):
        message = self.message_input.text().strip()
        if message:
            self.client.send_message(message)
            self.display_message(f"You: {message}")
            self.message_input.clear()

    def display_message(self, message):
        self.chat_display.append(message)

    def update_buttons(self, connected):
        self.connect_button.setEnabled(not connected)
        self.disconnect_button.setEnabled(connected)
        self.send_button.setEnabled(connected)

    def request_name_and_connect(self):
        name, ok = QInputDialog.getText(self, "Enter Your Name", "Name:")
        if ok and name.strip():
            self.client.name = name.strip()
            self.client.connect_to_server()

if __name__ == "__main__":
    from client import ChatClient
    import sys

    app = QApplication(sys.argv)
    client = ChatClient()
    gui = ChatClientGUI(client)
    gui.show()
    app.exec()
