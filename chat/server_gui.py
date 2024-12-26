from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QApplication, QHBoxLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QTimer
from server import ChatServer

class ServerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.server = ChatServer()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Chat Server")
        self.setGeometry(100, 100, 600, 400)

        # Title
        title = QLabel("Chat Server")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")

        # Log display
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setStyleSheet(
            "background-color: #ecf0f1; color: #2c3e50; border: 1px solid #bdc3c7; padding: 5px;"
        )

        # Start button
        self.start_button = QPushButton("Start Server")
        self.start_button.setStyleSheet(
            "background-color: #2ecc71; color: white; padding: 10px; border-radius: 5px;"
        )
        self.start_button.clicked.connect(self.start_server)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(QLabel("Logs:"))
        layout.addWidget(self.log_display)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

        # Timer for updating logs
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_logs)

    def start_server(self):
        self.server.start()
        self.log_display.append("Server started.")
        self.start_button.setEnabled(False)
        self.timer.start(1000)

    def update_logs(self):
        if self.server.message_history:
            self.log_display.setPlainText("\n".join(self.server.message_history))

if __name__ == "__main__":
    app = QApplication([])
    gui = ServerGUI()
    gui.show()
    app.exec()
