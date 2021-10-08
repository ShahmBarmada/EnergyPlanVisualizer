import sys
import os
import subprocess
import re

from datetime import datetime
from PyQt6 import QtCore
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox, QLabel)
from PyQt6.QtGui import (QPixmap, QScreen)
from CSV_Parser import csvParser
from Plotter import (PlotterSelective, PlotterCollective)
from UI_Main import Ui_MainWindow

dataList = {'Renewable Energy Sources [g]':'0100','Hydrolic Powers [g]':'0200','Solar Thermal Powers [g]':'0300','Combined Steam & Heat Production [g]':'0400','Geothermal Heat Production [g]':'0500','Power Plants Electricity Production [g]':'0600','Nuclear [g]':'0700','Pump Consumption [g]':'0800','Turbine Production [g]':'0900','Pump Storage [g]':'1000','Electrolyser Gr.2 [g]':'1100','Electrolyser Gr.3 [g]':'1200','EV & V2G (Transport) [g]':'1300','Nordpool Prices [g]':'1400','Market Prices [g]':'1500','Exports Payment [g]':'1600','Individual Heat 1 [g]':'1700','Individual Electricity [g]':'1800','Individual Heat 2 [g]':'1900','Transports Heat 2 [g]':'2000','District Cooling [g]':'2100','Desalination [g]':'2200','Gas Grid Demand & Balance [g]':'2300','Electr. Demand':'0001','Elec.dem Cooling':'0002','Fixed Exp/Imp':'0003','DH Demand':'0004','Wind Electr.':'0101','Offshore Electr.':'0102','PV Electr.':'0103','CSP Electr.':'0104','River Electr.':'0105','Wave Electr.':'0106','Tidal Electr.':'0107','CSP2 Electr.':'0108','CSP2 Storage':'0109','CSP2 loss':'0110','Hydro Electr.':'0201','Hydro pump':'0202','Hydro storage':'0203','Hydro Wat-Sup':'0204','Hydro Wat-Loss':'0205','Solar Heat':'0301','CSHP 1 Heat':'0401','Waste 1 Heat':'0402','Boiler 1 Heat':'0005','Solar 1 Heat':'0302','Sol1 Str Heat':'0303','CSHP 2 Heat':'0403','Waste 2 Heat':'0404','Geoth 2 Heat':'0501','Geoth 2 Steam':'0502','Geoth 2 Storage':'0503','CHP 2 Heat':'0006','HP 2 Heat':'0007','Boiler 2 Heat':'0008','EH 2 Heat':'0009','ELT 2 Heat':'0010','Solar2 Heat':'0304','Sol2 Str Heat':'0305','Storage2 Heat':'0011','Balance2 Heat':'0012','CSHP 3 Heat':'0405','Waste 3 Heat':'0406','Geoth 3 Heat':'0504','Geoth 3 Steam':'0505','Geoth 3 Storage':'0506','CHP 3 Heat':'0013','HP 3 Heat':'0014','Boiler 3 Heat':'0015','EH 3 Heat':'0016','ELT 3 Heat':'0017','Solar3 Heat':'0306','Sol3 Str Heat':'0307','Storage3 Heat':'0018','Balance3 Heat':'0019','Flexible Electr.':'0020','HP Electr.':'0021','CSHP Electr.':'0022','CHP Electr.':'0023','PP Electr.':'0601','PP2 Electr.':'0602','Nuclear Electr.':'0701','Geother. Electr.':'0702','Pump Electr.':'0801','Turbine Electr.':'0901','Pumped Storage':'1001','Pump2 Electr.':'0802','Turbine2 Electr.':'0902','Pumped2 Storage':'1002','Rock in Electr.':'0903','Rock out Steam':'0904','Rock str Storage':'0905','ELT 2 Electr.':'1101','ELT 2 H2 ELT 2':'1102','ELT 3 Electr.':'1201','ELT 3 H2 ELT 3':'1202','V2G Demand':'1301','V2G Charge':'1302','V2G Discha.':'1303','V2G Storage':'1304','H2 Electr.':'2001','H2 Storage':'2002','CO2Hydro Electr.':'2003','NH3Hydro Electr.':'2004','CO2Hydro liq.fuel':'2005','NH3Hydro Ammonia':'2006','HH-CHP Electr.':'1801','HH-HP Electr.':'1802','HH-HP/EB Electr.':'1803','HH-EB Electr.':'1804','HH-H2 Electr.':'1901','HH-H2 Storage':'1902','HH-H2 Prices':'1903','HH Dem. Heat':'1701','HH CHP+HP Heat':'1702','HH Boil. Heat':'1703','HH Solar Heat':'1704','HH Store Heat':'1705','HH Balan Heat':'1706','Stabil. LoadPercent':'0024','Import Electr.':'0025','Export Electr.':'0026','CEEP Electr.':'0027','EEEP Electr.':'0028','ExMarket Prices':'1401','ExMarket Prod':'1402','System Prices':'1501','InMarket Prices':'1502','Btl-neck Prices':'1503','Import Payment':'0029','Export Payment':'1601','Blt-neck Payment':'1602','Add-exp Payment':'0030','Boilers ':'2301','CHP2+3 ':'2302','PP CAES':'2303','Indi- vidual':'2304','Transp. ':'2305','Indust. Various':'2306','Demand Sum':'2307','Biogas ':'2308','Syngas ':'2309','CO2HyGas ':'2310','SynHyGas ':'2311','SynFuel ':'2312','Storage ':'2313','Storage Content':'2314','Sum ':'2315','Import Gas':'2316','Export Gas':'2317','FreshW Demand':'2201','FreshW Storage':'2202','SaltW Demand':'2203','Brine Prod.':'2204','Brine Storage':'2205','Desal.Pl Electr.':'2206','FWPump Electr.':'2207','Turbine Electr.':'2208','Pump Electr.':'2209','CoolGr1 Demand':'2101','CoolGr2 Demand':'2102','CoolGr3 Demand':'2103','Cool-El Demand':'2104','CoolGr1 Natural':'2105','CoolGr2 Natural':'2106','CoolGr3 Natural':'2107','Cooling DHgr1':'2108','Cooling DHgr2':'2109','Cooling DHgr3':'2110','Cooling Electr.':'2111'}

