from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QComboBox, QDateTimeEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt
from data import Order

from ui.UserWindow import UserWindow

class OperatorWindow(UserWindow):
    def __init__(self, employee_id, employee_name):
        super().__init__(employee_id, employee_name)
        self.order_table = Order.OrderTable()
        self.editable_columns = [2, 3, 5]  # Drilling Operation, Start Time, and Pass Quality Control are editable
        self._setup_ui()

    def _setup_ui(self):
        self._create_work_order_widget()
        self._setup_work_order_table()

    def _setup_work_order_table(self):
        self.table = QTableWidget(0, 6)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(["Work Order ID", "Customer ID", "Drilling Operation", "Start Time", "Status", "Pass Quality Control"])
        self.table.itemChanged.connect(self._handle_item_changed)
        self._populate_work_order_table()
        self.content_layout.addWidget(self.table)

    def _populate_work_order_table(self):
        work_orders = self.order_table.get_all_orders()
        for work_order in work_orders:
            self._add_work_order_to_table(work_order)

    def _add_work_order_to_table(self, work_order):
        #TODO: This is bad, the table should update from changes in the database, right now inserting manually is bad
        row_idx = self.table.rowCount()
        self.table.insertRow(row_idx)
        for col_idx, item in enumerate(work_order):
            table_item = QTableWidgetItem(str(item))
            if col_idx not in self.editable_columns:
                table_item.setFlags(table_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row_idx, col_idx, table_item)

    def _create_work_order_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Create Work Order"))

        self.customer_id = QLineEdit()
        self.drilling_operation = QComboBox()
        self.drilling_operation.addItems(["1", "2", "3"])
        self.start_time = QDateTimeEdit()

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

        self.order_table.add_order(customer_id, drilling_operation, start_time, "pending", True)
        new_order_id = self.order_table.get_last_row_id()

        new_work_order = (new_order_id, customer_id, drilling_operation, start_time, "pending", True)
        self._add_work_order_to_table(new_work_order)

        # Clear input fields after submission
        self.customer_id.clear()
        self.drilling_operation.setCurrentIndex(0)
        self.start_time.setDateTime(QDateTimeEdit().dateTime())

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
                self.order_table.update_pass_quality_control(work_order_id, new_value)

            print(self.order_table.get_all_orders())

    def update_order_status(self, work_order_id, new_status):
        # Update the status in the database
        self.order_table.update_status(work_order_id, new_status)

        # Update the status in the table
        for row in range(self.table.rowCount()):
            if int(self.table.item(row, 0).text()) == work_order_id:
                self.table.item(row, 4).setText(new_status)
                break