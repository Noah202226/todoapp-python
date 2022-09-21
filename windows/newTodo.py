from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox

class NewTodoDialog(QDialog):
    def __init__(self, data, reload):
        super().__init__()

        uic.loadUi('./ui/newTodo.ui', self)

        self.data = data
        self.reload = reload
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.todoNameTxt.setFocus()
        
        self.saveBtn.clicked.connect(self.saveTodo)
        self.cancelBtn.clicked.connect(self.cancel)

        print(data)

    def saveTodo(self):
        if self.todoNameTxt.text() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('No Task Name! Invalid to save')
            msg.exec()
        else:
            self.data.append({'name': self.todoNameTxt.text(), 'label': self.todoLabelTxt.toPlainText()})
            self.close()
            self.reload()
        

    def cancel(self):
        self.close()