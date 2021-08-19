import sys
import os
import subprocess
import re

from datetime import datetime
from PyQt6 import QtCore
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox)
from CSV_Parser import csvParser
from Plotter import plotter
from ui_main import Ui_MainWindow

dataList = {'Electricity Demand':'0001','Electricity Demand Cooling':'0002','Fixed Export / Import':'0003','District Heat Demand':'0004','Boiler 1':'0005','Combined Heat & Power 2':'0006','Heat Pump 2':'0007','Boiler 2':'0008','Electricity Heat 2':'0009','Electrolyser 2':'0010','Storage 2':'0011','Heat Balance Gr.2':'0012','Combined Heat and Power 3':'0013','Heat Pump 3':'0014','Boiler 3':'0015','Electricity Heat 3':'0016','Electrolyser 3':'0017','Storage 3':'0018','Heat Balance Gr.3':'0019','Flexible Electricity demand':'0020','Heat Pump Electricity Production':'0021','Combined Steam & Heat Electricity Production':'0022','Combined Heat & Power Electricity Production':'0023','Satbelization Load Percaentage':'0024','Imported Electricity':'0025','Exorted Electricity':'0026','Critical Electricity Excess Production':'0027','Exportable Electricity Excess Production':'0028','Import Payment':'0029','Added Export Payment':'0030','Renewable Energy Sources [g]':'0100','Hydrolic Powers [g]':'0200','Solar Thermal Powers [g]':'0300','Combined Steam & Heat Production [g]':'0400','Geothermal Heat Production [g]':'0500','Power Plants Electricity Production [g]':'0600','Nuclear [g]':'0700','Pump Consumption [g]':'0800','Turbine Production [g]':'0900','Pump Storage [g]':'1000','Electrolyser Gr.2 [g]':'1100','Electrolyser Gr.3 [g]':'1200','EV & V2G (Transport) [g]':'1300','Nordpool Prices [g]':'1400','Market Prices [g]':'1500','Exports Payment [g]':'1600','Individual Heat 1 [g]':'1700','Individual Electricity [g]':'1800','Individual Heat 2 [g]':'1900','Transports Heat 2 [g]':'2000','District Cooling [g]':'2100','Desalination [g]':'2200','Gas Grid Demand & Balance [g]':'2300'}

monthList = ['January','February','March','April','May','June','July','August','September','October','November','December']
figList, pltList, stdList = [], [], []
figID, pltID, stdID = 1, 1, 1

