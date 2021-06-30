import tkinter, csv
from tkinter import *
from tkinter import ttk, filedialog
import pandas as pd
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

window = tkinter.Tk()
window.title('EnergyPlanVisualizer Stage3')
window.geometry('1010x200')

comboSelection = tkinter.StringVar()
comboField = ttk.Combobox(window, width=40, textvariable=comboSelection)
comboField['values'] = aliasList
comboField.grid(column=0, row=1, padx=10, pady=10)
comboField.current()

window.mainloop()