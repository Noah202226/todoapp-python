from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView
from PyQt5.QtGui import QPainter
from PyQt5.QtPrintSupport import QPrinter

from .newTodo import NewTodoDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('./ui/main.ui', self)

        self.printTodoBtn.clicked.connect(self.print)
        self.newTodoBtn.clicked.connect(self.openNew)
        
        self.todolist = []
        self.reload()

        # Table
        self.todoTableWidget.setColumnWidth(1, 150)
        self.todoTableWidget.setColumnWidth(2, 230)
        self.todoTableWidget.setColumnHidden(0, True)
        self.todoTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.todoTableWidget.setSelectionMode()

        self.todoTableWidget.doubleClicked.connect(self.showSomething)

    def showSomething(self):
        row = self.todoTableWidget.currentRow()
        todoname = self.todoTableWidget.item(row, 1).text()

        for i in range(len(self.todolist)):
            if self.todolist[i]['name'] == todoname:
                del self.todolist[i]
                break
        
        self.reload()
        
    def reload(self):
        print('reloading ...')
        
        row = 0
        self.todoTableWidget.setRowCount(len(self.todolist))
        for todo in self.todolist:
            self.todoTableWidget.setItem(row, 1, QTableWidgetItem(todo['name']))
            self.todoTableWidget.setItem(row, 2, QTableWidgetItem(todo['label']))
            row = row + 1

    def print(self):
        print('printing ...')

        myprinter = QPrinter(QPrinter.HighResolution)
        myprinter.setPrinterName('XP-58')
        mypainter = QPainter()
        
        mypainter.begin(myprinter)
        
        mypainter.drawText(10, 20 , "NOAHS TODO LIST")
        x = 10
        y = 50
        task = 0

        for todo in self.todolist:
            mypainter.drawText(x, y, f"Task {task + 1} - {todo['name']}")
            mypainter.drawText(x, y + 30, f'=>{todo["label"]}')

            y = y + 70
            task = task + 1

        mypainter.end()

        
    def openNew(self):
        print('opening')

        newTodoWin = NewTodoDialog(self.todolist, self.reload)
        newTodoWin.exec()