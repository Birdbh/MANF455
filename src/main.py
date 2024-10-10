import sys
from PyQt5.QtWidgets import QApplication
from ui.MainWindow import MainWindow

from data2 import DatabaseConnector
from data2 import Order
from data2 import Employee


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()