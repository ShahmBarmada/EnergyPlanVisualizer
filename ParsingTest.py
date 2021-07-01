import tkinter
from tkinter import *
from tkinter import filedialog

import pandas as pd
import csv

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

rootWindow = tkinter.Tk()
rootWindow.withdraw()

inPath = filedialog.askopenfilename()
outPath = inPath[:inPath.rfind('/')] + '/test.png'
headerPath = inPath[:inPath.rfind('/')] + '/HeaderDictionary.csv'

StudyDF = pd.read_csv(inPath, low_memory=False)

with open(headerPath, 'r') as ipf:
    aliasDict = {rows[0]:rows[1] for rows in csv.reader(ipf)}

aliasList = list(aliasDict.values())
headerList = list(aliasDict.keys())

fig, ax = plt.subplots()
ax.set_xlabel('Hourly Values')
ax.set_ylabel('Electric Demand')
ax.set_title('Electric Demand Jan, Feb, Mar')

xAxis = StudyDF.loc[143:311,'g0-Data1']
yAxis = StudyDF.loc[143:311,'g2-ElectrDemand']
ax.plot(xAxis, yAxis)

xAxis = StudyDF.loc[143:311,'g0-Data1']
yAxis = StudyDF.loc[816:984,'g2-ElectrDemand']
ax.plot(xAxis, yAxis)

xAxis = StudyDF.loc[143:311,'g0-Data1']
yAxis = StudyDF.loc[1487:1655,'g2-ElectrDemand']
ax.plot(xAxis, yAxis)

ax.legend(['January','February','March'])
ax.xaxis.set_major_locator(MultipleLocator(24))
ax.xaxis.set_minor_locator(MultipleLocator(12))
ax.yaxis.set_major_locator(MultipleLocator(5000))

fig.set_size_inches(18.5,10.5)

plt.savefig(outPath)

rootWindow.destroy()
