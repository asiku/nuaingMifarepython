from Tkinter import *
import subprocess
import os
import requests
import thread

def starServ():
    cwd = os.getcwd()
    p = subprocess.Popen("python "+cwd+"/tesFlask.py", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    print "Today is", output

def stopServ():
    r = requests.post("http://127.0.0.1:5000/shutdown")
    print r

win = Frame()
win.pack()
Label(win, text='Presensi Service').pack(side=TOP)
Button(win, text='Star Server', command=starServ).pack(side=LEFT)
Button(win, text='Quit Server', command=stopServ).pack(side=RIGHT)
win.mainloop()