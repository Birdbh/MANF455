from data.DatabaseManager import DatabaseManager
# from data import Employee
# from data import Customers
from data.Orders import Orders

class MESDatabase:
    def __init__(self, db_name: str):
        self.db_manager = DatabaseManager(db_name)
        # self.employees = Employee(self.db_manager)
        # self.customers = Customers(self.db_manager)
        self.orders = Orders(self.db_manager)