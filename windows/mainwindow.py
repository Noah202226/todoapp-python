from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView, QMessageBox, QTextEdit, QApplication
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtCore import QRect, QRectF, Qt
from PyQt5.QtPrintSupport import QPrinter, QPrinterInfo

from datetime import datetime
from textwrap import wrap

from .newTodo import NewTodoDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('./ui/main.ui', self)

        self.setGeometry(500,30, 451, 687)

        self.printTodoBtn.clicked.connect(self.print)
        self.newTodoBtn.clicked.connect(self.openNew)
        
        self.todolist = []
        self.reload()
        self.itemlist = []
        self.reloadFrame3()

        printers = QPrinterInfo.availablePrinterNames()
        self.comboBox.addItems(printers)

        self.frame2.hide()
        self.frame3.hide()
        # self.frame2TaskDescription.setLineWrapMode(QTextEdit.NoWrap)
        # Table
        self.todoTableWidget.setColumnWidth(1, 150)
        self.todoTableWidget.setColumnWidth(2, 230)
        self.todoTableWidget.setColumnHidden(0, True)
        self.todoTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.todoTableWidget.setSelectionMode()

        self.todoTableWidget.doubleClicked.connect(self.showSomething)
        self.taskType.currentTextChanged.connect(self.changeType)
        self.newItemBtn.clicked.connect(self.saveNewItem)
        self.frame3ResetBtn.clicked.connect(self.resetField)
    
    # def center(self):
    #     frameGeometry = self.frameGeometry()
    #     screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
    #     print(QApplication.desktop().cursor().pos())
    #     centerPoint = QApplication.desktop().screenGeometry(screen).center()
    #     print(centerPoint)
    #     frameGeometry.moveCenter(centerPoint)
    #     self.move(frameGeometry.topLeft())
  
    
    def resetField(self):
        self.itemlist = []
        self.frame3ItemName.setText('')
        self.frame3Qty.setValue(1)
        self.frame3Price.setValue(1)
        self.frame3TotalAmount.setValue(0)
        self.reloadFrame3()

    def changeType(self):
        if self.taskType.currentText() == 'LIST':
            self.frame1.show()
            self.frame2.hide()
            self.frame3.hide()
        elif self.taskType.currentText() == 'LONGTASK':
            self.frame1.hide()
            self.frame2.show()
            self.frame3.hide()
        elif self.taskType.currentText() == 'NOEMSPRINT':
            self.frame1.hide()
            self.frame2.hide()
            self.frame3.show()

    def showSomething(self):
        row = self.todoTableWidget.currentRow()
        todoname = self.todoTableWidget.item(row, 1).text()

        for i in range(len(self.todolist)):
            if self.todolist[i]['name'] == todoname:
                del self.todolist[i]
                break
        
        self.reload()
        
    def reload(self):
        row = 0
        self.todoTableWidget.setRowCount(len(self.todolist))
        for todo in self.todolist:
            self.todoTableWidget.setItem(row, 1, QTableWidgetItem(todo['name']))
            self.todoTableWidget.setItem(row, 2, QTableWidgetItem(todo['label']))
            row = row + 1
    def reloadFrame3(self):
        row = 0
        totalAmount = 0
        self.frame3ItemTbl.setRowCount(len(self.itemlist))
        for item in self.itemlist:
            print(item)
            self.frame3ItemTbl.setItem(row, 0, QTableWidgetItem(str(item['qty'])))
            self.frame3ItemTbl.setItem(row, 1, QTableWidgetItem(item['name']))
            self.frame3ItemTbl.setItem(row, 2, QTableWidgetItem(str(item['price'])))
            self.frame3ItemTbl.setItem(row, 3, QTableWidgetItem(str(item['total'])))
            totalAmount += item['total']
            self.frame3TotalAmount.setValue(totalAmount)
            row = row + 1

    def print(self):
        if self.taskType.currentText() == 'LIST':
            try:
                myprinter = QPrinter(QPrinter.HighResolution)
                myprinter.setPrinterName(self.comboBox.currentText())
                mypainter = QPainter()
                
                mypainter.begin(myprinter)
                mypainter.drawText(2, 20 , f'TODO APP - TYPE {self.taskType.currentText()}')
                x = 2
                y = 50
                task = 0

                for todo in self.todolist:
                    mypainter.drawText(x, y, f"Task {task + 1} - {todo['name']}")
                    todolabelWrap = wrap(todo['label'], 20)
                    
                    for t in todolabelWrap:
                        mypainter.drawText(x, y + 30, t)
                        y += 30

                    y = y + 70
                    task = task + 1

                mypainter.end()

            except Exception as ex:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(ex)
                msg.exec()
        elif self.taskType.currentText() == 'NOEMSPRINT':
            if self.frame3RecieptName.text() == "":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText('Reciept Name is Required.')
                msg.exec()
            else:
                try:
                    myprinter = QPrinter(QPrinter.HighResolution)
                    myprinter.setPrinterName(self.comboBox.currentText())
                    mypainter = QPainter()
                    
                    mypainter.begin(myprinter)

                    mypainter.setFont(QFont('Verdana', 10, QFont.Bold))
                    mypainter.drawText(2, 25 , self.frame3RecieptName.text())
                    mypainter.setFont(QFont('Verdana', 7))
                    mypainter.drawText(2, 50 , datetime.now().strftime("%A - %m/%d/%Y, %I:%M:%S %p"))
                    x = 2
                    y = 50
                    task = 0

                    for item in self.itemlist:
                        mypainter.drawText(x, y + 40, f"{item['name']}")
                        mypainter.drawText(x, y + 70, f"{item['qty']}  *   {item['price']}                          {item['total']}")
                        mypainter.drawText(x, y + 90, f"-----------------------------------------------------------------------------")
                        y = y + 70
                        task = task + 1
                    mypainter.drawText(x, y + 40, f'No. of Items                          {task}')
                    mypainter.drawText(x, y + 80, f'Total Amount                        {self.frame3TotalAmount.text()}')
                    mypainter.drawText(x, y + 120, f'THANK YOU, GOD BLESS.')
                    mypainter.end()

                except Exception as ex:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(str(ex))
                    msg.exec()

        elif self.taskType.currentText() == 'LONGTASK':
            try:
                myprinter = QPrinter(QPrinter.HighResolution)
                myprinter.setPrinterName(self.comboBox.currentText())
                mypainter = QPainter()
                
                mypainter.begin(myprinter)

                x = 2
                y = 120
                width = 300
                height = 100
                
                mypainter.drawText(2, 20 , f'TODO APP - TYPE {self.taskType.currentText()}')
                # print(wrapText)
                # print(f'Length of text: {len(text)}')
                # for line in text.split('\n'):
                #     print(f'line: {line}')
                #     word = line.strip()
                #     print(f'word: {word}')
                #     if word:
                #         print(word)
                #         lineCount += 1
                #         height += 25

                print(f'height: {height}')
                # print(lineCount)
                rect = QRectF(x, 120, width, height)
                mypainter.drawText(2, 80, f"Task Name: {self.frame2TaskName.text()}")
                # mypainter.drawText(x, 100, text)
                

                lineCount = 0

                text = self.frame2TaskDescription.toPlainText()
                wrapText = wrap(text, 25)
                print(len(wrapText))
                for t in wrapText:
                    print(len(t))
                    mypainter.drawText(2, y, t)
                    y += 40

                mypainter.end()

            except Exception as ex:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(ex)
                msg.exec()

    def saveNewItem(self):

        if self.frame3ItemName.text() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Please enter item name')
            msg.exec()
        else:
            self.itemlist.append({'name': self.frame3ItemName.text(), 'qty': self.frame3Qty.value(), 'price': self.frame3Price.value(), 'total': self.frame3Qty.value() * self.frame3Price.value()})
            self.reloadFrame3()

            # Reset Field
            self.frame3ItemName.setText('')
            self.frame3Qty.setValue(1)
            self.frame3Price.setValue(0)

    def openNew(self):
        print('opening')

        newTodoWin = NewTodoDialog(self.todolist, self.reload)
        newTodoWin.exec()