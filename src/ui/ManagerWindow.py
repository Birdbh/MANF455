from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
import sys
from PyQt5.QtWebEngineWidgets import *

class ManagerWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Manager Template"))

        # Buttons
        layout.addWidget(QPushButton("View OEE", clicked=self.display_oee))
        layout.addWidget(QPushButton("Generate Reports"))
        layout.addWidget(QPushButton("Manage Users"))
        
        # Table for Employees
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Employee Name", "Hours Worked", "Position"])
        self.populate_employee_table()
        layout.addWidget(self.table)

        # Button to export table
        export_button = QPushButton("Export to CSV")
        export_button.clicked.connect(self.export_to_csv)
        layout.addWidget(export_button)

        # Plotly chart display
        self.chart_view = QWebEngineView()
        layout.addWidget(self.chart_view)

        self.setLayout(layout)

    def populate_employee_table(self):
        # Example data, replace with actual employee data as needed
        employees = [
            ("Alice", 40, "Operator"),
            ("Bob", 35, "Technician"),
            ("Charlie", 30, "Manager")
        ]
        
        self.table.setRowCount(len(employees))
        for row_idx, (name, hours, position) in enumerate(employees):
            self.table.setItem(row_idx, 0, QTableWidgetItem(name))
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(hours)))
            self.table.setItem(row_idx, 2, QTableWidgetItem(position))

    def display_oee(self):
        # Example OEE data, replace with actual calculations
        categories = ['Availability', 'Performance', 'Quality']
        values = [80, 75, 90]

        fig = go.Figure(data=[
            go.Bar(name='OEE', x=categories, y=values)
        ])
        fig.update_layout(title='Overall Equipment Effectiveness (OEE)', barmode='group')

        # Save plot to HTML and display in the web view
        plot_div = plot(fig, include_plotlyjs='cdn', output_type='div')
        self.chart_view.setHtml(plot_div)

    def export_to_csv(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)", options=options)
        if file_name:
            # Gather data from the table
            data = []
            for row in range(self.table.rowCount()):
                row_data = []
                for column in range(self.table.columnCount()):
                    item = self.table.item(row, column)
                    row_data.append(item.text() if item else "")
                data.append(row_data)

            # Create a DataFrame and save to CSV
            df = pd.DataFrame(data, columns=["Employee Name", "Hours Worked", "Position"])
            df.to_csv(file_name, index=False)
