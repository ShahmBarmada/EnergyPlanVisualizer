# Form implementation generated from reading ui file '.\QtUI\ui_main_window.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 646)
        MainWindow.setMinimumSize(QtCore.QSize(900, 646))
        MainWindow.setMaximumSize(QtCore.QSize(900, 646))
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(9, 9, 881, 581))
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.stackedWidget.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.lbl_pg1 = QtWidgets.QLabel(self.page_1)
        self.lbl_pg1.setGeometry(QtCore.QRect(800, 0, 40, 18))

        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        self.lbl_pg1.setFont(font)
        self.lbl_pg1.setObjectName("lbl_pg1")
        self.gb_Config = QtWidgets.QGroupBox(self.page_1)
        self.gb_Config.setGeometry(QtCore.QRect(0, 20, 880, 280))

        font.setBold(False)
        self.gb_Config.setFont(font)
        self.gb_Config.setFlat(True)
        self.gb_Config.setObjectName("gb_Config")
        self.lbl_ExePath = QtWidgets.QLabel(self.gb_Config)
        self.lbl_ExePath.setGeometry(QtCore.QRect(20, 30, 130, 24))
        self.lbl_ExePath.setObjectName("lbl_ExePath")
        self.txt_ExePath = QtWidgets.QLineEdit(self.gb_Config)
        self.txt_ExePath.setGeometry(QtCore.QRect(20, 60, 751, 24))
        self.txt_ExePath.setObjectName("txt_ExePath")
        self.btn_ExePath = QtWidgets.QPushButton(self.gb_Config)
        self.btn_ExePath.setGeometry(QtCore.QRect(790, 60, 75, 24))
        self.btn_ExePath.setObjectName("btn_ExePath")
        self.lbl_IPF = QtWidgets.QLabel(self.gb_Config)
        self.lbl_IPF.setGeometry(QtCore.QRect(20, 90, 130, 24))
        self.lbl_IPF.setObjectName("lbl_IPF")
        self.btn_IPF = QtWidgets.QPushButton(self.gb_Config)
        self.btn_IPF.setGeometry(QtCore.QRect(790, 120, 75, 24))
        self.btn_IPF.setObjectName("btn_IPF")
        self.txt_IPF = QtWidgets.QLineEdit(self.gb_Config)
        self.txt_IPF.setGeometry(QtCore.QRect(20, 120, 751, 24))
        self.txt_IPF.setObjectName("txt_IPF")
        self.lbl_OPD = QtWidgets.QLabel(self.gb_Config)
        self.lbl_OPD.setGeometry(QtCore.QRect(20, 150, 130, 24))
        self.lbl_OPD.setObjectName("lbl_OPD")
        self.btn_OPD = QtWidgets.QPushButton(self.gb_Config)
        self.btn_OPD.setGeometry(QtCore.QRect(790, 180, 75, 24))
        self.btn_OPD.setObjectName("btn_OPD")
        self.txt_OPD = QtWidgets.QLineEdit(self.gb_Config)
        self.txt_OPD.setGeometry(QtCore.QRect(20, 180, 751, 24))
        self.txt_OPD.setObjectName("txt_OPD")
        self.cb_OpenOPD = QtWidgets.QCheckBox(self.gb_Config)
        self.cb_OpenOPD.setGeometry(QtCore.QRect(40, 210, 247, 22))
        self.cb_OpenOPD.setObjectName("cb_OpenOPD")
        self.cb_LoadVis = QtWidgets.QCheckBox(self.gb_Config)
        self.cb_LoadVis.setGeometry(QtCore.QRect(40, 240, 247, 22))
        self.cb_LoadVis.setObjectName("cb_LoadVis")
        self.gb_Process = QtWidgets.QGroupBox(self.page_1)
        self.gb_Process.setGeometry(QtCore.QRect(0, 300, 880, 280))
        self.gb_Process.setFlat(True)
        self.gb_Process.setObjectName("gb_Process")
        self.lbl_State = QtWidgets.QLabel(self.gb_Process)
        self.lbl_State.setGeometry(QtCore.QRect(20, 30, 32, 24))
        self.lbl_State.setObjectName("lbl_State")
        self.txt_Log = QtWidgets.QTextBrowser(self.gb_Process)
        self.txt_Log.setGeometry(QtCore.QRect(60, 80, 811, 192))
        self.txt_Log.setSource(QtCore.QUrl(""))
        self.txt_Log.setObjectName("txt_Log")
        self.lbl_Log = QtWidgets.QLabel(self.gb_Process)
        self.lbl_Log.setGeometry(QtCore.QRect(20, 80, 32, 24))
        self.lbl_Log.setObjectName("lbl_Log")
        self.lbl_Status = QtWidgets.QLabel(self.gb_Process)
        self.lbl_Status.setGeometry(QtCore.QRect(60, 30, 711, 24))
        self.lbl_Status.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.lbl_Status.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.lbl_Status.setObjectName("lbl_Status")
        self.lbl_Status.setStyleSheet("font-style:italic; text-align:center; color:red")
        self.lbl_Status.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.btn_Exec = QtWidgets.QPushButton(self.gb_Process)
        self.btn_Exec.setGeometry(QtCore.QRect(790, 30, 75, 24))
        self.btn_Exec.setObjectName("btn_Exec")
        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.lbl_pg2 = QtWidgets.QLabel(self.page_2)
        self.lbl_pg2.setGeometry(QtCore.QRect(800, 0, 40, 18))

        font.setBold(True)
        font.setUnderline(False)
        self.lbl_pg2.setFont(font)
        self.lbl_pg2.setObjectName("lbl_pg2")
        self.gb_Plots = QtWidgets.QGroupBox(self.page_2)
        self.gb_Plots.setGeometry(QtCore.QRect(305, 20, 575, 560))
        self.gb_Plots.setFlat(False)
        self.gb_Plots.setCheckable(False)
        self.gb_Plots.setObjectName("gb_Plots")
        self.lw_PltList = QtWidgets.QListWidget(self.gb_Plots)
        self.lw_PltList.setGeometry(QtCore.QRect(385, 310, 180, 205))
        self.lw_PltList.setObjectName("lw_PltList")
        self.lw_StdList = QtWidgets.QListWidget(self.gb_Plots)
        self.lw_StdList.setGeometry(QtCore.QRect(385, 40, 180, 205))
        self.lw_StdList.setObjectName("lw_StdList")
        self.btn_PltNew = QtWidgets.QPushButton(self.gb_Plots)
        self.btn_PltNew.setGeometry(QtCore.QRect(385, 520, 70, 24))
        self.btn_PltNew.setObjectName("btn_PltNew")
        self.btn_PltDlt = QtWidgets.QPushButton(self.gb_Plots)
        self.btn_PltDlt.setGeometry(QtCore.QRect(495, 520, 70, 24))
        self.btn_PltDlt.setObjectName("btn_PltDlt")
        self.lbl23 = QtWidgets.QLabel(self.gb_Plots)
        self.lbl23.setGeometry(QtCore.QRect(385, 290, 80, 20))
        self.lbl23.setObjectName("lbl23")
        self.lbl24 = QtWidgets.QLabel(self.gb_Plots)
        self.lbl24.setGeometry(QtCore.QRect(385, 20, 80, 20))
        self.lbl24.setObjectName("lbl24")
        self.btn_StdLoad = QtWidgets.QPushButton(self.gb_Plots)
        self.btn_StdLoad.setGeometry(QtCore.QRect(385, 250, 70, 24))
        self.btn_StdLoad.setObjectName("btn_StdLoad")
        self.btn_StdRemove = QtWidgets.QPushButton(self.gb_Plots)
        self.btn_StdRemove.setGeometry(QtCore.QRect(495, 250, 70, 24))
        self.btn_StdRemove.setObjectName("btn_StdRemove")
        self.gb_PlotConfigs = QtWidgets.QGroupBox(self.gb_Plots)
        self.gb_PlotConfigs.setGeometry(QtCore.QRect(10, 30, 365, 215))
        self.gb_PlotConfigs.setFlat(True)
        self.gb_PlotConfigs.setObjectName("gb_PlotConfigs")
        self.cb_Trace = QtWidgets.QComboBox(self.gb_PlotConfigs)
        self.cb_Trace.setGeometry(QtCore.QRect(60, 25, 110, 24))
        self.cb_Trace.setObjectName("cb_Trace")
        self.rb_HourlyVal = QtWidgets.QRadioButton(self.gb_PlotConfigs)
        self.rb_HourlyVal.setGeometry(QtCore.QRect(60, 60, 110, 24))
        self.rb_HourlyVal.setChecked(True)
        self.rb_HourlyVal.setObjectName("rb_HourlyVal")
        self.rb_MonthlyVal = QtWidgets.QRadioButton(self.gb_PlotConfigs)
        self.rb_MonthlyVal.setGeometry(QtCore.QRect(60, 90, 110, 24))
        self.rb_MonthlyVal.setObjectName("rb_MonthlyVal")
        self.rb_AnnualVal = QtWidgets.QRadioButton(self.gb_PlotConfigs)
        self.rb_AnnualVal.setEnabled(False)
        self.rb_AnnualVal.setGeometry(QtCore.QRect(60, 120, 110, 24))
        self.rb_AnnualVal.setObjectName("rb_AnnualVal")
        self.lbl10 = QtWidgets.QLabel(self.gb_PlotConfigs)
        self.lbl10.setGeometry(QtCore.QRect(10, 25, 40, 24))
        self.lbl10.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl10.setObjectName("lbl10")
        self.cb_Style = QtWidgets.QComboBox(self.gb_PlotConfigs)
        self.cb_Style.setGeometry(QtCore.QRect(245, 25, 110, 24))
        self.cb_Style.setObjectName("cb_Style")
        self.lbl11 = QtWidgets.QLabel(self.gb_PlotConfigs)
        self.lbl11.setGeometry(QtCore.QRect(195, 25, 40, 24))
        self.lbl11.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl11.setObjectName("lbl11")
        self.lbl12 = QtWidgets.QLabel(self.gb_PlotConfigs)
        self.lbl12.setGeometry(QtCore.QRect(10, 60, 40, 24))
        self.lbl12.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl12.setObjectName("lbl12")
        self.lbl13 = QtWidgets.QLabel(self.gb_PlotConfigs)
        self.lbl13.setGeometry(QtCore.QRect(185, 60, 50, 24))
        self.lbl13.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl13.setObjectName("lbl13")
        self.cb_FillArea = QtWidgets.QCheckBox(self.gb_PlotConfigs)
        self.cb_FillArea.setEnabled(True)
        self.cb_FillArea.setGeometry(QtCore.QRect(245, 60, 110, 24))
        self.cb_FillArea.setObjectName("cb_FillArea")
        self.cb_TicksX = QtWidgets.QCheckBox(self.gb_PlotConfigs)
        self.cb_TicksX.setEnabled(True)
        self.cb_TicksX.setGeometry(QtCore.QRect(245, 90, 50, 24))
        self.cb_TicksX.setChecked(True)
        self.cb_TicksX.setObjectName("cb_TicksX")
        self.txt_TicksX = QtWidgets.QLineEdit(self.gb_PlotConfigs)
        self.txt_TicksX.setEnabled(False)
        self.txt_TicksX.setGeometry(QtCore.QRect(305, 90, 50, 24))
        self.txt_TicksX.setText("")
        self.txt_TicksX.setFrame(True)
        self.txt_TicksX.setObjectName("txt_TicksX")
        self.cb_TicksY = QtWidgets.QCheckBox(self.gb_PlotConfigs)
        self.cb_TicksY.setEnabled(True)
        self.cb_TicksY.setGeometry(QtCore.QRect(245, 120, 50, 24))
        self.cb_TicksY.setChecked(True)
        self.cb_TicksY.setObjectName("cb_TicksY")
        self.txt_TicksY = QtWidgets.QLineEdit(self.gb_PlotConfigs)
        self.txt_TicksY.setEnabled(False)
        self.txt_TicksY.setGeometry(QtCore.QRect(305, 120, 50, 24))
        self.txt_TicksY.setText("")
        self.txt_TicksY.setObjectName("txt_TicksY")
        self.lbl14 = QtWidgets.QLabel(self.gb_PlotConfigs)
        self.lbl14.setGeometry(QtCore.QRect(185, 90, 50, 24))
        self.lbl14.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl14.setObjectName("lbl14")
        self.lbl15 = QtWidgets.QLabel(self.gb_PlotConfigs)
        self.lbl15.setGeometry(QtCore.QRect(185, 120, 50, 24))
        self.lbl15.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl15.setObjectName("lbl15")
        self.lbl16 = QtWidgets.QLabel(self.gb_PlotConfigs)
        self.lbl16.setGeometry(QtCore.QRect(10, 150, 100, 24))
        self.lbl16.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl16.setObjectName("lbl16")
        self.lbl19 = QtWidgets.QLabel(self.gb_PlotConfigs)
        self.lbl19.setGeometry(QtCore.QRect(115, 180, 40, 24))
        self.lbl19.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl19.setObjectName("lbl19")
        self.sb_Row = QtWidgets.QSpinBox(self.gb_PlotConfigs)
        self.sb_Row.setGeometry(QtCore.QRect(160, 150, 50, 24))
        self.sb_Row.setMinimum(1)
        self.sb_Row.setMaximum(12)
        self.sb_Row.setObjectName("sb_Row")
        self.lbl17 = QtWidgets.QLabel(self.gb_PlotConfigs)
        self.lbl17.setGeometry(QtCore.QRect(115, 150, 40, 24))
        self.lbl17.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl17.setObjectName("lbl17")
        self.sb_Col = QtWidgets.QSpinBox(self.gb_PlotConfigs)
        self.sb_Col.setGeometry(QtCore.QRect(160, 180, 50, 24))
        self.sb_Col.setMinimum(1)
        self.sb_Col.setMaximum(12)
        self.sb_Col.setObjectName("sb_Col")
        self.lbl18 = QtWidgets.QLabel(self.gb_PlotConfigs)
        self.lbl18.setGeometry(QtCore.QRect(235, 150, 60, 24))
        self.lbl18.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl18.setObjectName("lbl18")
        self.sb_RowSpan = QtWidgets.QSpinBox(self.gb_PlotConfigs)
        self.sb_RowSpan.setGeometry(QtCore.QRect(305, 150, 50, 24))
        self.sb_RowSpan.setMinimum(1)
        self.sb_RowSpan.setMaximum(12)
        self.sb_RowSpan.setObjectName("sb_RowSpan")
        self.sb_ColSpan = QtWidgets.QSpinBox(self.gb_PlotConfigs)
        self.sb_ColSpan.setGeometry(QtCore.QRect(305, 180, 50, 24))
        self.sb_ColSpan.setMinimum(1)
        self.sb_ColSpan.setMaximum(12)
        self.sb_ColSpan.setObjectName("sb_ColSpan")
        self.lbl20 = QtWidgets.QLabel(self.gb_PlotConfigs)
        self.lbl20.setGeometry(QtCore.QRect(235, 180, 60, 24))
        self.lbl20.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl20.setObjectName("lbl20")
        self.gb_SeriesX = QtWidgets.QGroupBox(self.gb_Plots)
        self.gb_SeriesX.setGeometry(QtCore.QRect(10, 300, 365, 120))
        self.gb_SeriesX.setFlat(True)
        self.gb_SeriesX.setObjectName("gb_SeriesX")
        self.cb_Xdata = QtWidgets.QComboBox(self.gb_SeriesX)
        self.cb_Xdata.setGeometry(QtCore.QRect(110, 90, 245, 24))
        self.cb_Xdata.setObjectName("cb_Xdata")
        self.cb_Xstart = QtWidgets.QComboBox(self.gb_SeriesX)
        self.cb_Xstart.setGeometry(QtCore.QRect(150, 25, 130, 24))
        self.cb_Xstart.setEditable(True)
        self.cb_Xstart.setObjectName("cb_Xstart")
        self.lbl21 = QtWidgets.QLabel(self.gb_SeriesX)
        self.lbl21.setGeometry(QtCore.QRect(110, 25, 30, 24))
        self.lbl21.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl21.setObjectName("lbl21")
        self.lbl22 = QtWidgets.QLabel(self.gb_SeriesX)
        self.lbl22.setGeometry(QtCore.QRect(110, 55, 30, 24))
        self.lbl22.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl22.setObjectName("lbl22")
        self.cb_Xend = QtWidgets.QComboBox(self.gb_SeriesX)
        self.cb_Xend.setGeometry(QtCore.QRect(150, 55, 130, 24))
        self.cb_Xend.setEditable(True)
        self.cb_Xend.setObjectName("cb_Xend")
        self.rb_Xtime = QtWidgets.QRadioButton(self.gb_SeriesX)
        self.rb_Xtime.setChecked(True)
        self.rb_Xtime.setGeometry(QtCore.QRect(10, 25, 90, 24))
        self.rb_Xtime.setObjectName("rb_Xtime")
        self.rb_Xdata = QtWidgets.QRadioButton(self.gb_SeriesX)
        self.rb_Xdata.setGeometry(QtCore.QRect(10, 90, 90, 24))
        self.rb_Xdata.setObjectName("rb_Xdata")
        self.gb_SeriesY = QtWidgets.QGroupBox(self.gb_Plots)
        self.gb_SeriesY.setGeometry(QtCore.QRect(10, 440, 365, 50))
        self.gb_SeriesY.setFlat(True)
        self.gb_SeriesY.setObjectName("gb_SeriesY")
        self.cb_Ydata = QtWidgets.QComboBox(self.gb_SeriesY)
        self.cb_Ydata.setGeometry(QtCore.QRect(110, 20, 245, 24))
        self.cb_Ydata.setObjectName("cb_Ydata")
        self.gb_Figures = QtWidgets.QGroupBox(self.page_2)
        self.gb_Figures.setGeometry(QtCore.QRect(0, 20, 295, 440))
        self.gb_Figures.setFlat(False)
        self.gb_Figures.setObjectName("gb_Figures")
        self.lw_FigList = QtWidgets.QListWidget(self.gb_Figures)
        self.lw_FigList.setGeometry(QtCore.QRect(90, 160, 195, 210))
        self.lw_FigList.setObjectName("lw_FigList")
        self.btn_FigDlt = QtWidgets.QPushButton(self.gb_Figures)
        self.btn_FigDlt.setGeometry(QtCore.QRect(215, 130, 70, 24))
        self.btn_FigDlt.setObjectName("btn_FigDlt")
        self.lbl08 = QtWidgets.QLabel(self.gb_Figures)
        self.lbl08.setGeometry(QtCore.QRect(10, 160, 70, 24))
        self.lbl08.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl08.setObjectName("lbl08")
        self.btn_FigAdd = QtWidgets.QPushButton(self.gb_Figures)
        self.btn_FigAdd.setGeometry(QtCore.QRect(90, 130, 70, 24))
        self.btn_FigAdd.setObjectName("btn_FigAdd")
        self.lbl01 = QtWidgets.QLabel(self.gb_Figures)
        self.lbl01.setGeometry(QtCore.QRect(10, 30, 70, 24))

        font.setBold(False)
        self.lbl01.setFont(font)
        self.lbl01.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl01.setObjectName("lbl01")
        self.txt_FigName = QtWidgets.QLineEdit(self.gb_Figures)
        self.txt_FigName.setGeometry(QtCore.QRect(90, 30, 195, 24))
        self.txt_FigName.setObjectName("txt_FigName")
        self.lbl02 = QtWidgets.QLabel(self.gb_Figures)
        self.lbl02.setGeometry(QtCore.QRect(10, 60, 70, 24))
        self.lbl02.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl02.setObjectName("lbl02")
        self.sb_FigCols = QtWidgets.QSpinBox(self.gb_Figures)
        self.sb_FigCols.setGeometry(QtCore.QRect(235, 60, 50, 24))
        self.sb_FigCols.setMinimum(1)
        self.sb_FigCols.setMaximum(12)
        self.sb_FigCols.setObjectName("sb_FigCols")
        self.lbl03 = QtWidgets.QLabel(self.gb_Figures)
        self.lbl03.setGeometry(QtCore.QRect(90, 60, 40, 24))
        self.lbl03.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl03.setObjectName("lbl03")
        self.sb_FigRows = QtWidgets.QSpinBox(self.gb_Figures)
        self.sb_FigRows.setGeometry(QtCore.QRect(135, 60, 50, 24))
        self.sb_FigRows.setMinimum(1)
        self.sb_FigRows.setMaximum(12)
        self.sb_FigRows.setObjectName("sb_FigRows")
        self.lbl04 = QtWidgets.QLabel(self.gb_Figures)
        self.lbl04.setGeometry(QtCore.QRect(190, 60, 40, 24))
        self.lbl04.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl04.setObjectName("lbl04")
        self.lbl05 = QtWidgets.QLabel(self.gb_Figures)
        self.lbl05.setGeometry(QtCore.QRect(10, 90, 70, 24))
        self.lbl05.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl05.setObjectName("lbl05")
        self.lbl06 = QtWidgets.QLabel(self.gb_Figures)
        self.lbl06.setGeometry(QtCore.QRect(90, 90, 40, 24))
        self.lbl06.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl06.setObjectName("lbl06")
        self.lbl07 = QtWidgets.QLabel(self.gb_Figures)
        self.lbl07.setGeometry(QtCore.QRect(190, 90, 40, 24))
        self.lbl07.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl07.setObjectName("lbl07")
        self.txt_FigWidth = QtWidgets.QLineEdit(self.gb_Figures)
        self.txt_FigWidth.setGeometry(QtCore.QRect(135, 90, 50, 24))
        self.txt_FigWidth.setObjectName("txt_FigWidth")
        self.txt_FigHeight = QtWidgets.QLineEdit(self.gb_Figures)
        self.txt_FigHeight.setGeometry(QtCore.QRect(235, 90, 50, 24))
        self.txt_FigHeight.setObjectName("txt_FigHeight")
        self.lbl09 = QtWidgets.QLabel(self.gb_Figures)
        self.lbl09.setGeometry(QtCore.QRect(10, 380, 70, 24))
        self.lbl09.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl09.setObjectName("lbl09")
        self.cb_FileFormat = QtWidgets.QComboBox(self.gb_Figures)
        self.cb_FileFormat.setGeometry(QtCore.QRect(90, 380, 105, 24))
        self.cb_FileFormat.setCurrentText("")
        self.cb_FileFormat.setObjectName("cb_FileFormat")
        self.btn_FigSave = QtWidgets.QPushButton(self.gb_Figures)
        self.btn_FigSave.setGeometry(QtCore.QRect(205, 380, 80, 24))
        self.btn_FigSave.setObjectName("btn_FigSave")
        self.btn_FigView = QtWidgets.QPushButton(self.gb_Figures)
        self.btn_FigView.setGeometry(QtCore.QRect(90, 410, 105, 24))
        self.btn_FigView.setObjectName("btn_FigView")
        self.btn_FigLoad = QtWidgets.QPushButton(self.gb_Figures)
        self.btn_FigLoad.setGeometry(QtCore.QRect(205, 410, 80, 24))
        self.btn_FigLoad.setObjectName("btn_FigLoad")
        self.gb_Info = QtWidgets.QGroupBox(self.page_2)
        self.gb_Info.setGeometry(QtCore.QRect(0, 460, 295, 120))
        self.gb_Info.setObjectName("gb_Info")
        self.lbl_Selection1 = QtWidgets.QLabel(self.gb_Info)
        self.lbl_Selection1.setGeometry(QtCore.QRect(10, 30, 95, 24))
        self.lbl_Selection1.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl_Selection1.setObjectName("lbl_Selection1")
        self.lbl_Selection2 = QtWidgets.QLabel(self.gb_Info)
        self.lbl_Selection2.setGeometry(QtCore.QRect(10, 60, 95, 24))
        self.lbl_Selection2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl_Selection2.setObjectName("lbl_Selection2")
        self.lbl_Selection3 = QtWidgets.QLabel(self.gb_Info)
        self.lbl_Selection3.setGeometry(QtCore.QRect(10, 90, 95, 24))
        self.lbl_Selection3.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl_Selection3.setObjectName("lbl_Selection3")

        font.setItalic(True)
        self.lbl_SlctFig = QtWidgets.QLabel(self.gb_Info)
        self.lbl_SlctFig.setGeometry(QtCore.QRect(115, 30, 170, 24))
        self.lbl_SlctFig.setFont(font)
        self.lbl_SlctFig.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.lbl_SlctFig.setObjectName("lbl_SlctFig")
        self.lbl_SlctFig.setStyleSheet("border-bottom-width: 1px; border-bottom-style: solid; border-radius: 0px; color: red;")
        self.lbl_SlctPlt = QtWidgets.QLabel(self.gb_Info)
        self.lbl_SlctPlt.setGeometry(QtCore.QRect(115, 60, 170, 24))
        self.lbl_SlctPlt.setFont(font)
        self.lbl_SlctPlt.setObjectName("lbl_SlctPlt")
        self.lbl_SlctPlt.setStyleSheet("border-bottom-width: 1px; border-bottom-style: solid; border-radius: 0px; color: red;")
        self.lbl_SlctStd = QtWidgets.QLabel(self.gb_Info)
        self.lbl_SlctStd.setGeometry(QtCore.QRect(115, 90, 170, 24))
        self.lbl_SlctStd.setFont(font)
        self.lbl_SlctStd.setObjectName("lbl_SlctStd")
        self.lbl_SlctStd.setStyleSheet("border-bottom-width: 1px; border-bottom-style: solid; border-radius: 0px; color: red;")
        
        self.gb_Config.setStyleSheet("QGroupBox {font-weight: bold;}")
        self.gb_Figures.setStyleSheet("QGroupBox {font-weight: bold;}")
        self.gb_Info.setStyleSheet("QGroupBox {font-weight: bold;}")
        self.gb_Plots.setStyleSheet("QGroupBox {font-weight: bold;}")
        self.gb_Process.setStyleSheet("QGroupBox {font-weight: bold;}")
        self.stackedWidget.addWidget(self.page_2)
        self.btn_Page = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Page.setGeometry(QtCore.QRect(850, 8, 30, 21))
        self.btn_Page.setObjectName("btn_Page")
        self.btn_Page.setFlat(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 24))
        self.menubar.setObjectName("menubar")
        self.m_Menu = QtWidgets.QMenu(self.menubar)
        self.m_Menu.setObjectName("m_Menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.m_Menu.addAction(self.actionAbout)
        self.m_Menu.addAction(self.actionExit)
        self.menubar.addAction(self.m_Menu.menuAction())

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        self.cb_FileFormat.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EnergyPLAN Visuzalizer"))
        self.lbl_pg1.setText(_translate("MainWindow", "Page 1"))
        self.gb_Config.setTitle(_translate("MainWindow", "Configuration"))
        self.lbl_ExePath.setText(_translate("MainWindow", "EnergyPLAN .exe Path:"))
        self.btn_ExePath.setText(_translate("MainWindow", "Select"))
        self.lbl_IPF.setText(_translate("MainWindow", "Input File Path:"))
        self.btn_IPF.setText(_translate("MainWindow", "Select"))
        self.lbl_OPD.setText(_translate("MainWindow", "Output Directory:"))
        self.btn_OPD.setText(_translate("MainWindow", "Browse"))
        self.cb_OpenOPD.setText(_translate("MainWindow", "Open output directiry after processing"))
        self.cb_LoadVis.setText(_translate("MainWindow", "Load Study to Visualizer"))
        self.gb_Process.setTitle(_translate("MainWindow", "Process"))
        self.lbl_State.setText(_translate("MainWindow", "State:"))
        self.lbl_Log.setText(_translate("MainWindow", "Log:"))
        self.lbl_Status.setText(_translate("MainWindow", "Use the options above to process a study input file"))
        self.btn_Exec.setText(_translate("MainWindow", "Execute"))
        self.lbl_pg2.setText(_translate("MainWindow", "Page 2"))
        self.gb_Plots.setTitle(_translate("MainWindow", "Plots"))
        self.btn_PltNew.setText(_translate("MainWindow", "New"))
        self.btn_PltDlt.setText(_translate("MainWindow", "Delete"))
        self.lbl23.setText(_translate("MainWindow", "Plots List:"))
        self.lbl24.setText(_translate("MainWindow", "Studies List:"))
        self.btn_StdLoad.setText(_translate("MainWindow", "Load"))
        self.btn_StdRemove.setText(_translate("MainWindow", "Remove"))
        self.gb_PlotConfigs.setTitle(_translate("MainWindow", "Plot Configurations:"))
        self.rb_HourlyVal.setText(_translate("MainWindow", "Hourly Values"))
        self.rb_MonthlyVal.setText(_translate("MainWindow", "Monthly Values"))
        self.rb_AnnualVal.setText(_translate("MainWindow", "Annual Values"))
        self.lbl10.setText(_translate("MainWindow", "Trace:"))
        self.lbl11.setText(_translate("MainWindow", "Style:"))
        self.lbl12.setText(_translate("MainWindow", "Type:"))
        self.lbl13.setText(_translate("MainWindow", "Options:"))
        self.cb_FillArea.setText(_translate("MainWindow", "Fill Under Lines"))
        self.cb_TicksX.setText(_translate("MainWindow", "Auto"))
        self.txt_TicksX.setInputMask(_translate("MainWindow", "0009"))
        self.cb_TicksY.setText(_translate("MainWindow", "Auto"))
        self.txt_TicksY.setInputMask(_translate("MainWindow", "0009"))
        self.lbl14.setText(_translate("MainWindow", "X Ticks"))
        self.lbl15.setText(_translate("MainWindow", "Y Ticks"))
        self.lbl16.setText(_translate("MainWindow", "Position in Grid:"))
        self.lbl19.setText(_translate("MainWindow", "Col"))
        self.lbl17.setText(_translate("MainWindow", "Row"))
        self.lbl18.setText(_translate("MainWindow", "Row Span"))
        self.lbl20.setText(_translate("MainWindow", "Col Span"))
        self.gb_SeriesX.setTitle(_translate("MainWindow", "Range (X Axis):"))
        self.lbl21.setText(_translate("MainWindow", "From"))
        self.lbl22.setText(_translate("MainWindow", "To"))
        self.rb_Xtime.setText(_translate("MainWindow", "Time Series"))
        self.rb_Xdata.setText(_translate("MainWindow", "Data Series"))
        self.gb_SeriesY.setTitle(_translate("MainWindow", "Data (Y Axis):"))
        self.gb_Figures.setTitle(_translate("MainWindow", "Figures"))
        self.btn_FigDlt.setText(_translate("MainWindow", "Delete"))
        self.lbl08.setText(_translate("MainWindow", "Figuers List:"))
        self.btn_FigAdd.setText(_translate("MainWindow", "Add"))
        self.lbl01.setText(_translate("MainWindow", "Name:"))
        self.lbl02.setText(_translate("MainWindow", "Grid:"))
        self.lbl03.setText(_translate("MainWindow", "Rows"))
        self.lbl04.setText(_translate("MainWindow", "Cols"))
        self.lbl05.setText(_translate("MainWindow", "Size (Pixels):"))
        self.lbl06.setText(_translate("MainWindow", "Width"))
        self.lbl07.setText(_translate("MainWindow", "Height"))
        self.txt_FigWidth.setInputMask(_translate("MainWindow", "0009"))
        self.txt_FigWidth.setText(_translate("MainWindow", "1366"))
        self.txt_FigHeight.setInputMask(_translate("MainWindow", "0009"))
        self.txt_FigHeight.setText(_translate("MainWindow", "768"))
        self.lbl09.setText(_translate("MainWindow", "File Format:"))
        self.btn_FigSave.setText(_translate("MainWindow", "Save"))
        self.btn_FigView.setText(_translate("MainWindow", "Preview"))
        self.btn_FigLoad.setText(_translate("MainWindow", "Load"))
        self.gb_Info.setTitle(_translate("MainWindow", "Information"))
        self.lbl_Selection1.setText(_translate("MainWindow", "Selected Figure:"))
        self.lbl_Selection2.setText(_translate("MainWindow", "Selected Plot:"))
        self.lbl_Selection3.setText(_translate("MainWindow", "Selected Study:"))
        self.lbl_SlctFig.setText(_translate("MainWindow", "none"))
        self.lbl_SlctPlt.setText(_translate("MainWindow", "none"))
        self.lbl_SlctStd.setText(_translate("MainWindow", "none"))
        self.btn_Page.setText(_translate("MainWindow", "\u2B9C\u2B9E"))
        self.m_Menu.setTitle(_translate("MainWindow", "Menu"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
