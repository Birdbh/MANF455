from PyQt5.QtWidgets import (QLabel, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog)
import pandas as pd
import pyqtgraph as pg
from data import Employee

from ui.UserWindow import UserWindow

class ManagerWindow(UserWindow):
    def __init__(self, employee_id, employee_name):
        super().__init__(employee_id, employee_name)
        self.employee_table = Employee.EmployeeTable()
        self._setup_ui()

    def _setup_ui(self):
        self._add_buttons()
        self._setup_employee_table()
        self._setup_oee_chart()

    def _add_buttons(self):
        for button_text in ["Generate Reports", "Manage Users"]:
            button = QPushButton(button_text)
            button.clicked.connect(lambda checked, text=button_text: self._handle_button_click(text))
            self.content_layout.addWidget(button)

    def _handle_button_click(self, button_text):
        # Placeholder for button click handlers
        print(f"Button clicked: {button_text}")

    def _setup_employee_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Employee ID", "Employee Name", "Position"])
        self._populate_employee_table()
        self.content_layout.addWidget(self.table)

        export_button = QPushButton("Export to CSV")
        export_button.clicked.connect(self._export_to_csv)
        self.content_layout.addWidget(export_button)

    def _populate_employee_table(self):
        employees = self.employee_table.get_employee_details()
        
        self.table.setRowCount(len(employees))
        for row_idx, (emp_id, name, role) in enumerate(employees):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(emp_id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(role))

    def _export_to_csv(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)", options=options)
        if file_name:
            data = [
                [self.table.item(row, col).text() if self.table.item(row, col) else ""
                 for col in range(self.table.columnCount())]
                for row in range(self.table.rowCount())
            ]
            df = pd.DataFrame(data, columns=["Employee ID", "Employee Name", "Position"])
            df.to_csv(file_name, index=False)

    def _setup_oee_chart(self):
        self.plot_graph = pg.PlotWidget()
        self.content_layout.addWidget(self.plot_graph)
        self._update_oee_chart()

    def _update_oee_chart(self):
        time, temperature = self._get_oee_data()
        self.plot_graph.clear()
        self.plot_graph.plot(time, temperature)

    def _get_oee_data(self):
        # TODO: Replace with actual OEE data from database
        time = list(range(1, 11))
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 30]
        return time, temperature