from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget)

class ManagerWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Manager Template"))
        layout.addWidget(QPushButton("View OEE"))
        layout.addWidget(QPushButton("Generate Reports"))
        layout.addWidget(QPushButton("Manage Users"))
        self.setLayout(layout)