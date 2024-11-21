from PyQt5.QtWidgets import (QLabel, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog,QWidget,QLineEdit,QComboBox,QVBoxLayout)
import pandas as pd
import pyqtgraph as pg
from data import Employee, Downtime
import pypdf
from datetime import datetime
from ui.UserWindow import UserWindow
from data.OEECalculator import OEECalculator
from data.ReportGenerator import ReportGenerator

class ManagerWindow(UserWindow):
    def __init__(self, employee_id, employee_name):
        super().__init__(employee_id, employee_name)
        self.employee_table = Employee.EmployeeTable()
        self._setup_ui()

    def _setup_ui(self):
        self._add_button()
        self._setup_employee_table()
        self._setup_oee_chart()
        self._create_add_employee_widget()

    def _add_button(self):
        button = QPushButton("Generate Downtime Report")
        button.clicked.connect(self._handle_button_click)
        self.content_layout.addWidget(button)

    def _handle_button_click(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save PDF Report", "", "PDF Files (*.pdf)", options=options)
        if file_name:
            downtime_table = Downtime.DowntimeTable()
            # Create ReportGenerator with the selected file path
            report_gen = ReportGenerator(file_name)
            df = downtime_table.turn_all_data_into_dataframe()
            report_gen.generate_report(df)

    def _generate_empty_pdf(self, file_name):
        downtime_table = Downtime.DowntimeTable()
        report_gen = ReportGenerator("downtime_report.pdf")
        df = downtime_table.turn_all_data_into_dataframe()
        report_gen.generate_report(df)

    def _setup_employee_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Employee ID", "Employee Name", "Position"])
        self._populate_employee_table()
        self.content_layout.addWidget(self.table)

        export_button = QPushButton("Export Employee Table to CSV")
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
    
    def _create_add_employee_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Add Employee"))
        
        self.employee_username1 = QLineEdit()
        self.employee_Password1 = QLineEdit()
        self.employee_name1 = QLineEdit()
        self.employee_role1 = QComboBox()
        self.employee_role1.addItems(["Manager", "Technician", "Operator"])
        
        

        for label, w in [("Employee Name", self.employee_name1),
                         ("Employee Username", self.employee_username1),
                         ("Employee Password", self.employee_Password1),
                         ("Employee Role", self.employee_role1)]:
            layout.addWidget(QLabel(label))
            layout.addWidget(w)

        submit_button1 = QPushButton("Add Employee")
        submit_button1.clicked.connect(self._submit_employee)
        layout.addWidget(submit_button1)

        self.content_layout.addWidget(widget)

    def _submit_employee(self):
        Employee_name = self.employee_name1.text()
        Employee_username=self.employee_username1.text()
        Employee_password=self.employee_Password1.text()
        Employee_role = self.employee_role1.currentText()
        

        self.employee_table.add_employee(Employee_name,Employee_username,Employee_password,Employee_role)

        self._populate_employee_table()

        # Clear input fields after submission
        self.employee_name1.clear()
        self.employee_username1.clear()
        self.employee_Password1.clear()
        self.employee_role1()
        
    
   