import tkinter
from tkinter import filedialog

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

import pandas as pd


rootWindow = tkinter.Tk()
rootWindow.withdraw()

inpath = filedialog.askopenfilename()
outpath = inpath[:inpath.rfind('/')] + '/test.png'

dfObj = pd.read_csv(inpath, low_memory=False)

fig, ax = plt.subplots()
ax.set_xlabel('Hourly Values')
ax.set_ylabel('Electric Demand')
ax.set_title('Electric Demand Jan, Feb, Mar')

xAxis = dfObj.loc[143:311,'g0-Data1']
yAxis = dfObj.loc[143:311,'g2-ElectrDemand']
ax.plot(xAxis, yAxis)

xAxis = dfObj.loc[143:311,'g0-Data1']
yAxis = dfObj.loc[816:984,'g2-ElectrDemand']
ax.plot(xAxis, yAxis)

xAxis = dfObj.loc[143:311,'g0-Data1']
yAxis = dfObj.loc[1487:1655,'g2-ElectrDemand']
ax.plot(xAxis, yAxis)

ax.legend(['January','February','March'])
ax.xaxis.set_major_locator(MultipleLocator(24))
ax.xaxis.set_minor_locator(MultipleLocator(12))
ax.yaxis.set_major_locator(MultipleLocator(5000))

fig.set_size_inches(18.5,10.5)

plt.savefig(outpath)

rootWindow.destroy()
