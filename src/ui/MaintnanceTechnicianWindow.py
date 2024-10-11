from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget, QComboBox)

from data2 import Downtime

class MaintnanceTechnicianWindow(QWidget):
    def __init__(self, employee_id, employee_name):
        super().__init__()
        self.employee_id = employee_id
        self.employee_name = employee_name

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Technician: {self.employee_name} (ID: {self.employee_id})"))
        layout.addWidget(QPushButton("Create Maintenance Report"))
        layout.addWidget(self.display_current_downtime_widget())
        self.setLayout(layout)

    def display_current_downtime_widget(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Current Downtime"))
        downtime = Downtime.DowntimeTable()
        downtime_data = downtime.get_last_row()
        if downtime_data is not None:
            layout.addWidget(QLabel(f"Reason: {downtime_data[2]}"))
            layout.addWidget(QLabel(f"Status: {downtime_data[4]}"))
        else:
            layout.addWidget(QLabel("No downtime in progress"))

        #add a widget to 
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def set_downtime_period_widget(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Downtime Period"))

        #select downtime reason
        downtime_reason = QComboBox()
        downtime_reason.addItems(["Machine Fault", "Product Malfunction", "Labour Incident"])
        layout.addWidget(downtime_reason)

        layout.addWidget(QPushButton("Start Downtime"))
        widget = QWidget()
        widget.setLayout(layout)
        return widget
    
    def end_downtime_period_widget(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("End Downtime"))
        layout.addWidget(QPushButton("End Downtime"))
        widget = QWidget()
        widget.setLayout(layout)
        return widget