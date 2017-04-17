#coding:cp936
import psutil,time
import Tkinter as tk
#memory
EXE_PROCESS_NAME="w1.exe"
def get_pid():
    all_processes = list(psutil.process_iter())
    for p in all_processes:
        try:
            if p.name()==EXE_PROCESS_NAME:
                w1=p
                # print p.name(),p.pid,p.username()
                # print p.get_cpu_percent(interval=0)
                #print type(p.get_memory_info()),p.get_memory_percent()
                # print p.get_cpu_times()
                return w1
        except Exception as e:
            pass

def get_memory():
    try:
        w1=get_pid()
        if not w1.name()==EXE_PROCESS_NAME:
            a.configure(text="not exist:"+str(EXE_PROCESS_NAME))
            w1=get_pid()
            root.after(2000,get_memory)
        else:
            text2=str(w1.memory_info()[0]/1024.0/1024.0)+'M '+w1.name()
            a.configure(text=text2)
            root.after(1000,get_memory)
    except Exception:
        a.configure(text="not exist:"+str(EXE_PROCESS_NAME))
        #w1=getpid()
        root.after(2000,get_memory)
if __name__=="__main__":
    root =tk.Tk()
    root.wm_attributes('-topmost',1)
    root.resizable(False, False)
    root.title(u"w1进程内存")
    root.geometry('230x30')
    a=tk.Label(root)
    a.pack()
    get_memory()
    root.mainloop()
