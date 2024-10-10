from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget,QLineEdit,QComboBox,QTimeEdit,QDateTimeEdit)

#from data2 import MESDatabase
from data2 import Order

class OperatorWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Operator Template"))
        layout.addWidget(self.widget_to_create_work_order())
        layout.addWidget(QPushButton("View Work Orders"))

        self.setLayout(layout)
        

    def widget_to_create_work_order(self):
        # Create a widget to create a work order
        #This should have the following fields:
        #Enter number for customer id
        #dropdown to select drilling operation
        #Time select to select the start time of the operation
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


#create a function to handle when the submit_buttom is clicked
#this function should take the values from the fields and create a work order
#this function should then call the MES logic to create the work order
    def submit_work_order(self):
        customer_id = int(self.findChild(QLineEdit).text())
        drilling_operation = int(self.findChild(QComboBox).currentText())
        start_time = self.findChild(QDateTimeEdit).dateTime().toString("yyyy-MM-dd hh:mm:ss")
        print(type(customer_id))
        print(customer_id)
        print(type(drilling_operation))
        print(drilling_operation)
        print(type(start_time))
        print(start_time)
        # Add a new entry to the Order database
        order = Order.OrderTable()
        order.add_order(
            customer_id,
            drilling_operation,
            start_time,
            "pending"
        )
        print(order.get_all_orders())

