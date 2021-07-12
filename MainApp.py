import sys

from PyQt6 import QtWidgets
from ui_about_dialog import Ui_DialogAbout
from PyQt6.QtWidgets import (QFileDialog, QApplication, QDialog, QMainWindow)
from ui_main_window import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.openAboutDialog)
        self.btn_Page.clicked.connect(self.ChangePage)
        self.btn_ExePath.clicked.connect(self.SelectExePath)

    def openAboutDialog(self):
        AboutDialog()

    def ChangePage(self):
        if self.stackedWidget.currentIndex() == 0:
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.stackedWidget.setCurrentIndex(0)

    def SelectExePath(self):
        global exePath
        exePath = QFileDialog.getOpenFileName(self, caption = 'Select EneryPLAN.exe file',filter = 'energyPLAN.exe')
        self.txt_ExePath.setText(exePath[0])


class AboutDialog(QDialog, Ui_DialogAbout):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.exec()
        

app = QApplication(sys.argv)
mainWindow = Window()
mainWindow.show()
sys.exit(app.exec())