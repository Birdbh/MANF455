from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, 
                             QPushButton, QStackedWidget,QTableWidget, QTableWidgetItem)
from data import Downtime
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
        self._setup_downtime_table()

    def _setup_downtime_table(self):
        self.downtime_table = QTableWidget()
        self.downtime_table.setColumnCount(3)
        self.downtime_table.setHorizontalHeaderLabels(["Downtime ID", "Employee ID", "Reason"])
        self._populate_downtime_table()
        self.content_layout.addWidget(self.downtime_table)

    def _populate_downtime_table(self):
        downtimes = self.downtime.get_all_data()
        self.downtime_table.setRowCount(len(downtimes))
        for row_idx, downtime in enumerate(downtimes):
            self.downtime_table.setItem(row_idx, 0, QTableWidgetItem(str(downtime.downtimeId)))
            self.downtime_table.setItem(row_idx, 1, QTableWidgetItem(str(downtime.employeeId)))
            self.downtime_table.setItem(row_idx, 2, QTableWidgetItem(downtime.downtimeReason))

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
        self._populate_downtime_table()

    def update_downtime_display(self):
        if self.downtime.is_currently_downtime():
            last_downtime = self.downtime.get_last_row()
            self.current_downtime_label.setText(
                f"Reason: {last_downtime.downtimeReason}\n"
                f"Status: {last_downtime.status}"
            )
            self.downtime_stack.setCurrentIndex(1)  # Show end downtime widget
        else:
            self.current_downtime_label.setText("No downtime in progress")
            self.downtime_stack.setCurrentIndex(0)  # Show set downtime widget