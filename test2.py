import pandas as pd

path = 'D:/Projects/EnergyPlanVisualizer-Windows/TestOuput/2030_210722043112.csv'
dfObj = pd.read_csv(path, delimiter=',', low_memory=False, index_col='Index')

print(dfObj.loc[['January','February','March','April','May','June','July','August','September','October','November','December'],'0001_ElectrDemand'].tolist())