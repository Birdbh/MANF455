from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog
import pandas as pd
import pyqtgraph as pg

class ManagerWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Manager Template"))

        # Buttons
        layout.addWidget(QPushButton("Generate Reports"))
        layout.addWidget(QPushButton("Manage Users"))
        
        # Table for Employees
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Employee Name", "Hours Worked"])
        self.populate_employee_table()
        layout.addWidget(self.table)

        # Button to export table
        export_button = QPushButton("Export to CSV")
        export_button.clicked.connect(self.export_to_csv)
        layout.addWidget(export_button)

        #chart display
        self.plot_graph = pg.PlotWidget()
        layout.addWidget(self.plot_graph)
        self.plot_graph.plot(*self.getOEEData())

        self.setLayout(layout)

    #this needs to be moved into the data and report class, currently just to test data
    def getOEEData(self):
        # Example data, replace with actual OEE data as needed
        time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 30]
        return time, temperature

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
