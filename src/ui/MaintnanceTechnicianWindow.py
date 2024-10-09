from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget)

class MaintnanceTechnicianWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Technician Template"))
        layout.addWidget(QPushButton("View Maintenance Reports"))
        layout.addWidget(QPushButton("Create Maintenance Report"))
        self.setLayout(layout)