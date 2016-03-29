import psutil,time
import Tkinter as tk
def getpid():
    all_processes = list(psutil.process_iter())
    for p in all_processes:
        try:
            if p.name()=="w1.exe":
                w1=p
                # print p.name(),p.pid,p.username()
                # print p.get_cpu_percent(interval=0)
                # print p.get_memory_info(),p.get_memory_percent()
                # print p.get_cpu_times()
                return w1
        except Exception as e:
            pass
w1=getpid()
def getMemery():
    text2=str(float(w1.get_memory_info()[0]/1024.0/1024.0))+'M '+w1.name()
    a.configure(text=text2)
    root.after(1000,getMemery)

root =tk.Tk()
root.wm_attributes('-topmost',1)
root.resizable(False, False)
root.title("Memory")
root.geometry('300x30')
a=tk.Label(root)
a.pack()
getMemery()
root.mainloop()
