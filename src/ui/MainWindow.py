from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QLineEdit, QMessageBox

from data2 import Employee
from ui import OperatorWindow
from ui import ManagerWindow
from ui import MaintnanceTechnicianWindow
from ui import SignInWindow

#This should be a constant in the future
#UI_TEMPLATES

WINDOW_SIZE_AX=100
WINDOW_SIZE_AY=100
WINDOW_SIZE_AW=800
WINDOW_SIZE_AH=600

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        #Create a main window
        self.setWindowTitle('Manufacturing Execution System')
        self.setGeometry(WINDOW_SIZE_AX, WINDOW_SIZE_AY, WINDOW_SIZE_AW, WINDOW_SIZE_AH)
        self.generateUIStructureWidget()

    def generateUIStructureWidget(self):
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
        
        emp = Employee.EmployeeTable()

        authentication_role = emp.validate_user(username, password)
        if authentication_role is not None:
            self.show_template(authentication_role)
            print(authentication_role)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

    def show_template(self, user_type):
        if user_type == "Operator":
            self.stacked_widget.setCurrentWidget(self.operator_template)
        elif user_type == "Technician":
            self.stacked_widget.setCurrentWidget(self.technician_template)
        elif user_type == "Manager":
            self.stacked_widget.setCurrentWidget(self.manager_template)
