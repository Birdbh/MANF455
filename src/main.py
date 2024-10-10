import sys
from PyQt5.QtWidgets import QApplication
#from ui.MainWindow import MainWindow

from data2 import DatabaseConnector
from data2 import Order


def main():
    # app = QApplication(sys.argv)
    # main_window = MainWindow(0)
    # main_window.show()
    # sys.exit(app.exec_())
    order = Order.OrderTable()
    order.add_order(1, 1, "2021-05-01", "pending")
    print(order.get_all_orders())

if __name__ == '__main__':
    main()