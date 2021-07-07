import sys

from PyQt6.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox)
#from PyQt6.uic import loadUi

from ui_mainapp import Ui_MainWindow

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)



app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec())