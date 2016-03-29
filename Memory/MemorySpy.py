import psutil,time
import Tkinter as tk
exename="w1.exe"
def getpid():
    all_processes = list(psutil.process_iter())
    for p in all_processes:
        try:
            if p.name()==exename:
                w1=p
                return w1
        except Exception as e:
            pass
w1=getpid()
def getMemory():
    if not w1.name()==exename:
        a.configure(text="not exist:"+str(exename))
        w1=getpid()
        root.after(2000,getMemory)
    else:    
        text2=str(float(w1.get_memory_info()[0]/1024.0/1024.0))+'M '+w1.name()
        a.configure(text=text2)
        root.after(1000,getMemory)

root =tk.Tk()
root.wm_attributes('-topmost',1)
root.resizable(False, False)
root.title("Memory")
root.geometry('300x30')
a=tk.Label(root)
a.pack()
getMemory()
root.mainloop()
