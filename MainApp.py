import sys
import os
import subprocess

from datetime import datetime
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox)
from ui_main_window import Ui_MainWindow
from CSV_Parser import csvParser

class Window(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Connections()

        global logFile
        if os.path.exists(os.getcwd() + "/log.txt") == False:
            logFile = open(os.getcwd() + "/log.txt", 'w+')
        else:
            logFile = open(os.getcwd() + "/log.txt", 'w')

        self.txt_Log.setSource(QUrl('file:///' + os.getcwd().replace('\\','/') + "/log.txt"))

    def Connections(self):
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.openAboutDialog)
        self.btn_Page.clicked.connect(self.ChangePage)
        self.btn_ExePath.clicked.connect(self.SelectExePath)
        self.btn_IPF.clicked.connect(self.SelectIPF)
        self.btn_OPD.clicked.connect(self.SelectOPD)
        self.btn_Exec.clicked.connect(self.ProcessFile)

    def openAboutDialog(self):
        QMessageBox.about(self, 'About', 'Hi, I\'m developer')

    def ChangePage(self):
        if self.stackedWidget.currentIndex() == 0:
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.stackedWidget.setCurrentIndex(0)

    def SelectExePath(self):
        filePath = QFileDialog.getOpenFileName(
            self, 'Select EneryPLAN.exe file', filter='energyPLAN.exe')
        self.txt_ExePath.setText(filePath[0])

    def SelectIPF(self):
        filePath = QFileDialog.getOpenFileName(
            self, 'Select Input file', filter='*.txt')
        self.txt_IPF.setText(filePath[0])

    def SelectOPD(self):
        global path_OPD
        path_OPD = QFileDialog.getExistingDirectory(
            self, 'Select ouput directory', '', options=QFileDialog.Option.ShowDirsOnly)
        self.txt_OPD.setText(path_OPD)

    def ProcessFile(self):
        timeStamp = datetime.now().strftime('%y%m%d%H%M%S')

        if self.txt_ExePath.text() != '' and self.txt_IPF.text() != '' and self.txt_OPD.text() != '':
            subprocess.run([self.txt_ExePath.text(), "-i", self.txt_IPF.text(), "-ascii", path_OPD + '/ops.txt'])
            csvParser(path_OPD + '/ops.txt', timeStamp)
            logFile.write('Success\n')
            
            if self.cb_OpenOPD.isChecked:
                subprocess.run(['explorer', os.path.realpath(path_OPD)])

        else:
            QMessageBox.critical(self, 'Error', 'Fuck')
            logFile.write('Failed\n')


app = QApplication(sys.argv)
mainWindow = Window()
mainWindow.show()
sys.exit(app.exec())
