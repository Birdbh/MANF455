from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QLineEdit, QMessageBox
import sys

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from ui import OperatorWindow
from ui import ManagerWindow
from ui import MaintnanceTechnicianWindow
from ui import SignInWindow

#This should be a constant in the future
#UI_TEMPLATES
#WINDOW_SIZE

class MainWindow(QMainWindow):
    def __init__(self, mes_logic):
        super().__init__()
        self.mes_logic = mes_logic
        self.init_ui()


    def init_ui(self):
        #Create a main window
        self.setWindowTitle('Manufacturing Execution System')
        self.setGeometry(100, 100, 800, 600)
        self.generateUIStructureWidget()
        pass

    def generateUIStructureWidget(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Create a central widget and a layout for it
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Create a stacked widget to hold our templates
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Create our templates and add them to the stacked widget
        self.sign_in_template = SignInWindow.SignInWindow()
        self.stacked_widget.addWidget(self.sign_in_template)

        self.operator_template = OperatorWindow.OperatorWindow()
        self.stacked_widget.addWidget(self.operator_template)

        self.technician_template = MaintnanceTechnicianWindow.MaintnanceTechnicianWindow()
        self.stacked_widget.addWidget(self.technician_template)
        
        self.manager_template = ManagerWindow.ManagerWindow()
        self.stacked_widget.addWidget(self.manager_template)


        # Set the initial template to the sign-in template
        self.stacked_widget.setCurrentWidget(self.sign_in_template)

        # Connect the sign-in button to the authenticate method
        self.sign_in_template.sign_in_button.clicked.connect(self.authenticate)

    def authenticate(self):
        username = self.sign_in_template.username_input.text()
        password = self.sign_in_template.password_input.text()
        
        # This is a placeholder authentication logic. Replace with your actual authentication system.
        if username == "operator" and password == "password":
            self.show_template("operator")
        elif username == "technician" and password == "password":
            self.show_template("technician")
        elif username == "manager" and password == "password":
            self.show_template("manager")
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

    def show_template(self, user_type):
        if user_type == "operator":
            self.stacked_widget.setCurrentWidget(self.operator_template)
        elif user_type == "technician":
            self.stacked_widget.setCurrentWidget(self.technician_template)
        elif user_type == "manager":
            self.stacked_widget.setCurrentWidget(self.manager_template)
