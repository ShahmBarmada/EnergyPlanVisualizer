# Form implementation generated from reading ui file '.\QtUI\ui_main_window.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ui_MainWindow(object):
    def setupUi(self, ui_MainWindow):
        ui_MainWindow.setObjectName("ui_MainWindow")
        ui_MainWindow.resize(800, 600)
        ui_MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        ui_MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        font = QtGui.QFont()
        font.setPointSize(10)
        ui_MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(ui_MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, -1, 802, 552))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_Stage1 = QtWidgets.QWidget()
        self.tab_Stage1.setObjectName("tab_Stage1")
        self.frame_1 = QtWidgets.QFrame(self.tab_Stage1)
        self.frame_1.setGeometry(QtCore.QRect(-2, -2, 802, 252))
        self.frame_1.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.frame_1.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_1.setLineWidth(1)
        self.frame_1.setObjectName("frame_1")
        self.label_h1 = QtWidgets.QLabel(self.frame_1)
        self.label_h1.setGeometry(QtCore.QRect(10, 10, 90, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_h1.setFont(font)
        self.label_h1.setObjectName("label_h1")
        self.label_1 = QtWidgets.QLabel(self.frame_1)
        self.label_1.setGeometry(QtCore.QRect(10, 40, 126, 24))
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(self.frame_1)
        self.label_2.setGeometry(QtCore.QRect(10, 100, 84, 24))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.frame_1)
        self.label_3.setGeometry(QtCore.QRect(10, 160, 100, 24))
        self.label_3.setObjectName("label_3")
        self.txt_energyplan = QtWidgets.QLineEdit(self.frame_1)
        self.txt_energyplan.setGeometry(QtCore.QRect(10, 70, 691, 24))
        self.txt_energyplan.setObjectName("txt_energyplan")
        self.txt_ipf = QtWidgets.QLineEdit(self.frame_1)
        self.txt_ipf.setGeometry(QtCore.QRect(10, 130, 691, 24))
        self.txt_ipf.setObjectName("txt_ipf")
        self.txt_opd = QtWidgets.QLineEdit(self.frame_1)
        self.txt_opd.setGeometry(QtCore.QRect(10, 190, 691, 24))
        self.txt_opd.setObjectName("txt_opd")
        self.button_energyplan = QtWidgets.QPushButton(self.frame_1)
        self.button_energyplan.setGeometry(QtCore.QRect(710, 70, 75, 24))
        self.button_energyplan.setObjectName("button_energyplan")
        self.button_ipf = QtWidgets.QPushButton(self.frame_1)
        self.button_ipf.setGeometry(QtCore.QRect(710, 130, 75, 24))
        self.button_ipf.setObjectName("button_ipf")
        self.button_opd = QtWidgets.QPushButton(self.frame_1)
        self.button_opd.setGeometry(QtCore.QRect(710, 190, 75, 24))
        self.button_opd.setObjectName("button_opd")
        self.checkBox_opd = QtWidgets.QCheckBox(self.frame_1)
        self.checkBox_opd.setGeometry(QtCore.QRect(30, 220, 250, 24))
        self.checkBox_opd.setObjectName("checkBox_opd")
        self.frame_2 = QtWidgets.QFrame(self.tab_Stage1)
        self.frame_2.setGeometry(QtCore.QRect(-2, 250, 802, 275))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_h2 = QtWidgets.QLabel(self.frame_2)
        self.label_h2.setGeometry(QtCore.QRect(10, 10, 50, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_h2.setFont(font)
        self.label_h2.setObjectName("label_h2")
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(10, 50, 49, 24))
        self.label_4.setObjectName("label_4")
        self.txt_Log = QtWidgets.QTextBrowser(self.frame_2)
        self.txt_Log.setGeometry(QtCore.QRect(70, 50, 715, 211))
        self.txt_Log.setObjectName("txt_Log")
        self.button_Exec = QtWidgets.QPushButton(self.frame_2)
        self.button_Exec.setEnabled(False)
        self.button_Exec.setGeometry(QtCore.QRect(700, 10, 85, 24))
        self.button_Exec.setObjectName("button_Exec")
        self.label_State = QtWidgets.QLabel(self.frame_2)
        self.label_State.setGeometry(QtCore.QRect(70, 10, 621, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        font.setUnderline(True)
        font.setStrikeOut(False)
        self.label_State.setFont(font)
        self.label_State.setObjectName("label_State")
        self.tabWidget.addTab(self.tab_Stage1, "")
        self.tab_Stage2 = QtWidgets.QWidget()
        self.tab_Stage2.setObjectName("tab_Stage2")
        self.tabWidget.addTab(self.tab_Stage2, "")
        ui_MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ui_MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        ui_MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ui_MainWindow)
        self.statusbar.setObjectName("statusbar")
        ui_MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(ui_MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtGui.QAction(ui_MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionExit)
        self.menuFile.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(ui_MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ui_MainWindow)

    def retranslateUi(self, ui_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        ui_MainWindow.setWindowTitle(_translate("ui_MainWindow", "EnergyPLAN Visulaizer"))
        self.label_h1.setText(_translate("ui_MainWindow", "Configuration:"))
        self.label_1.setText(_translate("ui_MainWindow", "EnergyPLAN.exe Path:"))
        self.label_2.setText(_translate("ui_MainWindow", "Input File Path:"))
        self.label_3.setText(_translate("ui_MainWindow", "Output Directory:"))
        self.button_energyplan.setText(_translate("ui_MainWindow", "Select"))
        self.button_ipf.setText(_translate("ui_MainWindow", "Select"))
        self.button_opd.setText(_translate("ui_MainWindow", "Browse"))
        self.checkBox_opd.setText(_translate("ui_MainWindow", "Open Ouput directory after processing"))
        self.label_h2.setText(_translate("ui_MainWindow", "Process:"))
        self.label_4.setText(_translate("ui_MainWindow", "Log:"))
        self.button_Exec.setText(_translate("ui_MainWindow", "Execute"))
        self.label_State.setText(_translate("ui_MainWindow", "<html><head/><body><p><span style=\" color:#ff0000;\">Please load required data above first.</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Stage1), _translate("ui_MainWindow", "Process Study File"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Stage2), _translate("ui_MainWindow", "Visualize Study Output"))
        self.menuFile.setTitle(_translate("ui_MainWindow", "Menu"))
        self.actionExit.setText(_translate("ui_MainWindow", "Exit"))
        self.actionAbout.setText(_translate("ui_MainWindow", "About"))
