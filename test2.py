import pandas as pd
import re

path = 'D:/Workspace/Projects/EnergyPlanVisualizer-Windows/TestOuput/2030_210722043112.csv'
dfObj = pd.read_csv(path, delimiter=',', low_memory=False, index_col='Index')

test1 = dfObj.loc['h1':'h12','0001_ElectrDemand'].tolist()
test2 = dfObj.loc['h1':'h12'].index.values.tolist()


print(test1)
print(test2)