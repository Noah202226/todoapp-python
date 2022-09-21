import sys

from PyQt5.QtWidgets import QApplication

from windows import mainwindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = mainwindow.MainWindow()
    win.show()

    sys.exit(app.exec_())