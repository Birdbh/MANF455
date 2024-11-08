from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QComboBox, QDateTimeEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QMenu)
from PyQt5.QtCore import Qt
from data.Order import OrderTable
from data.Customer import CustomerTable
import datetime

from ui.UserWindow import UserWindow

class OperatorWindow(UserWindow):
    def __init__(self, employee_id, employee_name):
        super().__init__(employee_id, employee_name)
        self.customer_table = CustomerTable()
        self.order_table = OrderTable()
        #TODO: This should not be hard coded but changed to something that populates based on string comparison and a global CONST variable list
        self.editable_columns = [2, 3, 5]  # Drilling Operation, Start Time, and Pass Quality Control are editable
        self.setup_ui()

    def setup_ui(self):
        self.create_order_widget()
        self.setup_table(self.create_order_table(), ["Order ID", "Customer ID", "Drilling Operation", "Start Time", "Status", "Pass Quality Control"], self.populate_order_table, self.handle_item_changed)
        self.create_customer_widget()
        self.setup_table(self.create_customer_table(), ["Customer ID", "Customer Name", "Customer Email", "Customer Address"], self.populate_customer_table)

    def setup_table(self, table, headers, populate_table, item_change_handler=None):
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setHorizontalHeaderLabels(headers)
        if item_change_handler:
            table.itemChanged.connect(item_change_handler)
            table.setContextMenuPolicy(Qt.CustomContextMenu)
            table.customContextMenuRequested.connect(self.show_context_menu)
        populate_table()
        self.content_layout.addWidget(table)

    def create_order_table(self):
        #TODO: Change the number of columns of the QTableWidget to be the length of the number of columns of the OrderTable not some hardcoded value which it current is
        self.order_table_widget = QTableWidget(0, 6)
        return self.order_table_widget

    def create_customer_table(self):
        #TODO: Change the number of columns of the QTableWidget to be the length of the number of columns of the CustomerTable not some hardcoded value which it current is
        self.customer_table_widget = QTableWidget(0, 4)
        return self.customer_table_widget
    
    def populate_order_table(self):
        self.populate_table(self.order_table_widget, self.order_table.get_all_orders_from_today(), self.add_order_row)

    def populate_customer_table(self):
        self.populate_table(self.customer_table_widget, self.customer_table.get_all_customers(), self.add_customer_row)
    
    def populate_table(self, table, data_list, add_row_function):
        table.clearContents()
        table.setRowCount(0)
        for data in data_list:
            add_row_function(data)

    def add_order_row(self, work_order):
        row_idx = self.order_table_widget.rowCount()
        self.order_table_widget.insertRow(row_idx)
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
            self.order_table_widget.setItem(row_idx, col_idx, table_item)

    def add_customer_row(self, customer):
        row_idx = self.customer_table_widget.rowCount()
        self.customer_table_widget.insertRow(row_idx)
        items = [
            customer.customerid,
            customer.customername,
            customer.customeremail,
            customer.customeraddress
        ]
        for col_idx, item in enumerate(items):
            table_item = QTableWidgetItem(str(item))
            table_item.setFlags(table_item.flags() & ~Qt.ItemIsEditable)
            self.customer_table_widget.setItem(row_idx, col_idx, table_item)

    def create_order_widget(self):
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
        submit_button.clicked.connect(self.submit_order)
        layout.addWidget(submit_button)

        self.content_layout.addWidget(widget)

    def submit_order(self):
        customer_id = int(self.customer_id.text())
        drilling_operation = int(self.drilling_operation.currentText())
        start_time = self.start_time.dateTime().toString("yyyy-MM-dd hh:mm:ss")

        if customer_id not in [customer.customerid for customer in self.customer_table.get_all_customers()]:
            QMessageBox.warning(self, "Work Order Submission Failed", "Invalid Customer ID")
            self.customer_id.clear()
            return

        self.order_table.add_order(customer_id, drilling_operation, start_time, "Pending", True)

        self.populate_order_table()

        # Clear input fields after submission
        self.customer_id.clear()
        self.drilling_operation.setCurrentIndex(0)
        self.start_time.setDateTime(QDateTimeEdit().dateTime())

    def create_customer_widget(self):
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
        submit_button.clicked.connect(self.submit_customer)
        layout.addWidget(submit_button)

        self.content_layout.addWidget(widget)

    def submit_customer(self):
        customer_name = self.customer_name.text()
        customer_email = self.customer_email.text()
        customer_address = self.customer_address.text()

        self.customer_table.add_customer(customer_name, customer_email, customer_address)

        self.populate_customer_table()

        # Clear input fields after submission
        self.customer_name.clear()
        self.customer_email.clear()
        self.customer_address.clear()

    def handle_item_changed(self, item):
        if item.column() in self.editable_columns:
            row = item.row()
            work_order_id = int(self.order_table_widget.item(row, 0).text())
            column = item.column()
            new_value = item.text()

            if column == 2:  # Drilling Operation
                self.order_table.update_drilling_operation(work_order_id, int(new_value))
            elif column == 3:  # Start Time
                self.order_table.update_start_time(work_order_id, new_value)
            elif column == 5: # Quality Check
                self.order_table.update_pass_quality_control(work_order_id, new_value.lower() == 'true')

    def show_context_menu(self, position):
        row = self.order_table_widget.rowAt(position.y())
        if row >= 0:  # Only show menu if user clicked on a row
            menu = QMenu()
            delete_action = menu.addAction("Delete Order")
            action = menu.exec_(self.order_table_widget.viewport().mapToGlobal(position))
            
            if action == delete_action:
                order_id = int(self.order_table_widget.item(row, 0).text())
                self.delete_order(order_id, row)

    def delete_order(self, order_id, row):
        status = self.order_table_widget.item(row, 4).text()
        
        if status == "Completed":
            QMessageBox.warning(self, "Cannot Delete", "Completed orders cannot be deleted")
            return
            
        reply = QMessageBox.question(self, 'Delete Order', 
                                'Are you sure you want to delete this order?',
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.order_table.delete_order(order_id)
                self.order_table_widget.removeRow(row)
                QMessageBox.information(self, "Success", "Order deleted successfully")
            except:
                QMessageBox.warning(self, "Error", "Failed to delete order")

    # def create_order_widget(self):
    #     self.create_form_widget("Create Work Order", [
    #         ("Customer ID", QLineEdit(), lambda: self.order_form.customer_id),
    #         ("Drilling Operation", self.create_combo(["1", "2", "3"]), lambda: self.order_form.drilling_operation),
    #         ("Start Time", self.create_datetime_edit(), lambda: self.order_form.start_time)
    #     ], self.submit_order)

    # def create_customer_widget(self):
    #     self.create_form_widget("Add Customer", [
    #         ("Customer Name", QLineEdit(), lambda: self.customer_form.customer_name),
    #         ("Customer Email", QLineEdit(), lambda: self.customer_form.customer_email),
    #         ("Customer Address", QLineEdit(), lambda: self.customer_form.customer_address)
    #     ], self.submit_customer)

    # def create_form_widget(self, title, fields, submit_action):
    #     widget = QWidget()
    #     layout = QVBoxLayout(widget)
    #     layout.addWidget(QLabel(title))
        
    #     if title == "Create Work Order":
    #         self.order_form = widget
    #     elif title == "Add Customer":
    #         self.customer_form = widget
        
    #     for label, field, assign_fn in fields:
    #         layout.addWidget(QLabel(label))
    #         layout.addWidget(field)
    #         assign_fn().set(field)
        
    #     submit_button = QPushButton(f"Submit {title.split()[0]}")
    #     submit_button.clicked.connect(submit_action)
    #     layout.addWidget(submit_button)
        
    #     self.content_layout.addWidget(widget)

    # def create_combo(self, items):
    #     combo = QComboBox()
    #     combo.addItems(items)
    #     return combo

    # def create_datetime_edit(self):
    #     dt_edit = QDateTimeEdit()
    #     dt_edit.setMinimumDateTime(datetime.datetime.now())
    #     dt_edit.setDisplayFormat("yyyy-MM-dd hh:mm:ss")
    #     dt_edit.setDateTime(datetime.datetime.now())
    #     return dt_edit

    # def submit_order(self):
    #     customer_id = int(self.order_form.customer_id.text())
    #     if not self.is_valid_customer_id(customer_id):
    #         return self.show_warning("Invalid Customer ID")
        
    #     self.order_table.add_order(customer_id, int(self.order_form.drilling_operation.currentText()), self.order_form.start_time.dateTime().toString("yyyy-MM-dd hh:mm:ss"), "Pending", True)
    #     self.populate_order_table()
    #     self.clear_fields([self.order_form.customer_id, self.order_form.drilling_operation, self.order_form.start_time])

    # def submit_customer(self):
    #     self.customer_table.add_customer(self.customer_form.customer_name.text(), self.customer_form.customer_email.text(), self.customer_form.customer_address.text())
    #     self.populate_customer_table()
    #     self.clear_fields([self.customer_form.customer_name, self.customer_form.customer_email, self.customer_form.customer_address])

    # def is_valid_customer_id(self, customer_id):
    #     return customer_id in [customer.customerid for customer in self.customer_table.get_all_customers()]

    # def show_warning(self, message):
    #     QMessageBox.warning(self, "Submission Failed", message)
    #     self.customer_id.clear()

    # def clear_fields(self, fields):
    #     for field in fields:
    #         if isinstance(field, QComboBox):
    #             field.setCurrentIndex(0)
    #         elif isinstance(field, QDateTimeEdit):
    #             field.setDateTime(QDateTimeEdit().dateTime())
    #         else:
    #             field.clear()

    # def handle_item_changed(self, item):
    #     if item.column() not in self.editable_columns:
    #         return
    #     work_order_id = int(self.order_table_widget.item(item.row(), 0).text())
    #     new_value = item.text()

    #     update_methods = {
    #         2: lambda val: self.order_table.update_drilling_operation(work_order_id, int(val)),
    #         3: lambda val: self.order_table.update_start_time(work_order_id, val),
    #         5: lambda val: self.order_table.update_pass_quality_control(work_order_id, val.lower() == 'true')
    #     }
    #     update_methods[item.column()](new_value)

    # def show_context_menu(self, position):
    #     row = self.order_table_widget.rowAt(position.y())
    #     if row < 0:
    #         return
    #     menu = QMenu()
    #     delete_action = menu.addAction("Delete Order")
    #     action = menu.exec_(self.order_table_widget.viewport().mapToGlobal(position))

    #     if action == delete_action:
    #         self.confirm_delete_order(row)

    # def confirm_delete_order(self, row):
    #     order_id = int(self.order_table_widget.item(row, 0).text())
    #     if self.order_table_widget.item(row, 4).text() == "Completed":
    #         return QMessageBox.warning(self, "Cannot Delete", "Completed orders cannot be deleted")

    #     if QMessageBox.question(self, 'Delete Order', 'Are you sure you want to delete this order?', QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
    #         self.delete_order(order_id, row)

    # def delete_order(self, order_id, row):
    #     try:
    #         self.order_table.delete_order(order_id)
    #         self.order_table_widget.removeRow(row)
    #         QMessageBox.information(self, "Success", "Order deleted successfully")
    #     except:
    #         QMessageBox.warning(self, "Error", "Failed to delete order")