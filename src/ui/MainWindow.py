from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QLineEdit, QMessageBox

from data2 import Employee
from ui import OperatorWindow
from ui import ManagerWindow
from ui import MaintenanceTechnicianWindow
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
        self.showMaximized()

    def generateUIStructureWidget(self):
        # Create a central widget and a layout for it
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.initialize_set_and_activate_sign_in_window()

    def authenticate(self):
        username = self.sign_in_template.username_input.text()
        password = self.sign_in_template.password_input.text()
        
        emp = Employee.EmployeeTable()

        # Get employee details
        employee = emp.authenticate_employee_details(username, password)

        if employee is not None:
            employee_id, employee_name, role = employee[0], employee[1], employee[2]
            self.show_template(role, employee_id, employee_name)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

    def show_template(self, role, employee_id, employee_name):
        if role == "Operator":
            self.setCentralWidget(OperatorWindow.OperatorWindow(employee_id, employee_name))
        elif role == "Technician":
            self.setCentralWidget(MaintenanceTechnicianWindow.MaintenanceTechnicianWindow(employee_id, employee_name))
        elif role == "Manager":
            self.setCentralWidget(ManagerWindow.ManagerWindow(employee_id, employee_name))

    def initialize_set_and_activate_sign_in_window(self):
        self.sign_in_template = SignInWindow.SignInWindow()
        self.setCentralWidget(self.sign_in_template)
        self.sign_in_template.sign_in_button.clicked.connect(self.authenticate)
