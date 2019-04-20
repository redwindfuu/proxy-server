from tkinter import *
import webbrowser

def open_webbrowser():
    chrome_path = 'C:/Program Files/Mozilla Firefox/firefox.exe %s'
    webbrowser.get(chrome_path).open(e1.get())

master = Tk()
master.title("Ahihi")
Label(master, text="Enter Website link:").grid(row = 0)

e1 = Entry(master)
e1.grid(row = 0, column = 1)
Button(master, text='Show', command=open_webbrowser).grid(row=3, column=1, sticky=W, pady=4)

master.mainloop()
'''
This is just for fun, openning firefox
'''
