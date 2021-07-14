import sys
import os
import subprocess
import pandas as pd

from datetime import datetime
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox)
from pandas.core.frame import DataFrame
from ui_main_window import Ui_MainWindow
from CSV_Parser import csvParser

yList = {'Added Export Payment':'0030','Boiler 1':'0005','Boiler 2':'0008','Boiler 3':'0015','Combined Heat & Power 2':'0006','Combined Heat & Power Electricity Production':'0023','Combined Heat and Power 3':'0013','Combined Steam & Heat Electricity Production':'0022','Combined Steam & Heat Production':'0400','Critical Electricity Excess Production':'0027','Desalination':'2200','District Cooling':'2100','District Heat Demand':'0004','Electricity Demand':'0001','Electricity Demand Cooling':'0002','Electricity Heat 2':'0009','Electricity Heat 3':'0016','Electrolyser 2':'0010','Electrolyser 3':'0017','Electrolyser Gr.2':'1100','Electrolyser Gr.3':'1200','EV & V2G (Transport)':'1300','Exorted Electricity':'0026','Exportable Electricity Excess Production':'0028','Exports Payment':'1600','Fixed Export / Import':'0003','Flexible Electricity demand':'0020','Gas Grid Demand & Balance':'2300','Geothermal Heat Production':'0500','Heat Balance Gr.2':'0012','Heat BalanceGgr.3':'0019','Heat Pump 2':'0007','Heat Pump 3':'0014','Heat Pump Electricity Production':'0021','Hydrolic Powers':'0200','Import Payment':'0029','Imported Electricity':'0025','Individual Electricity':'1800','Individual Heat 1':'1700','Individual Heat 2':'1900','Market Prices':'1500','Nordpool Prices':'1400','Nuclear':'0700','Power Plants Electricity Production':'0600','Pump Consumption':'0800','Pump Storage':'1000','Renewable Energy Sources':'0100','Satbelization Load Percaentage':'0024','Solar Thermal Powers':'0300','Storage 2':'0011','Storage 3':'0018','Transports Heat 2':'2000','Turbine Production':'0900'}

xListM = ['','January','February','March','April','May','June','July','August','September','October','November','December']

class Window(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Connections()

#        global logFile
#        if os.path.exists(os.getcwd() + "/log.txt") == False:
#            logFile = open(os.getcwd() + "/log.txt", 'w+')
#        else:
#            logFile = open(os.getcwd() + "/log.txt", 'w')
#
#        self.txt_Log.setSource(QUrl('file:///' + os.getcwd().replace('\\','/') + "/log.txt"))

    def Connections(self):
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.openAboutDialog)
        self.btn_Page.clicked.connect(self.ChangePage)
        self.btn_ExePath.clicked.connect(self.SelectExePath)
        self.btn_IPF.clicked.connect(self.SelectIPF)
        self.btn_OPD.clicked.connect(self.SelectOPD)
        self.btn_Exec.clicked.connect(self.ProcessFile)
        self.btn_LoadStudy1.clicked.connect(self.loadStd1)

    def openAboutDialog(self):
        QMessageBox.about(self, 'About', 'Hi, I\'m developer')

    def ChangePage(self):
        if self.stackedWidget.currentIndex() == 0:
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.stackedWidget.setCurrentIndex(0)

    def SelectExePath(self):
        filePath = QFileDialog.getOpenFileName(self, 'Select EneryPLAN.exe file', filter='energyPLAN.exe')
        self.txt_ExePath.setText(filePath[0])

    def SelectIPF(self):
        filePath = QFileDialog.getOpenFileName(self, 'Select Input file', filter='*.txt')
        self.txt_IPF.setText(filePath[0])
    
    def SelectOPD(self):
        global path_OPD
        path_OPD = QFileDialog.getExistingDirectory(self, 'Select ouput directory', '', options=QFileDialog.Option.ShowDirsOnly)
        self.txt_OPD.setText(path_OPD)

    def ProcessFile(self):
        timeStamp = datetime.now().strftime('%y%m%d%H%M%S')

        if self.txt_ExePath.text() != '' and self.txt_IPF.text() != '' and self.txt_OPD.text() != '':
            path_OPD = self.txt_OPD.text()
            subprocess.run([self.txt_ExePath.text(), "-i", self.txt_IPF.text(), "-ascii", path_OPD + '/ops.txt'])
            prsStudy = csvParser(path_OPD + '/ops.txt', timeStamp)
            
            if self.cb_OpenOPD.isChecked():
                subprocess.run(['explorer', os.path.realpath(path_OPD)])

            if self.cb_LoadVis.isChecked():
                std1f = pd.read_csv(prsStudy, low_memory=False, index_col=0)
                std1n = std1f.loc['InputStudy','g0-Data1']
                std1n = std1n[:std1n.rfind('.')]
                self.lbl_Study1.setText('<span style=\" font-style:bold; color:#007f00;\">' + std1n + '</span>')
                self.readStd1()

        else:
            QMessageBox.critical(self, 'Error', 'Fuck')

    def loadStd1(self):
        filePath = QFileDialog.getOpenFileName(self, 'Select Study file', filter='*.csv')
        std1f = pd.read_csv(filePath[0], low_memory=False, index_col=0)
        std1n = std1f.loc['InputStudy','g0-Data1']
        std1n = std1n[:std1n.rfind('.')]
        self.lbl_Study1.setText('<span style=\" font-style:bold; color:#007f00;\">' + std1n + '</span>')
        self.readStd1(std1f)

    def readStd1(self, std1f: DataFrame):
        self.cb_Yseries1.clear()
        self.cb_Yseries1.addItems(yList.keys())
        self.cb_Xstart1.addItems(xListM)
        self.cb_Xend1.addItems(xListM)
        print(yList[self.cb_Yseries1.currentText()])
        self.cb_Yseries1.currentIndexChanged(self.openAboutDialog)



app = QApplication(sys.argv)
mainWindow = Window()
mainWindow.show()
sys.exit(app.exec())
