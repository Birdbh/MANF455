from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, 
                             QPushButton, QStackedWidget)
from data2 import Downtime
from .UserWindow import UserWindow

class MaintenanceTechnicianWindow(UserWindow):
    def __init__(self, employee_id, employee_name):
        super().__init__(employee_id, employee_name)
        self.downtime = Downtime.DowntimeTable()
        self._setup_ui()

    def _setup_ui(self):
        self._add_downtime_display()
        self._add_downtime_forms()
        self.update_downtime_display()

    def _add_downtime_forms(self):
        self.downtime_stack = QStackedWidget()
        self.downtime_stack.addWidget(self._create_set_downtime_widget())
        self.downtime_stack.addWidget(self._create_end_downtime_widget())
        self.content_layout.addWidget(self.downtime_stack)

    def _add_downtime_display(self):
        self.current_downtime_label = QLabel()
        self.content_layout.addWidget(self._create_widget("Current Downtime", self.current_downtime_label))

    def _create_widget(self, title, *widgets):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel(title))
        for w in widgets:
            layout.addWidget(w)
        return widget

    def _create_set_downtime_widget(self):
        downtime_reason = QComboBox()
        downtime_reason.addItems(["Machine Fault", "Product Malfunction", "Labour Incident"])
        
        submit_button = QPushButton("Start Downtime")
        submit_button.clicked.connect(lambda: self._submit_downtime(downtime_reason.currentText()))
        
        return self._create_widget("Downtime Period", downtime_reason, submit_button)

    def _create_end_downtime_widget(self):
        end_button = QPushButton("End Downtime")
        end_button.clicked.connect(self._end_downtime)
        return self._create_widget("End Downtime", end_button)

    def _submit_downtime(self, reason):
        self.downtime.add_downtime(self.employee_id, reason)
        self.update_downtime_display()

    def _end_downtime(self):
        self.downtime.end_downtime()
        self.update_downtime_display()

    def update_downtime_display(self):
        if self.downtime.is_currently_downtime():
            self.current_downtime_label.setText(
                f"Reason: {self.downtime.get_last_row_reason()}\n"
                f"Status: {self.downtime.get_last_row_status()}"
            )
            self.downtime_stack.setCurrentIndex(1)  # Show end downtime widget
        else:
            self.current_downtime_label.setText("No downtime in progress")
            self.downtime_stack.setCurrentIndex(0)  # Show set downtime widget