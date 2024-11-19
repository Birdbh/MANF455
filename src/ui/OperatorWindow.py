from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QComboBox, QDateTimeEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QMenu)
from PyQt5.QtCore import Qt
from data import Order
from data import Customer
import datetime

from ui.UserWindow import UserWindow

class OperatorWindow(UserWindow):
    def __init__(self, employee_id, employee_name):
        super().__init__(employee_id, employee_name)
        self.customer_table = Customer.CustomerTable()
        self.order_table = Order.OrderTable()
        self.editable_columns = [2, 3, 5]  # Drilling Operation, Start Time, and Pass Quality Control are editable
        self._setup_ui()

    def _setup_ui(self):
        self._create_work_order_widget()
        self._setup_work_order_table()
        self._create_add_customer_widget()
        self._setup_customer_table()

    def _setup_work_order_table(self):
        self.table = QTableWidget(0, 6)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(["Work Order ID", "Customer ID", "Drilling Operation", "Start Time", "Status", "Pass Quality Control"])
        self.table.itemChanged.connect(self._handle_item_changed)

        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)

        self._populate_work_order_table()
        self.content_layout.addWidget(self.table)

    def _setup_customer_table(self):
        self.cust_table = QTableWidget(0, 4)
        self.cust_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cust_table.setHorizontalHeaderLabels(["Customer ID", "Name", "Email", "Address"])
        self._populate_customer_table()
        self.content_layout.addWidget(self.cust_table)

    def _populate_work_order_table(self):
        self.table.clearContents()
        self.table.setRowCount(0)
        work_orders = self.order_table.get_all_orders_from_today()
        for work_order in work_orders:
            self._add_work_order_to_table(work_order)

    def _populate_customer_table(self):
        self.cust_table.clearContents()
        self.cust_table.setRowCount(0)
        customers = self.customer_table.get_all_customers()
        for customer in customers:
            self._add_customer_to_table(customer)

    def _add_work_order_to_table(self, work_order):
        row_idx = self.table.rowCount()
        self.table.insertRow(row_idx)
        items = [
            work_order.orderId,
            work_order.customer_id,
            work_order.drilling_operation,
            work_order.order_date.strftime('%Y-%m-%d %H:%M:%S'),
            work_order.status,
            str(work_order.passQualityControl)
        ]
        for col_idx, item in enumerate(items):
            table_item = QTableWidgetItem(str(item))
            if work_order.status == "Completed" or col_idx not in self.editable_columns:
                table_item.setFlags(table_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row_idx, col_idx, table_item)

    def _add_customer_to_table(self, customer):
        row_idx = self.cust_table.rowCount()
        self.cust_table.insertRow(row_idx)
        items = [
            customer.customerid,
            customer.customername,
            customer.customeremail,
            customer.customeraddress
        ]
        for col_idx, item in enumerate(items):
            table_item = QTableWidgetItem(str(item))
            table_item.setFlags(table_item.flags() & ~Qt.ItemIsEditable)
            self.cust_table.setItem(row_idx, col_idx, table_item)

    def _create_work_order_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Create Work Order"))

        self.customer_id = QLineEdit()
        self.drilling_operation = QComboBox()
        self.drilling_operation.addItems(["1", "2", "3"])
        self.start_time = QDateTimeEdit()
        self.start_time.setMinimumDateTime(datetime.datetime.now())
        self.start_time.setDisplayFormat("yyyy-MM-dd hh:mm:ss")
        self.start_time.setDateTime(datetime.datetime.now())

        for label, w in [("Customer ID", self.customer_id),
                         ("Drilling Operation", self.drilling_operation),
                         ("Start Time", self.start_time)]:
            layout.addWidget(QLabel(label))
            layout.addWidget(w)

        submit_button = QPushButton("Submit Work Order")
        submit_button.clicked.connect(self._submit_work_order)
        layout.addWidget(submit_button)

        self.content_layout.addWidget(widget)

    def _submit_work_order(self):
        customer_id = int(self.customer_id.text())
        drilling_operation = int(self.drilling_operation.currentText())
        start_time = self.start_time.dateTime().toString("yyyy-MM-dd hh:mm:ss")

        if customer_id not in [customer.customerid for customer in self.customer_table.get_all_customers()]:
            QMessageBox.warning(self, "Work Order Submission Failed", "Invalid Customer ID")
            self.customer_id.clear()
            return

        self.order_table.add_order(customer_id, drilling_operation, start_time, "Pending", True)

        self._populate_work_order_table()

        # Clear input fields after submission
        self.customer_id.clear()
        self.drilling_operation.setCurrentIndex(0)
        self.start_time.setDateTime(QDateTimeEdit().dateTime())

    def _create_add_customer_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Add Customer"))

        self.customer_name = QLineEdit()
        self.customer_email = QLineEdit()
        self.customer_address = QLineEdit()

        for label, w in [("Customer Name", self.customer_name),
                         ("Customer Email", self.customer_email),
                         ("Customer Address", self.customer_address)]:
            layout.addWidget(QLabel(label))
            layout.addWidget(w)

        submit_button = QPushButton("Add Customer")
        submit_button.clicked.connect(self._submit_customer)
        layout.addWidget(submit_button)

        self.content_layout.addWidget(widget)

    def _submit_customer(self):
        customer_name = self.customer_name.text()
        customer_email = self.customer_email.text()
        customer_address = self.customer_address.text()

        self.customer_table.add_customer(customer_name, customer_email, customer_address)

        self._populate_customer_table()

        # Clear input fields after submission
        self.customer_name.clear()
        self.customer_email.clear()
        self.customer_address.clear()

    def _handle_item_changed(self, item):
        if item.column() in self.editable_columns:
            row = item.row()
            work_order_id = int(self.table.item(row, 0).text())
            column = item.column()
            new_value = item.text()

            if column == 2:  # Drilling Operation
                self.order_table.update_drilling_operation(work_order_id, int(new_value))
            elif column == 3:  # Start Time
                self.order_table.update_start_time(work_order_id, new_value)
            elif column == 5: # Quality Check
                self.order_table.update_pass_quality_control(work_order_id, new_value.lower() == 'true')

    def _show_context_menu(self, position):
        row = self.table.rowAt(position.y())
        if row >= 0:  # Only show menu if user clicked on a row
            menu = QMenu()
            delete_action = menu.addAction("Delete Order")
            action = menu.exec_(self.table.viewport().mapToGlobal(position))
            
            if action == delete_action:
                order_id = int(self.table.item(row, 0).text())
                self._delete_order(order_id, row)

    def _delete_order(self, order_id, row):
        status = self.table.item(row, 4).text()
        
        if status == "Completed":
            QMessageBox.warning(self, "Cannot Delete", "Completed orders cannot be deleted")
            return
            
        reply = QMessageBox.question(self, 'Delete Order', 
                                'Are you sure you want to delete this order?',
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.order_table.delete_order(order_id)
                self.table.removeRow(row)
                QMessageBox.information(self, "Success", "Order deleted successfully")
            except:
                QMessageBox.warning(self, "Error", "Failed to delete order")