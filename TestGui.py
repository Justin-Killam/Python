
import tkinter as tk

win=tk.Tk()
    
#size variables
wH=600
wW=400
sH=win.winfo_screenheight()
sW=win.winfo_screenwidth()
cX=int((sW-wW)/2)
cY=int((sH-wH)/2)

#Formatting
win.title("Arduino")
win.geometry(f"{wW}x{wH}+{cX}+{cY}")
win.resizable(False,False)

#Text entry
DbgEntry = tk.Entry(width=10)
DbgEntry.place(x=20,y=40)

i=0
def Custom_Loop():
    global i
    DbgEntry.delete(0,10000)
    DbgEntry.insert(0,str(i))
    win.after(1000,Custom_Loop)
    i=i+1
win.after(1000,Custom_Loop)
win.mainloop()