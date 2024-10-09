from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget)

class OperatorWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Operator Template"))
        layout.addWidget(QPushButton("Create Work Order"))
        layout.addWidget(QPushButton("View Work Orders"))
        self.setLayout(layout)