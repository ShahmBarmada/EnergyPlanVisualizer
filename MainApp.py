import sys
from ui_about_dialog import Ui_DialogAbout
from PyQt6.QtWidgets import (QApplication, QDialog, QMainWindow)
from ui_main_window import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.openAboutDialog)

    def openAboutDialog(self):
        print('yay')
        AboutDialog()


class AboutDialog(QDialog, Ui_DialogAbout):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.exec()
        
        

app = QApplication(sys.argv)
mainWindow = Window()
mainWindow.show()
sys.exit(app.exec())