monthList = ['January','February','March','April','May','June','July','August','September','October','November','December']
figList, pltList, stdList = [], [], []
figID, pltID, stdID = 1, 1, 1

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.InitialData()
        self.SwitchHandelers()
        self.Connections()

    def InitialData(self):
        self.cb_FileFormat.addItems(['image','html','json']) 
        self.cb_FileFormat.setCurrentIndex(0)
        self.SelectiveAnalysis()

    def SwitchHandelers(self):
        self.rb_Selective.toggled.connect(self.SelectiveAnalysis)
        self.rb_Collective.toggled.connect(self.CollectiveAnalysis)
        self.rb_HourlyVal.toggled.connect(self.UpdateDataType)
        self.rb_MonthlyVal.toggled.connect(self.UpdateDataType)
        self.rb_AnnualVal.toggled.connect(self.UpdateDataType)
        self.cb_Trace.currentIndexChanged.connect(self.UpdateTrace)
        self.lw_FigList.currentRowChanged.connect(self.UpdateFigSlct)
        self.lw_PltList.currentRowChanged.connect(self.UpdatePltSlct)
        self.lw_StdList.currentRowChanged.connect(self.UpdateStdSlct)
        self.cb_TicksX.stateChanged.connect(self.UpdateTickStateX)
        self.cb_TicksY.stateChanged.connect(self.UpdateTickStateY)

    def SelectiveAnalysis(self):
        self.rb_HourlyVal.setEnabled(True)
        self.rb_MonthlyVal.setEnabled(True)
        self.rb_AnnualVal.setEnabled(True)
        self.cb_StatMean.setEnabled(True)
        self.cb_StatMedian.setEnabled(True)
        self.rb_HourlyVal.setChecked(True)
        self.UpdateDataType()

    def CollectiveAnalysis(self):
        self.rb_HourlyVal.setEnabled(False)
        self.rb_MonthlyVal.setEnabled(False)
        self.rb_AnnualVal.setEnabled(True)
        self.cb_StatMean.setEnabled(False)
        self.cb_StatMedian.setEnabled(False)
        self.rb_AnnualVal.setChecked(True)
        self.UpdateDataType()

    def UpdateDataType(self):
        if self.rb_HourlyVal.isEnabled and self.rb_HourlyVal.isChecked():
            self.cb_Trace.clear()
            self.cb_Trace.addItems(['Scatter Plot'])
            self.cb_Trace.setCurrentIndex(0)
            self.rb_Xtime.setEnabled(True)
            self.rb_Xtime.setChecked(True)
            self.cb_Xstart.setEnabled(True)
            self.cb_Xstart.clear()
            self.cb_Xend.setEnabled(True)
            self.cb_Xend.clear()
            self.cb_Ydata.clear()
            self.cb_Ydata.setEnabled(True)
            self.cb_Ydata.addItems(dataList.keys())
            self.cb_Ydata.insertSeparator(23)
            self.cb_Xdata.clear()
            self.cb_Xdata.addItems(dataList.keys())
            self.cb_Xdata.insertSeparator(23)
            
        if self.rb_MonthlyVal.isEnabled and self.rb_MonthlyVal.isChecked():
            self.cb_Trace.clear()
            self.cb_Trace.addItems(['Scatter Plot', 'Bar Chart'])
            self.cb_Trace.setCurrentIndex(0)
            self.rb_Xtime.setEnabled(True)
            self.rb_Xtime.setChecked(True)
            self.cb_Xstart.setEnabled(True)
            self.cb_Xstart.clear()
            self.cb_Xstart.addItems(monthList)
            self.cb_Xstart.setCurrentIndex(0)
            self.cb_Xend.setEnabled(True)
            self.cb_Xend.clear()
            self.cb_Xend.addItems(monthList)
            self.cb_Xend.setCurrentIndex(11)
            self.cb_Ydata.clear()
            self.cb_Ydata.setEnabled(True)
            self.cb_Ydata.addItems(dataList.keys())
            self.cb_Ydata.insertSeparator(23)
            self.cb_Xdata.clear()
            self.cb_Xdata.addItems(dataList.keys())
            self.cb_Xdata.insertSeparator(23)
            
        if self.rb_AnnualVal.isEnabled and self.rb_AnnualVal.isChecked():
            if self.rb_Selective.isChecked():
                self.cb_Trace.clear()
                self.cb_Trace.addItems(['Bar Chart', 'Pie Chart', 'Box Plot'])
                self.cb_Trace.setCurrentIndex(0)
                self.rb_Xdata.setChecked(True)
                self.rb_Xtime.setEnabled(False)
                self.cb_Xstart.setEnabled(False)
                self.cb_Xend.setEnabled(False)
                self.cb_Ydata.clear()
                self.cb_Ydata.setEnabled(True)
                self.cb_Ydata.addItems(dataList.keys())
                self.cb_Ydata.insertSeparator(23)
                self.cb_Xdata.clear()

            if self.rb_Collective.isChecked():
                self.cb_Trace.clear()
                self.cb_Trace.addItems(['Box Plot'])
                self.cb_Trace.setCurrentIndex(0)
                self.rb_Xdata.setChecked(True)
                self.rb_Xtime.setEnabled(False)
                self.cb_Xstart.setEnabled(False)
                self.cb_Xend.setEnabled(False)
                self.sb_Col.setEnabled(False)
                self.sb_Row.setEnabled(False)
                self.cb_Ydata.clear()
                self.cb_Ydata.setEnabled(False)
                self.cb_Xdata.clear()

        self.UpdateTrace()

    def UpdateTrace(self):
        if self.cb_Trace.currentText() == 'Scatter Plot':
            self.cb_Style.clear()
            self.cb_Style.addItems(['Lines + Markers', 'Lines Only', 'Markers Only', 'Smooth Linear'])
            self.cb_Style.setCurrentIndex(0)
            self.cb_FillArea.setEnabled(True)
            self.cb_TicksX.setEnabled(True)
            self.cb_TicksY.setEnabled(True)

        elif self.cb_Trace.currentText() == 'Bar Chart':
            self.cb_Style.clear()
            self.cb_Style.addItems(['Stacked', 'Grouped'])
            self.cb_Style.setCurrentIndex(0)
            self.cb_FillArea.setEnabled(False)
            self.cb_TicksX.setEnabled(False)
            self.cb_TicksY.setEnabled(False)
            if self.rb_AnnualVal.isChecked():
                self.cb_Xdata.clear()
                self.cb_Xdata.addItems(['Energy Balance', 'Power Values - Totals','Power Values - Annual Average','Power Values - Annual Maximum','Power Values - Annual Minimum', 'Investment Costs - Total', 'Investment Costs - Annual', 'Investment Costs - O & M', 'Total Elect. Demand', 'Total Heat Demand'])

        elif self.cb_Trace.currentText() == 'Pie Chart':
            self.cb_Style.clear()
            self.cb_Style.addItems(['Domain', 'Domain Spaced'])
            self.cb_Style.setCurrentIndex(0)
            self.cb_FillArea.setEnabled(False)
            self.cb_TicksX.setEnabled(False)
            self.cb_TicksY.setEnabled(False)
            if self.rb_AnnualVal.isChecked():
                self.cb_Xdata.clear()
                self.cb_Xdata.addItems(['Annual CO2 Emissions','Annual Fuel Consumptions','Share of RES', 'Total Elect. Demand', 'Total Heat Demand'])

        elif self.cb_Trace.currentText() == 'Box Plot':
            self.cb_Style.clear()
            self.cb_Style.addItems(['Whiskers', 'OutLiers', 'Whiskers & Points', 'Whiskers & OutLiers'])
            self.cb_Style.setCurrentIndex(0)
            self.cb_FillArea.setEnabled(False)
            self.cb_TicksX.setEnabled(False)
            self.cb_TicksY.setEnabled(False)
            if self.rb_AnnualVal.isChecked():
                self.cb_Xdata.clear()
                self.cb_Xdata.addItems(['Energy Balance (per Index)', 'Installed Capacities (per Index)', 'Total Elect. Demand', 'Total Heat Demand'])

    def UpdateTickStateX(self):
        if self.cb_TicksX.isChecked():
            self.txt_TicksX.setEnabled(False)
        else:
            self.txt_TicksX.setEnabled(True)

    def UpdateTickStateY(self):
        if self.cb_TicksY.isChecked():
            self.txt_TicksY.setEnabled(False)
        else:
            self.txt_TicksY.setEnabled(True)

    def UpdateFigSlct(self):
        if self.lw_FigList.currentRow() == -1:
            self.lbl_SlctFig.setText('none')
            self.lbl_SlctFig.setStyleSheet('border-bottom-width: 1px; border-bottom-style: solid; border-radius: 0px; color: red;')
        else:
            self.lbl_SlctFig.setText(self.lw_FigList.currentItem().text())
            self.lbl_SlctFig.setStyleSheet('border-bottom-width: 1px; border-bottom-style: solid; border-radius: 0px; color: green;')

    def UpdatePltSlct(self):
        if self.lw_PltList.currentRow() == -1:
            self.lbl_SlctPlt.setText('none')
            self.lbl_SlctPlt.setStyleSheet('border-bottom-width: 1px; border-bottom-style: solid; border-radius: 0px; color: red;')
        else:
            self.lbl_SlctPlt.setText(self.lw_PltList.currentItem().text())
            self.lbl_SlctPlt.setStyleSheet('border-bottom-width: 1px; border-bottom-style: solid; border-radius: 0px; color: green;')

    def UpdateStdSlct(self):
        if self.lw_StdList.currentRow() == -1:
            self.lbl_SlctStd.setText('none')
            self.lbl_SlctStd.setStyleSheet('border-bottom-width: 1px; border-bottom-style: solid; border-radius: 0px; color: red;')
        else:
            self.lbl_SlctStd.setText(self.lw_StdList.currentItem().text())
            self.lbl_SlctStd.setStyleSheet('border-bottom-width: 1px; border-bottom-style: solid; border-radius: 0px; color: green;')

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
        self.btn_FigAdd.clicked.connect(self.AddFigure)
        self.btn_FigDlt.clicked.connect(self.RemoveFigure)
        self.btn_PltNew.clicked.connect(self.AddPlot)
        self.btn_PltDlt.clicked.connect(self.RemovePlot)
        self.btn_FigSave.clicked.connect(self.SaveFigure)
        self.btn_FigView.clicked.connect(self.PreviewFigure)

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
        global stdID
        timeStamp = datetime.now().strftime('%y%m%d%H%M%S')

        if self.txt_ExePath.text() != '' and self.txt_IPF.text() != '' and self.txt_OPD.text() != '':
            path_OPD = self.txt_OPD.text()
            subprocess.run([self.txt_ExePath.text(), "-i", self.txt_IPF.text(), "-ascii", path_OPD + '/ops.txt'])
            stdParsed = csvParser(self.txt_IPF.text(), path_OPD + '/ops.txt', timeStamp)
            
            if self.cb_OpenOPD.isChecked():
                subprocess.run(['explorer', os.path.realpath(path_OPD)])

            if self.cb_LoadVis.isChecked():
                stdName = stdParsed
                stdName = stdName[stdName.rfind('/') +1:stdName.rfind('.')]
                stdCard = {
                    'id': 'std' + str(stdID).zfill(2),
                    'name': stdName,
                    'path': stdParsed}
                stdID += 1
                stdList.append(stdCard)
                self.lw_StdList.addItem(stdName)

        else:
            QMessageBox.critical(self, 'Error', 'Error')

    def AddStudy(self):
        global stdID
        numbering = 1

        filePath = QFileDialog.getOpenFileName(self, 'Select Input file', filter='*.csv')
        stdName = filePath[0]
        stdName = stdName[stdName.rfind('/') +1:stdName.rfind('.')]
        
        while len(self.lw_StdList.findItems(stdName, QtCore.Qt.MatchFlag.MatchExactly)) > 0:
            if re.fullmatch(r'_\d{2}', stdName[-3:]) is not None:
                stdName = stdName[:-3] + '_' + str(numbering).zfill(2)
            else:
                stdName = stdName + '_' + str(numbering).zfill(2)
            numbering += 1

        stdCard = {
            'id': 'std' + str(stdID).zfill(2),
            'name': stdName,
            'path': filePath[0]}

        stdID += 1
        stdList.append(stdCard)
        self.lw_StdList.addItem(stdName)
        self.lw_StdList.setCurrentRow(self.lw_StdList.count() -1)
        self.lw_StdList.sortItems()

    def RemoveStudy(self):
        removeIndex = self.lw_StdList.currentRow()

        if self.lw_StdList.currentItem() is not None:
            removeName = self.lw_StdList.currentItem().text()

        self.lw_StdList.takeItem(removeIndex)

        for i in range(len(stdList)):

            if stdList[i]['name'] == removeName:
                del stdList[i]
                break
            else:
                next

    def AddFigure(self):
        global figID
        numbering = 1

        figName = re.sub(r'\s+', r' ', self.txt_FigName.text().strip())

        if re.fullmatch(r'(?=.)[\w[|]\s][^<>:"/|?*\\]', figName) is None:

            if re.match(r'\w|\w+', figName):

                while len(self.lw_FigList.findItems(figName, QtCore.Qt.MatchFlag.MatchExactly)) > 0:
                    if re.fullmatch(r'_\d{2}', figName[-3:]) is not None:
                        figName = figName[:-3] + '_' + str(numbering).zfill(2)
                    else:
                        figName = figName + '_' + str(numbering).zfill(2)
                    numbering += 1

                if int(self.txt_FigHeight.text()) != 0 and int(self.txt_FigWidth.text()) != 0:
                    figCard = {
                        'id': 'fig' + str(figID).zfill(2),
                        'name': figName,
                        'width': int(self.txt_FigWidth.text()),
                        'height': int(self.txt_FigHeight.text()),
                        'rows': int(self.sb_FigRows.text()),
                        'cols': int(self.sb_FigCols.text()),
                        'font': int(self.sb_FontSize.text()),
                        'legend': self.cb_Legend.isChecked()}
                    figID += 1
                    figList.append(figCard)
                    self.lw_FigList.addItem(figName)
                    self.lw_FigList.setCurrentRow(self.lw_FigList.count() -1)
                    self.lw_FigList.sortItems()

            else:
                print('error 1')
                pass
        else:
            print('error 2')
            pass

    def RemoveFigure(self):
        removeIndex = self.lw_FigList.currentRow()

        if self.lw_FigList.currentItem() is not None:
            removeName = self.lw_FigList.currentItem().text()

        self.lw_FigList.takeItem(removeIndex)

        for i in range(len(figList)):

            if figList[i]['name'] == removeName:
                del figList[i]
                break
            else:
                next

    def AddPlot(self):
        global pltID
        numbering = 1

        if self.lw_StdList.currentRow() == -1:
            pass

        else:
            dataSrc = self.lw_StdList.currentItem().text()
            for i in range(len(stdList)):
                if stdList[i]['name'] == self.lw_StdList.currentItem().text():
                    dataSrc = stdList[i]

        if self.lw_FigList.currentRow() == -1:
            pass

        else:
            pltSrcName = self.lw_FigList.currentItem().text()

            for i in range(len(figList)):
                if figList[i]['name'] == pltSrcName:
                    pltSrcID = figList[i]['id']

            pltName = 'Fig(' + pltSrcName + ')_' + str(numbering).zfill(2)

            while len(self.lw_PltList.findItems(pltName, QtCore.Qt.MatchFlag.MatchExactly)) > 0:
                numbering += 1
                pltName = 'Fig(' + pltSrcName + ')_' + str(numbering).zfill(2)

            if self.rb_HourlyVal.isChecked():
                pltType = 'hourly'
                if self.rb_Xtime.isChecked():
                    xType = 'time'
                elif self.rb_Xdata.isChecked():
                    xType = 'data'
                for i, key in enumerate(dataList.keys()):
                    if key == self.cb_Xdata.currentText():
                        xData = dataList[key]
                        xTitle = key
                        next
                    if key == self.cb_Ydata.currentText():
                        yData = dataList[key]
                        yTitle = key
                        next

            elif self.rb_MonthlyVal.isChecked():
                pltType = 'monthly'
                if self.rb_Xtime.isChecked():
                    xType = 'time'
                elif self.rb_Xdata.isChecked():
                    xType = 'data'
                for i, key in enumerate(dataList.keys()):
                    if key == self.cb_Xdata.currentText():
                        xData = dataList[key]
                        xTitle = key
                        next
                    if key == self.cb_Ydata.currentText():
                        yData = dataList[key]
                        yTitle = key
                        next

            elif self.rb_AnnualVal.isChecked():
                pltType = 'annual'
                xType = 'data'
                xData = self.cb_Xdata.currentText()
                xTitle = 'Annual Values'
                for i, key in enumerate(dataList.keys()):
                    if key == self.cb_Ydata.currentText():
                        yData = dataList[key]
                        yTitle = key
                        next

            traceType = self.cb_Trace.currentText()
            traceStyle = self.cb_Style.currentText()

            if self.cb_FillArea.isEnabled():
                if self.cb_FillArea.isChecked():
                    traceFill = True
                else:
                    traceFill = False
            else:
                traceFill = False

            if self.cb_TicksX.isChecked():
                xTick = 'auto'
                xStep = 0
            else:
                xTick = 'fixed'
                xStep = int(self.txt_TicksX.text()) -1

            if self.cb_TicksY.isChecked():
                yTick = 'auto'
                yStep = 0
            else:
                yTick = 'fixed'
                yStep = int(self.txt_TicksX.text()) -1

            posR = int(self.sb_Row.text())
            posC = int(self.sb_Col.text())
            spanR = int(self.sb_RowSpan.text())
            spanC = int(self.sb_ColSpan.text())

            xTimeStart = self.cb_Xstart.currentText()
            xTimeEnd = self.cb_Xend.currentText()

            pltCard = {
                'id': 'plt' + str(pltID).zfill(2),
                'name': pltName,
                'figid': pltSrcID,
                'figname': pltSrcName,
                'datasrc': dataSrc,
                'datatype': pltType,
                'tracetype': traceType,
                'tracestyle': traceStyle,
                'tracefill': traceFill,
                'row': posR,
                'rowspan': spanR,
                'col': posC,
                'colspan': spanC,
                'xstart': xTimeStart,
                'xend': xTimeEnd,
                'xdata': xData,
                'xtitle': xTitle,
                'xtype': xType,
                'xtick': xTick,
                'xstep': xStep,
                'ydata': yData,
                'ytitle': yTitle,
                'ytick': yTick,
                'ystep': yStep}

            pltID += 1
            pltList.append(pltCard)
            self.lw_PltList.addItem(pltName)
            self.lw_PltList.setCurrentRow(self.lw_PltList.count() -1)
            self.lw_PltList.sortItems()

    def RemovePlot(self):
        removeIndex = self.lw_PltList.currentRow()

        if self.lw_PltList.currentItem() is not None:
            removeName = self.lw_PltList.currentItem().text()

        self.lw_PltList.takeItem(removeIndex)

        for i in range(len(pltList)):
            if pltList[i]['name'] == removeName:
                del pltList[i]
                break
            else:
                next

    def PrepareFigure(self):

        global figure

        if self.rb_Selective.isChecked():
            # get selected figure card
            slctFig = self.lbl_SlctFig.text()

            for i in range(len(figList)):
                if figList[i]['name'] == slctFig:
                    slctFig = figList[i]
                    slctFigID = figList[i]['id']
                    break
                else:
                    next

            # generate sub-plots list of cards
            slctPlt = []

            for i in range(len(pltList)):
                if pltList[i]['figid'] == slctFigID:
                    slctPlt.append(pltList[i])
                    next
                else:
                    next

            # process figure in plotter
            figure = PlotterSelective(slctFig, slctPlt)

        if self.rb_Collective.isChecked():
            # get selected figure card
            slctFig = self.lbl_SlctFig.text()

            for i in range(len(figList)):
                if figList[i]['name'] == slctFig:
                    slctFig = figList[i]
                    break
                else:
                    next

            # get studies list:
            slctStd = []
            for i in range(len(stdList)):
                slctStd.append(stdList[i])

            # get X data series:
            xData = self.cb_Xdata.currentText()

            traceStyle = self.cb_Style.currentText()

            # process figure in plotter
            figure = PlotterCollective(slctFig, slctStd, xData, traceStyle)

    def SaveFigure(self):
        try:
            self.PrepareFigure()

            if self.cb_FileFormat.currentText() == 'image':
                savePath = QFileDialog.getSaveFileName(self, 'Save File', filter='*.png;;*.jpg;;*.svg')
                figure.write_image(file= savePath[0], scale= 3, engine= 'kaleido')
            elif self.cb_FileFormat.currentText() == 'html':
                savePath = QFileDialog.getSaveFileName(self, 'Save File', filter='*.html')
                figure.write_html(file= savePath[0])
            elif self.cb_FileFormat.currentText() == 'json':
                savePath = QFileDialog.getSaveFileName(self, 'Save File', filter='*.json')
                figure.write_json(file= savePath[0], engine= 'json')

        except:
            pass
    
    def PreviewFigure(self):
        self.PrepareFigure()

        try:
            figure.write_image(file= './preview.jpg', scale= 1)
            self.PreviewWindowDialog = PreviewWindow(self)
            self.PreviewWindowDialog.show()

        except:
            pass

