#coding:cp936
import Tkinter as tk
import tkMessageBox
from PIL import ImageGrab
import time,os,ctypes
#print os.getcwd()
#os.chdir("D:\python_code\mywork\WA55")
def windowCapture():
    try:
        dll=ctypes.cdll.LoadLibrary('PrScrn.dll')
    except Exception:
        tkMessageBox.showinfo(title='error',message="can't find PrScrn.dll!")
        exit(0)
    else:
        try:
            dll.PrScrn(0)
        except:
            tkMessageBox.showinfo(title='error',message="Sth wrong in capture!")
            exit(0)
def Capture():
    try:
        dll = ctypes.cdll.LoadLibrary('CameraDll.dll')
    except Exception:
        tkMessageBox.showinfo(title='error',message="can't find CameraDll.dll!")
        exit(0)
    else:
        try:
            dll.CameraSubArea(0)
        except Exception as e:
            return

def savepic():
    if getpath():
        addr_path=getpath()
    else:
        tkMessageBox.showinfo(title='without path',message="without path!pic will save to \"E:\\1\"")
        var.set("E:\\1")
        addr_path=getpath()

    if not os.path.exists(addr_path):
        os.makedirs(addr_path)

    examtime=time.strftime("%Y%m%d%H%M%S",time.localtime())
    addr=os.path.normcase(addr_path+"\\"+examtime+".jpeg")
    im = ImageGrab.grab()
    im.save(addr,'jpeg')
    tkMessageBox.showinfo(title='done',message="pic save done!")

def getpath():
    filepath=var.get()
    return filepath

root =tk.Tk()
root.wm_attributes('-topmost',1)
root.title("GrabWA55")
root.geometry('200x300')

pathLable=tk.Label(root,text=u'��ͼ·��:')
pathLable.pack()

var=tk.StringVar()
e=tk.Entry(root,textvariable=var)
var.set("E:\\1")
e.pack()

tk.Button(root, width=10,heigh=4,fg="blue",text="Save", command = savepic).pack()
tk.Button(root, width=10,heigh=4,fg="blue",text="Winodow\nCapture", command = windowCapture).pack()
tk.Button(root, width=10,heigh=4,fg="blue",text="Capture", command = Capture).pack()
root.mainloop()