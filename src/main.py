import sys
from PyQt5.QtWidgets import QApplication
from ui.MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow(0)
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()