class PreviewWindow(QMainWindow):
    def __init__(self, parent= None):
        super(PreviewWindow, self).__init__(parent)

        self.setWindowTitle('Figure Preview')
        self.resize(100,100)

        imageHolder = QPixmap('./preview.jpg')

        if imageHolder.width() > int(QScreen.availableGeometry(QApplication.primaryScreen()).width() * 0.95):
            imageWidth = int(QScreen.availableGeometry(QApplication.primaryScreen()).width() / 1.2)
            imageHeight = int(imageHolder.height() * (imageWidth / imageHolder.width()))

        elif imageHolder.height() > int(QScreen.availableGeometry(QApplication.primaryScreen()).height() * 0.95):
            imageHeight = int(QScreen.availableGeometry(QApplication.primaryScreen()).height() / 1.2)
            imageWidth = int(imageHolder.width() * (imageHeight / imageHolder.height()))

        else:
            imageWidth = imageHolder.width()
            imageHeight = imageHolder.height()

        self.setMinimumSize(imageWidth, imageHeight)
        self.setMaximumSize(imageWidth, imageHeight)

        self.imageLable = QLabel()
        self.imageLable.setPixmap(imageHolder)
        self.imageLable.setScaledContents(True)
        self.setCentralWidget(self.imageLable)
        os.remove('./preview.jpg')


app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
sys.exit(app.exec())