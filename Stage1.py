from tkinter import *
from tkinter import filedialog, messagebox
import subprocess, os

window = Tk()
window.title('EnergyPlanVisualizer Stage1')
window.geometry('1010x200')

lbl1 = Label(window, text="EnergyPlan.exe Path :", font=("Segoe UI",13), anchor='e', width=18)
lbl1.grid(column=0, row=0, padx=10, pady=10)

lbl2 = Label(window, text="Input File Path :", font=("Segoe UI",13), anchor='e', width=18)
lbl2.grid(column=0, row=1, padx=10, pady=10)

lbl3 = Label(window, text="Output Directory Path :", font=("Segoe UI",13), anchor='e', width=18)
lbl3.grid(column=0, row=2, padx=10, pady=10)

txt1 = Entry(window,width=80, font=("Segoe UI",13))
txt1.grid(column=1,row=0, padx=10, pady=10)

txt2 = Entry(window,width=80, font=("Segoe UI",13))
txt2.grid(column=1,row=1, padx=10, pady=10)

txt3 = Entry(window,width=80, font=("Segoe UI",13), )
txt3.grid(column=1,row=2, padx=10, pady=10)

def clicked1():
    path_a = filedialog.askopenfilename()
    txt1.delete(0, END)
    txt1.insert(0, path_a)

def clicked2():
    path_b = filedialog.askopenfilename()
    txt2.delete(0, END)
    txt2.insert(0, path_b)

def clicked3():
    global path_c
    path_c = filedialog.askdirectory()
    txt3.delete(0, END)
    txt3.insert(0, path_c + "/Result.txt")

def clicked4():
    messagebox.showinfo('Info', 'The ouput file will be named Result.txt')
    subprocess.run([str(txt1.get()), "-i", str(txt2.get()), "-ascii", str(txt3.get())])
    subprocess.run(['explorer', os.path.realpath(path_c)])

btn1 = Button(window, text="Select", command=clicked1)
btn1.grid(column=2, row=0, padx=10, pady=10)

btn2 = Button(window, text="Select", command=clicked2)
btn2.grid(column=2, row=1, padx=10, pady=10)

btn3 = Button(window, text="Select", command=clicked3)
btn3.grid(column=2, row=2, padx=10, pady=10)

btn4 = Button(window, text="Execute", command=clicked4)
btn4.grid(column=1, row=3, padx=10, pady=10)

window.mainloop()