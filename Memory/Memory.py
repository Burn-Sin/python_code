# 导入一些API必须库from win32gui import *
import win32gui,win32process,win32api,ctypes,time


class Memory():
    def __init__(self,windowname):
        # 系统常量，标识最高权限打开一个进程
        PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)  # |位运算， 0x 十六进制
        window = win32gui.FindWindow("MainWindow", windowname)  # 查找窗体
        # 根据窗体抓取进程编号（pid 是进程编号 hid和pid一般描述一个进程信息）
        hid, pid = win32process.GetWindowThreadProcessId(window)
        # phand 打开一个进程（参数意思是使用最高权限非安全打这个进程）
        self.phand = win32api.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        self.date = ctypes.c_long()
        # 调用系统内核模块(Kerne123.dll windows内核)
        self.mydll = ctypes.windll.LoadLibrary("C:\\Windows\\System32\\kernel32.dll")

    def du(self,dizhi):
        # 读取内存(“4”表示占4个字节，types.byref(date)表示转递地址信息，写入的结果到date中)
        # int(phand)打开的进程编号   “244866760”需要读取的内存的地址
        self.mydll.ReadProcessMemory(int(self.phand), dizhi[0], ctypes.byref(self.date), 4, None)
        for i in dizhi[1:]:
            self.mydll.ReadProcessMemory(int(self.phand), self.date.value + i, ctypes.byref(self.date), 4, None)
            # 读内存 （可以获取内存中对应的数据）
        print(self.date.value)


    def xie(self,dizhi,value):
        data2 = ctypes.c_long()
        self.mydll.ReadProcessMemory(int(self.phand), dizhi[0], ctypes.byref(data2), 4, None)
        for i in dizhi[1:-1]:
            self.mydll.ReadProcessMemory(int(self.phand), data2.value+i, ctypes.byref(data2), 4, None)
        self.mydll.WriteProcessMemory(int(self.phand),data2.value+dizhi[-1], ctypes.byref(ctypes.c_long(value)), 4, None)


M = Memory("Plants vs. Zombies")
#M.du([0x00755e0c,0x868,0x5578])
#M.xie([0x00755e0c,0x868,0x5578],1000)