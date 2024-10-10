from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QComboBox, QDateTimeEdit, QPushButton, QTableWidget, QTableWidgetItem)

from data2 import Order

class OperatorWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Operator"))
        self.setup_work_order_table()
        layout.addWidget(self.table)

        layout.addWidget(self.create_work_order_widget())
        self.setLayout(layout)

    def setup_work_order_table(self):
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Work Order ID", "Customer ID", "Drilling Operation", "Start Time", "Status"])
        self.populate_work_order_table()

    def populate_work_order_table(self):
        work_orders = Order.OrderTable().get_all_orders()
        for work_order in work_orders:
            self.add_work_order_to_table(work_order)

    def add_work_order_to_table(self, work_order):
        row_idx = self.table.rowCount()
        self.table.insertRow(row_idx)
        for col_idx, item in enumerate(work_order):
            self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

    def create_work_order_widget(self):
        customer_id = QLineEdit()
        drilling_operation = QComboBox()
        drilling_operation.addItems(["1", "2", "3"])
        start_time = QDateTimeEdit()

        submit_button = QPushButton("Submit Work Order")
        submit_button.clicked.connect(lambda: self.submit_work_order(
            int(customer_id.text()),
            int(drilling_operation.currentText()),
            start_time.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        ))

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Create Work Order"))
        layout.addWidget(QLabel("Customer ID"))
        layout.addWidget(customer_id)
        layout.addWidget(QLabel("Drilling Operation"))
        layout.addWidget(drilling_operation)
        layout.addWidget(QLabel("Start Time"))
        layout.addWidget(start_time)
        layout.addWidget(submit_button)

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def submit_work_order(self, customer_id, drilling_operation, start_time):
        # Add new order to the database
        order = Order.OrderTable()
        order.add_order(customer_id, drilling_operation, start_time, "pending")

        new_order_id = order.get_last_row_id()

        # Add the new work order directly to the table
        new_work_order = (new_order_id, customer_id, drilling_operation, start_time, "pending")
        self.add_work_order_to_table(new_work_order)
