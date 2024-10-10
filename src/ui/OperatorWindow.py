from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget,QLineEdit,QComboBox,QTimeEdit,QDateTimeEdit)

from data import MESDatabase
from data import Orders

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
        drilling_operation.addItem("Drilling Operation 1")
        drilling_operation.addItem("Drilling Operation 2")
        drilling_operation.addItem("Drilling Operation 3")
        start_time = QDateTimeEdit()
        #Create a button to submit the work order
        submit_button = QPushButton("Submit Work Order")
        submit_button.clicked.connect(self.submit_work_order)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Create Work Order"))
        layout.addWidget(QLabel("Customer ID"))
        layout.addWidget(customer_id)
        layout.addWidget(QLabel("Drilling Operation"))
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
        customer_id = self.findChild(QLineEdit).text()
        drilling_operation = self.findChild(QComboBox).currentText()
        start_time = self.findChild(QDateTimeEdit).dateTime()
        

        # Add a new entry to the Order database
        db = MESDatabase.MESDatabase("mes.db")
        db.operators.insert({
            'customer_id': customer_id,
            'employee_id': 1,  # Assuming employee_id is fixed or obtained elsewhere in the actual implementation
            'order_date': start_time,
            'status': 'pending'  # Example status, this can be changed based on your requirements
        })