class Window(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.InitialData()
        self.SwitchHandelers()
        self.Connections()

    def InitialData(self):
        self.cb_FileFormat.addItems(['image','html','json']) 
        self.cb_FileFormat.setCurrentIndex(0)
        self.DataTypeHourly(True)
        self.UpdateTrace()

    def SwitchHandelers(self):
        self.rb_HourlyVal.toggled.connect(self.DataTypeHourly)
        self.rb_MonthlyVal.toggled.connect(self.DataTypeMonthly)
        self.rb_AnnualVal.toggled.connect(self.DataTypeAnnual)
        self.cb_Trace.currentIndexChanged.connect(self.UpdateTrace)
        self.lw_FigList.currentRowChanged.connect(self.UpdateFigSlct)
        self.lw_PltList.currentRowChanged.connect(self.UpdatePltSlct)
        self.lw_StdList.currentRowChanged.connect(self.UpdateStdSlct)
        self.cb_TicksX.stateChanged.connect(self.UpdateTickStateX)
        self.cb_TicksY.stateChanged.connect(self.UpdateTickStateY)

    def DataTypeHourly(self, enabled):
        if enabled:
            self.cb_Trace.clear()
            self.cb_Trace.addItems(['Scatter'])
            self.cb_Trace.setCurrentIndex(0)
            self.rb_Xtime.setEnabled(True)
            self.cb_Xstart.setEnabled(True)
            self.cb_Xstart.clear()
            self.cb_Xend.setEnabled(True)
            self.cb_Xend.clear()
            self.cb_Ydata.clear()
            self.cb_Ydata.addItems(dataList.keys())
            self.cb_Ydata.insertSeparator(30)
            self.cb_Xdata.clear()
            self.cb_Xdata.addItems(dataList.keys())
            self.cb_Xdata.insertSeparator(30)
            self.UpdateTrace()

    def DataTypeMonthly(self, enabled):
        if enabled:
            self.cb_Trace.clear()
            self.cb_Trace.addItems(['Scatter', 'Bar'])
            self.cb_Trace.setCurrentIndex(0)
            self.rb_Xtime.setEnabled(True)
            self.cb_Xstart.setEnabled(True)
            self.cb_Xstart.clear()
            self.cb_Xstart.addItems(monthList)
            self.cb_Xstart.setCurrentIndex(0)
            self.cb_Xend.setEnabled(True)
            self.cb_Xend.clear()
            self.cb_Xend.addItems(monthList)
            self.cb_Xend.setCurrentIndex(11)
            self.cb_Ydata.clear()
            self.cb_Ydata.addItems(dataList.keys())
            self.cb_Ydata.insertSeparator(30)
            self.cb_Xdata.clear()
            self.cb_Xdata.addItems(dataList.keys())
            self.cb_Xdata.insertSeparator(30)
            self.UpdateTrace()

    def DataTypeAnnual(self, enabled):
        if enabled:
            self.cb_Trace.clear()
            self.cb_Trace.addItems(['Bar', 'Pie'])
            self.cb_Trace.setCurrentIndex(0)

            self.rb_Xdata.setChecked(True)
            self.rb_Xtime.setDisabled(True)
            self.cb_Xstart.setDisabled(True)
            self.cb_Xend.setDisabled(True)
            self.cb_Ydata.clear()
            self.cb_Ydata.addItems(dataList.keys())
            self.cb_Ydata.insertSeparator(30)
            self.cb_Xdata.clear()
            self.UpdateTrace()

    def UpdateTrace(self):
        if self.cb_Trace.currentText() == 'Scatter':
            self.cb_Style.clear()
            self.cb_Style.addItems(['Lines + Markers', 'Lines Only', 'Markers Only', 'Smooth Linear'])
            self.cb_Style.setCurrentIndex(0)
            self.cb_FillArea.setEnabled(True)
            self.cb_TicksX.setEnabled(True)
            self.cb_TicksY.setEnabled(True)

        elif self.cb_Trace.currentText() == 'Bar':
            self.cb_Style.clear()
            self.cb_Style.addItems(['Stacked', 'Grouped'])
            self.cb_Style.setCurrentIndex(0)
            self.cb_FillArea.setEnabled(False)
            self.cb_TicksX.setEnabled(False)
            self.cb_TicksY.setEnabled(False)
            if self.rb_AnnualVal.isChecked():
                self.cb_Xdata.clear()
                self.cb_Xdata.addItems(['Total','Average','Maximum','Minimum'])

        elif self.cb_Trace.currentText() == 'Pie':
            self.cb_Style.clear()
            self.cb_Style.addItems(['Domain', 'Domain Spaced'])
            self.cb_Style.setCurrentIndex(0)
            self.cb_FillArea.setEnabled(False)
            self.cb_TicksX.setEnabled(False)
            self.cb_TicksY.setEnabled(False)
            if self.rb_AnnualVal.isChecked():
                self.cb_Xdata.clear()
                self.cb_Xdata.addItems(['Annual CO2 Emissions','Annual Fuel Consumptions','Share of RES'])
                pass

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
            stdParsed = csvParser(path_OPD + '/ops.txt', timeStamp)
            
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
                        'cols': int(self.sb_FigCols.text())}
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

    def SaveFigure(self):
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

        # save figure to file
        figure = plotter(slctFig, slctPlt)
        try:
            if self.cb_FileFormat.currentText() == 'image':
                savePath = QFileDialog.getSaveFileName(self, 'Save File', filter='*.png;;*.jpg;;*.svg')
                figure.write_image(file= savePath[0], scale=3, engine='kaleido')
            elif self.cb_FileFormat.currentText() == 'html':
                savePath = QFileDialog.getSaveFileName(self, 'Save File', filter='*.html')
                figure.write_html(file= savePath[0])
            elif self.cb_FileFormat.currentText() == 'json':
                savePath = QFileDialog.getSaveFileName(self, 'Save File', filter='*.json')
                figure.write_json(file= savePath[0], engine='json')
        except:
            pass

app = QApplication(sys.argv)
mainWindow = Window()
mainWindow.show()
sys.exit(app.exec())