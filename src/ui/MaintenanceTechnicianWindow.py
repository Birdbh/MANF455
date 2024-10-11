from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QStackedWidget)

from data2 import Downtime

class MaintenanceTechnicianWindow(QWidget):
    def __init__(self, employee_id, employee_name):
        super().__init__()
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.downtime = Downtime.DowntimeTable()

        # Create the main layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Technician: {self.employee_name} (ID: {self.employee_id})"))
        layout.addWidget(QPushButton("Create Maintenance Report"))

        # Add the always-visible current downtime widget
        self.current_downtime_widget = self.display_current_downtime_widget()
        layout.addWidget(self.current_downtime_widget)

        # Create a QStackedWidget to toggle between downtime widgets
        self.downtime_stack = QStackedWidget()
        self.downtime_stack.addWidget(self.set_downtime_period_widget())  # Index 0
        self.downtime_stack.addWidget(self.end_downtime_period_widget())  # Index 1

        # Add the downtime stack to the main layout
        layout.addWidget(self.downtime_stack)

        self.setLayout(layout)
        #self.update_downtime_display()

    def display_current_downtime_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Current Downtime"))

        self.current_downtime_label = QLabel()
        layout.addWidget(self.current_downtime_label)

        return widget
    
    def update_current_downtime_widget(self):
        if self.downtime.is_currently_downtime():
            self.current_downtime_label.setText(f"Reason: {self.downtime.get_last_row_reason()}\nStatus: {self.downtime.get_last_row_status()}")
        else:
            self.current_downtime_label.setText("No downtime in progress")

    def set_downtime_period_widget(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Downtime Period"))

        # Select downtime reason
        downtime_reason = QComboBox()
        downtime_reason.addItems(["Machine Fault", "Product Malfunction", "Labour Incident"])
        layout.addWidget(downtime_reason)

        submit_button = QPushButton("Start Downtime")
        submit_button.clicked.connect(lambda: self.submit_downtime(downtime_reason.currentText()))
        layout.addWidget(submit_button)

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def submit_downtime(self, downtime_reason):
        self.downtime.add_downtime(self.employee_id, downtime_reason)
        self.update_downtime_display()

    def end_downtime_period_widget(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("End Downtime"))

        self.submit_button = QPushButton("End Downtime")
        layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.end_downtime)

        widget = QWidget()
        widget.setLayout(layout)
        return widget
    
    def end_downtime(self):
        self.downtime.end_downtime()
        self.update_downtime_display()

    def update_downtime_display(self):
        self.update_current_downtime_widget()
        if self.downtime.is_currently_downtime():
            self.downtime_stack.setCurrentIndex(1)  # Show end downtime widget
        else:
            self.downtime_stack.setCurrentIndex(0)  # Show set downtime widget