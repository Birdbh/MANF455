from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

class UserWindow(QWidget):
    def __init__(self, employee_id, employee_name):
        super().__init__()
        self.employee_id = employee_id
        self.employee_name = employee_name
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Header bar
        header_bar = QHBoxLayout()
        header_bar.addWidget(QLabel(f"User: {self.employee_name} (ID: {self.employee_id})"))
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.submit_logout)
        header_bar.addWidget(self.logout_button)
        
        main_layout.addLayout(header_bar)
        
        # Content area
        self.content_layout = QVBoxLayout()
        main_layout.addLayout(self.content_layout)

    def submit_logout(self):
        # Assuming MainWindow has a method to handle logout
        self.window().initialize_set_and_activate_sign_in_window()