import sys, subprocess

from datetime import datetime
from PyQt6 import QtWidgets
from ui_about_dialog import Ui_DialogAbout
from PyQt6.QtWidgets import (QFileDialog, QApplication, QDialog, QMainWindow)
from ui_main_window import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Connections()

    def Connections(self):
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.openAboutDialog)
        self.btn_Page.clicked.connect(self.ChangePage)
        self.btn_ExePath.clicked.connect(self.SelectExePath)
        self.btn_IPF.clicked.connect(self.SelectIPF)
        self.btn_OPD.clicked.connect(self.SelectOPD)
        self.btn_Exec.clicked.connect(self.ProcessFile)

    def openAboutDialog(self):
        AboutDialog()

    def ChangePage(self):
        if self.stackedWidget.currentIndex() == 0:
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.stackedWidget.setCurrentIndex(0)

    def SelectExePath(self):
        filePath = QFileDialog.getOpenFileName(self, 'Select EneryPLAN.exe file', filter = 'energyPLAN.exe')
        self.txt_ExePath.setText(filePath[0])

    def SelectIPF(self):
        filePath = QFileDialog.getOpenFileName(self, 'Select Input file', filter = '*.txt')
        self.txt_IPF.setText(filePath[0])

    def SelectOPD(self):
        global path_OPD
        path_OPD = QFileDialog.getExistingDirectory(self,'Select ouput directory', '', options= QFileDialog.Option.ShowDirsOnly)
        self.txt_OPD.setText(path_OPD)

    def ProcessFile(self):
        timeStamp = datetime.now().strftime('%y%m%d%H%M%S')
        subprocess.run([self.txt_ExePath.text(), "-i", self.txt_IPF.text(), "-ascii", path_OPD + '/ops1_' + timeStamp + '.txt'])



class AboutDialog(QDialog, Ui_DialogAbout):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.exec()
        

app = QApplication(sys.argv)
mainWindow = Window()
mainWindow.show()
sys.exit(app.exec())