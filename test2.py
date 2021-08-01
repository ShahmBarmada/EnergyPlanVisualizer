import pandas as pd
import re
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox)

#path = 'D:/Workspace/Projects/EnergyPlanVisualizer-Windows/TestOuput/2030_210722043112.csv'
#dfObj = pd.read_csv(path, delimiter=',', low_memory=False, index_col='Index')
#
#test1 = dfObj.loc['h1':'h12','0001_ElectrDemand'].tolist()
#test2 = dfObj.loc['h1':'h12'].index.values.tolist()
#test3 = QFileDialog.getSaveFileName(caption='Save File', filter='*.jpg *.jpeg')
liss = ['one','two','three']
for i in liss:
    print(i)
