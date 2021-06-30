from tkinter import *
from tkinter import ttk, filedialog
import pandas as pd
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

inPath = filedialog.askopenfilename()
outPath = inPath[:inPath.rfind('/')] + '/test.png'
headerPath = inPath[:inPath.rfind('/')] + '/HeaderDictionary.csv'

StudyDF = pd.read_csv(inPath, low_memory=False)

with open(headerPath, 'r') as ipf:
    aliasDict = {rows[0]:rows[1] for rows in csv.reader(ipf)}

aliasList = list(aliasDict.values())
headerList = list(aliasDict.keys())

plt.close()