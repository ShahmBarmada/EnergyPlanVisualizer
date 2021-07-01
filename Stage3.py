import tkinter, csv
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from typing import Sized
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

window = tkinter.Tk()

window.title('EnergyPlanVisualizer Stage3')
window.geometry('1010x500')

lbl1 = ttk.Label(window, text='Load Study Output .txt or .csv:', font=("Segoe UI",12), anchor='e', width=23)
lbl1.grid(column=0, row=0, padx=10, pady=10)

lbl2 = ttk.Label(window, text='Choose Range (X Axis):', font=("Segoe UI",12), anchor='e', width=23)
lbl2.grid(column=0, row=2, padx=10, pady=10)

lbl3 = ttk.Label(window, text='Choose Field (Y Axis):', font=("Segoe UI",12), anchor='e', width=23)
lbl3.grid(column=0, row=3, padx=10, pady=10)

lbl4 = ttk.Label(window, text='State:', font=("Segoe UI",12), anchor='e', width=23)
lbl4.grid(column=0, row=1, padx=10, pady=10)

loadStateStr = StringVar()
loadStateStr.set('No File Loaded')
loadStateBol = FALSE

lbl5 = ttk.Label(window, textvariable=loadStateStr, font=("Segoe UI",12,'bold'), foreground='red', anchor='c', width=70)
lbl5.grid(column=1, row=1, padx=10, pady=10)

txt1 = ttk.Entry(window, width=72, font=("Segoe UI",12))
txt1.grid(column=1, row=0, padx=10, pady=10)

ttk.Style().configure('TCombobox', justify='left')

comboSelection1 = tkinter.StringVar()
comboField1 = ttk.Combobox(window, width=70, textvariable=comboSelection1, font=("Segoe UI",12), style='TCombobox')
comboField1['values'] = None
comboField1['state'] = 'readonly'
comboField1.grid(column=1, row=2, sticky='w', padx=10, pady=10)
comboField1.current()

comboSelection2 = tkinter.StringVar()
comboField2 = ttk.Combobox(window, width=70, textvariable=comboSelection2, font=("Segoe UI",12), style='TCombobox')
comboField2['values'] = None
comboField2['state'] = 'readonly'
comboField2.grid(column=1, row=3, sticky='w', padx=10, pady=10)
comboField2.current()

def loadFile():
    global inPath, loadStateBol
    inPath = filedialog.askopenfilename()
    txt1.delete(0, END)
    txt1.insert(0, inPath)

    if inPath.endswith('.txt'):
        pass

    elif inPath.endswith('.csv'):
        loadStateStr.set('Study File Loaded')
        loadStateBol = TRUE
        lbl5.configure(foreground='green')
        loadFileCSV()

    else:
        messagebox.showerror('Error','Please choose .txt or .csv file only')

btn1 = ttk.Button(window, text="Load", command=loadFile)
btn1.grid(column=2, row=0, padx=10, pady=10)

def loadFileCSV():
    #global aliasList, headerList, StudyDF
    StudyDF = pd.read_csv(inPath, low_memory=False)
    headerPath = inPath[:inPath.rfind('/')] + '/HeaderDictionary.csv'

    with open(headerPath, 'r') as ipf:
        aliasDict = {rows[0]:rows[1] for rows in csv.reader(ipf)}

    aliasList = list(aliasDict.values())
    comboField2['values'] = aliasList
    headerList = list(aliasDict.keys())

window.mainloop()