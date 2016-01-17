from win32api import *
from win32gui import *
import win32con
import sys, os
import time,winsound
import pyttsx
import wmi
 
engine=pyttsx.init()
batterythreshold=95
class WindowsBalloonTip:
    def __init__(self, title, msg):
        message_map = {
                win32con.WM_DESTROY: self.OnDestroy,
        }
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map
        classAtom = RegisterClass(wc)
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow( classAtom,  "Taskbar", style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, hinst, None)
        UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join( sys.path[0], "balloontip.ico" ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
            hicon = LoadImage(hinst, iconPathName, \
                    win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
            hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "Notification")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, \
                         (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,\
                          hicon, "Notification",title,200,msg))
        time.sleep(10)
        DestroyWindow(self.hwnd)
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0)
def balloon_tip(title, msg):
    WindowsBalloonTip(msg, title)
    
def checkbattery():
    battery = wmi.WMI().Win32_Battery()[0]
    if battery.EstimatedChargeRemaining<batterythreshold:
        thisbattery=battery.EstimatedChargeRemaining
        winsound.Beep(10000,200)
        balloon_tip('Low Battery Level', str(battery.EstimatedChargeRemaining)+'% remaining! Connect charger')
        #print thisbattery
        time.sleep(180)
        battery1=wmi.WMI().Win32_Battery()[0]
        if battery1.EstimatedChargeRemaining<thisbattery:
            for i in range(1, 5):
                winsound.Beep(i * 100, 200)
            engine.say(str(battery1.EstimatedChargeRemaining)+' % '+'charging remaining. Connect the charger!')
            engine.runAndWait()
            #print battery1.EstimatedChargeRemaining
        return 'NOT OK'
    else:
        return 'OK'

print checkbattery()