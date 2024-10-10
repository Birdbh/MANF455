from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget,QLineEdit,QComboBox,QTimeEdit,QDateTimeEdit, QTableWidget, QTableWidgetItem)

#from data2 import MESDatabase
from data2 import Order

class OperatorWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Operator Template"))
        self.widget_to_see_work_orders()
        layout.addWidget(self.table)
        layout.addWidget(self.widget_to_create_work_order())
        layout.addWidget(QPushButton("View Work Orders"))

        self.setLayout(layout)

    def widget_to_see_work_orders(self):

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Work Order ID", "Customer ID", "Drilling Operation", "Start Time", "Status"])
        self.populate_work_order_table()

    def populate_work_order_table(self):

        work_orders = Order.OrderTable().get_all_orders()
        self.table.setRowCount(len(work_orders))
        for row_idx, work_order in enumerate(work_orders):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(work_order[0])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(work_order[1])))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(work_order[2])))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(work_order[3])))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(work_order[4])))

    def widget_to_create_work_order(self):
        # Create a widget to create a work order
        customer_id = QLineEdit()
        drilling_operation = QComboBox()
        drilling_operation.addItem("1")
        drilling_operation.addItem("2")
        drilling_operation.addItem("3")
        start_time = QDateTimeEdit()
        #Create a button to submit the work order
        submit_button = QPushButton("Submit Work Order")
        submit_button.clicked.connect(self.submit_work_order)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Create Work Order"))
        layout.addWidget(QLabel("Customer ID"))
        layout.addWidget(customer_id)
        layout.addWidget(QLabel("Select Drilling Operation Type"))
        layout.addWidget(drilling_operation)
        layout.addWidget(QLabel("Start Time"))
        layout.addWidget(start_time)
        layout.addWidget(submit_button)

        widget=QWidget()
        widget.setLayout(layout)
        return widget


    def submit_work_order(self):
        customer_id = int(self.findChild(QLineEdit).text())
        drilling_operation = int(self.findChild(QComboBox).currentText())
        start_time = self.findChild(QDateTimeEdit).dateTime().toString("yyyy-MM-dd hh:mm:ss")

        # Add a new entry to the Order database
        order = Order.OrderTable()
        order.add_order(
            customer_id,
            drilling_operation,
            start_time,
            "pending"
        )

        self.table.update()

