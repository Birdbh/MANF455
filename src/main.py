import sys
from PyQt5.QtWidgets import QApplication
from ui.MainWindow import MainWindow
from data import Customer
from coms import ComsManager

def main():
    app = QApplication(sys.argv)

    main_window = MainWindow()
    coms_manager = ComsManager.ComsManager(main_window)

    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()