import os
from tkinter import *
import tkinter as tk
window=Tk()
window.geometry("850x450")
window.title("Welcome to Pranavi PC Control-Room")
head=Label(window, text="Shutdown, Restart and Logout Using Python by Pranavi T", font=('Times_New_Roman 18'))
head.pack(pady=20)

def Shutdown():
    os.system("shutdown /s /t 0")

def Restart():
    os.system("shutdown /r /t 0")

def logout():
    os.system("shutdown /l /t 0")

Button(window,text='Shutdown',command=Shutdown, font=('normal',20), bg='red').pack()
Button(window,text='Restart',command=Restart,font=('normal',20), bg='yellow').pack()
Button(window,text='Logout',command=logout,font=('normal',20), bg='green').pack()

window.mainloop()
