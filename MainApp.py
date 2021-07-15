import sys
import os
import subprocess
import pandas as pd
import plotly.express as pltx

from datetime import datetime
from PyQt6.QtCore import QFile, QUrl
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox)
from ui_main_window import Ui_MainWindow
from CSV_Parser import csvParser

yList = {'Added Export Payment':'0030','Boiler 1':'0005','Boiler 2':'0008','Boiler 3':'0015','Combined Heat & Power 2':'0006','Combined Heat & Power Electricity Production':'0023','Combined Heat and Power 3':'0013','Combined Steam & Heat Electricity Production':'0022','Combined Steam & Heat Production':'0400','Critical Electricity Excess Production':'0027','Desalination':'2200','District Cooling':'2100','District Heat Demand':'0004','Electricity Demand':'0001','Electricity Demand Cooling':'0002','Electricity Heat 2':'0009','Electricity Heat 3':'0016','Electrolyser 2':'0010','Electrolyser 3':'0017','Electrolyser Gr.2':'1100','Electrolyser Gr.3':'1200','EV & V2G (Transport)':'1300','Exorted Electricity':'0026','Exportable Electricity Excess Production':'0028','Exports Payment':'1600','Fixed Export / Import':'0003','Flexible Electricity demand':'0020','Gas Grid Demand & Balance':'2300','Geothermal Heat Production':'0500','Heat Balance Gr.2':'0012','Heat Balance Gr.3':'0019','Heat Pump 2':'0007','Heat Pump 3':'0014','Heat Pump Electricity Production':'0021','Hydrolic Powers':'0200','Import Payment':'0029','Imported Electricity':'0025','Individual Electricity':'1800','Individual Heat 1':'1700','Individual Heat 2':'1900','Market Prices':'1500','Nordpool Prices':'1400','Nuclear':'0700','Power Plants Electricity Production':'0600','Pump Consumption':'0800','Pump Storage':'1000','Renewable Energy Sources':'0100','Satbelization Load Percaentage':'0024','Solar Thermal Powers':'0300','Storage 2':'0011','Storage 3':'0018','Transports Heat 2':'2000','Turbine Production':'0900'}

xListM = ['January','February','March','April','May','June','July','August','September','October','November','December']

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
        self.rb_HV1.toggled.connect(self.setStd1HV)
        self.rb_MV1.toggled.connect(self.setStd1MV)
        self.btn_Plot1.clicked.connect(self.plotStd1)

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
            filePath = QFileDialog.getOpenFileName(self, 'Select Input file', filter='*.txt')
            self.txt_IPF.setText(filePath[0])
        except:
            pass
    
    def SelectOPD(self):
        global path_OPD
        try:
            path_OPD = QFileDialog.getExistingDirectory(self, 'Select ouput directory', '', options=QFileDialog.Option.ShowDirsOnly)
            self.txt_OPD.setText(path_OPD)
        except:
            pass

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
                self.readStd1(std1f)
                self.stackedWidget.setCurrentIndex(1)

        else:
            QMessageBox.critical(self, 'Error', 'Fuck')

    def loadStd1(self):
        try:
            filePath = QFileDialog.getOpenFileName(self, 'Select Study file', filter='*.csv')
            global std1f
            std1f = pd.read_csv(filePath[0], low_memory=False, index_col=0)
            std1n = std1f.loc['InputStudy','g0-Data1']
            std1n = std1n[:std1n.rfind('.')]
            self.lbl_Study1.setText('<span style=\" font-style:bold; color:#007f00;\">' + std1n + '</span>')
            self.btn_Plot1.setEnabled(True)
            if self.rb_MV1.isChecked():
                self.setStd1MV()
            elif self.rb_HV1.isChecked():
                self.setStd1HV()
            else:
                pass
        except:
            pass

    def setStd1MV(self):
        self.cb_Yseries1.addItems(yList.keys())
        self.cb_Xstart1.addItem(' ')
        self.cb_Xstart1.addItems(xListM)
        self.cb_Xend1.addItem(' ')
        self.cb_Xend1.addItems(xListM)
        self.cb_PlotType1.clear()
        self.cb_PlotType1.addItem('Bar Stacked')

    def setStd1HV(self):
        self.cb_Yseries1.addItems(yList.keys())
        self.cb_Xstart1.clear()
        self.cb_Xend1.clear()
        self.cb_PlotType1.clear()
        self.cb_PlotType1.addItem('Linear Stacked')

    def plotStd1(self):
        if self.rb_HV1.isChecked():

            if self.cb_Xstart1.currentText() == '':
                xSeriesSt = 'h1'
            else:
                xSeriesSt = 'h' + self.cb_Xstart1.currentText()

            if self.cb_Xend1.currentText() == '':
                xSeriesEn = 'h1'
            else:
                xSeriesEn = 'h' + self.cb_Xend1.currentText()
                
            xSeries = list(std1f.index.values)
            xSeries = xSeries[xSeries.index(xSeriesSt):xSeries.index(xSeriesEn)+1]

        if self.rb_MV1.isChecked():

            if self.cb_Xstart1.currentText() == ' ':
                xSeriesSt = xListM.index(xListM[0])
            else:
                xSeriesSt = xListM.index(self.cb_Xstart1.currentText())

            if self.cb_Xend1.currentText() == ' ':
                xSeriesEn = xListM.index(xListM[-1])
            else:
                xSeriesEn = xListM.index(self.cb_Xend1.currentText()) +1

            xSeries = xListM[xSeriesSt:xSeriesEn]

        try:
            yStructure = yList.get(self.cb_Yseries1.currentText())
            ySeries = []
            ySeries.clear()
            
            if yStructure[:2] == '00':
                for column in std1f:
                    colMatch = str(column)
                    if yStructure == colMatch[:colMatch.find('_')]:
                        ySeries.append(colMatch)

            elif yStructure[:2] != '00':
                for column in std1f:
                    colMatch = str(column)
                    if yStructure[:2] == colMatch[:2]:
                        ySeries.append(colMatch)
            
        except:
            pass
        finally:
            timeStamp = datetime.now().strftime('%y%m%d%H%M%S')
            std1fnew = std1f.loc[xSeries,ySeries]
            pd.options.plotting.backend = "plotly"

            if self.rb_MV1.isChecked():
                #figStd1 = pltx.bar(std1fnew,y=[ySeries], width=1366, height=768, labels={ySeries:self.cb_Yseries1.currentText()})
                #figStd1.update_layout(title=self.cb_Yseries1.currentText(),xaxis_title= 'Month')
                figStd1 = std1fnew.plot(kind='bar')
                figStd1.update_layout(title=self.cb_Yseries1.currentText(), xaxis_title= 'Month', width=1366, height=768)


            elif self.rb_HV1.isChecked():
                #figStd1 = pltx.line(std1fnew, width=1366, height=768, labels={ySeries:self.cb_Yseries1.currentText()})
                #figStd1.update_layout(title=self.cb_Yseries1.currentText(),xaxis_title= 'Hours')
                figStd1 = std1fnew.plot(kind='line')
                figStd1.update_layout(title=self.cb_Yseries1.currentText(), xaxis_title= 'Hours', width=1366, height=768)

            figStd1.write_image(os.getcwd() + '/plot_' + timeStamp + '.jpeg', scale=3, engine='kaleido')


app = QApplication(sys.argv)
mainWindow = Window()
mainWindow.show()
sys.exit(app.exec())
