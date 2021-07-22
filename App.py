import sys
import os
import subprocess
import pandas as pd

from datetime import datetime
from PyQt6 import QtCore
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox)
from CSV_Parser import csvParser
from ui_main import Ui_MainWindow

xSeriesData = ySeries = {'Added Export Payment':'0030','Boiler 1':'0005','Boiler 2':'0008','Boiler 3':'0015','Combined Heat & Power 2':'0006','Combined Heat & Power Electricity Production':'0023','Combined Heat and Power 3':'0013','Combined Steam & Heat Electricity Production':'0022','Combined Steam & Heat Production':'0400','Critical Electricity Excess Production':'0027','Desalination':'2200','District Cooling':'2100','District Heat Demand':'0004','Electricity Demand':'0001','Electricity Demand Cooling':'0002','Electricity Heat 2':'0009','Electricity Heat 3':'0016','Electrolyser 2':'0010','Electrolyser 3':'0017','Electrolyser Gr.2':'1100','Electrolyser Gr.3':'1200','EV & V2G (Transport)':'1300','Exorted Electricity':'0026','Exportable Electricity Excess Production':'0028','Exports Payment':'1600','Fixed Export / Import':'0003','Flexible Electricity demand':'0020','Gas Grid Demand & Balance':'2300','Geothermal Heat Production':'0500','Heat Balance Gr.2':'0012','Heat Balance Gr.3':'0019','Heat Pump 2':'0007','Heat Pump 3':'0014','Heat Pump Electricity Production':'0021','Hydrolic Powers':'0200','Import Payment':'0029','Imported Electricity':'0025','Individual Electricity':'1800','Individual Heat 1':'1700','Individual Heat 2':'1900','Market Prices':'1500','Nordpool Prices':'1400','Nuclear':'0700','Power Plants Electricity Production':'0600','Pump Consumption':'0800','Pump Storage':'1000','Renewable Energy Sources':'0100','Satbelization Load Percaentage':'0024','Solar Thermal Powers':'0300','Storage 2':'0011','Storage 3':'0018','Transports Heat 2':'2000','Turbine Production':'0900'}

xSeriesMonth = ['January','February','March','April','May','June','July','August','September','October','November','December']
figList = pltList = stdList = []
figInt = pltInt = stdInt = 1

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
        self.btn_StdLoad.clicked.connect(self.AddStudy)
        self.btn_StdRemove.clicked.connect(self.RemoveStudy)

    def openAboutDialog(self):
        QMessageBox.about(self, 'About', 'Hi, I\'m developer')

    def ChangePage(self):
        if self.stackedWidget.currentIndex() == 0:
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.stackedWidget.setCurrentIndex(0)

    def SelectExePath(self):
        try:
            filePath = QFileDialog.getOpenFileName(self, 'Select EneryPLAN.exe file', filter='energyPLAN.exe')
            self.txt_ExePath.setText(filePath[0])
        except:
            pass

    def SelectIPF(self):
        try:
            filePath = QFileDialog.getOpenFileName(self, 'Select Input file', filter= '*.txt')
            self.txt_IPF.setText(filePath[0])
        except:
            pass
    
    def SelectOPD(self):
        global path_OPD
        try:
            path_OPD = QFileDialog.getExistingDirectory(self, 'Select ouput directory', '', options= QFileDialog.Option.ShowDirsOnly)
            self.txt_OPD.setText(path_OPD)
        except:
            pass

    def ProcessFile(self):
        timeStamp = datetime.now().strftime('%y%m%d%H%M%S')

        if self.txt_ExePath.text() != '' and self.txt_IPF.text() != '' and self.txt_OPD.text() != '':
            path_OPD = self.txt_OPD.text()
            subprocess.run([self.txt_ExePath.text(), "-i", self.txt_IPF.text(), "-ascii", path_OPD + '/ops.txt'])
            stdParsed = csvParser(path_OPD + '/ops.txt', timeStamp)
            
            if self.cb_OpenOPD.isChecked():
                subprocess.run(['explorer', os.path.realpath(path_OPD)])

            if self.cb_LoadVis.isChecked():
                global stdInt

                stdName = stdParsed
                stdName = stdName[stdName.rfind('/') +1:stdName.rfind('.')]
                stdID = {'id': 'std' + str(stdInt), 'name': stdName, 'path': stdParsed}
                stdInt += 1
                stdList.append(stdID)
                self.lw_StdList.addItem(stdName)
                print(stdList)

        else:
            QMessageBox.critical(self, 'Error', 'Error')

    def AddStudy(self):
        global stdInt

        filePath = QFileDialog.getOpenFileName(self, 'Select Input file', filter='*.csv')
        stdName = filePath[0]
        stdName = stdName[stdName.rfind('/') +1:stdName.rfind('.')]
        
        if len(self.lw_StdList.findItems(stdName, QtCore.Qt.MatchFlag.MatchExactly)) > 0:
            stdName = stdName + '_' + str(stdInt)

        stdID = {'id': 'std' + str(stdInt), 'name': stdName, 'path': filePath[0]}
        stdInt += 1
        stdList.append(stdID)
        self.lw_StdList.addItem(stdName)

    def RemoveStudy(self):
        removeIndex = self.lw_StdList.currentRow()
        if self.lw_StdList.currentItem() is not None:
            removeName = self.lw_StdList.currentItem().text()

        self.lw_StdList.takeItem(removeIndex)

        for i in range(0, len(stdList)):
            if stdList[i]['name'] == removeName:
                del stdList[i]
                break
            else:
                next



app = QApplication(sys.argv)
mainWindow = Window()
mainWindow.show()
sys.exit(app.exec())