from PyQt5.QtWidgets import (QLabel, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog)
import pandas as pd
import pyqtgraph as pg
from data import Employee
import pypdf
from datetime import datetime
from ui.UserWindow import UserWindow
from data.OEECalculator import OEECalculator

class ManagerWindow(UserWindow):
    def __init__(self, employee_id, employee_name):
        super().__init__(employee_id, employee_name)
        self.employee_table = Employee.EmployeeTable()
        self._setup_ui()

    def _setup_ui(self):
        self._add_button()
        self._setup_employee_table()
        self._setup_oee_chart()

    def _add_button(self):
        button = QPushButton("Generate Report")
        button.clicked.connect(self._handle_button_click)
        self.content_layout.addWidget(button)

    def _handle_button_click(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save PDF Report", "", "PDF Files (*.pdf)", options=options)
        if file_name:
            self._generate_empty_pdf(file_name)

    def _generate_empty_pdf(self, file_name):
        pdf_writer = pypdf.PdfWriter()
        pdf_writer.add_blank_page(width=612, height=792)  # Standard letter size
        
        with open(file_name, 'wb') as file:
            pdf_writer.write(file)

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
        for row_idx, employee in enumerate(employees):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(employee.employeeId)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(employee.name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(employee.role))

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
        self.plot_graph = pg.PlotWidget(axisItems={'bottom': pg.DateAxisItem()})
        self.content_layout.addWidget(self.plot_graph)
        self._update_oee_chart()

    def _update_oee_chart(self):
        #TODO: need to find a way to plot the datetime objects on the x-axis of the chart
        time, oee_values = self._get_oee_data()
        #convert the time datetime objects to timestamps
        time = [datetime.combine(t, datetime.min.time()).timestamp() for t in time]
        self.plot_graph.clear()
        self.plot_graph.plot(time, oee_values)

    def _get_oee_data(self):
        oee = OEECalculator()
        return oee.get_past_week_of_oee()