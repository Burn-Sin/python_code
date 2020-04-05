import time,pyhk,keybd,threading
from pymouse import PyMouse
flage = 0
def fun():
    global flage
    if (flage == 0):
        print('open')
        flage = 1
        T1 = threading.Thread(target=s1)
        T2 = threading.Thread(target=timec,args=(20,))
        T3 = threading.Thread(target=mousemove)
        T1.start()
        T2.start()
        T3.start()

    else:
        print('closs')
        flage = 0

def s1():
    global flage
    time.sleep(0.2)
    keybd.key_press('1')
    while flage==1:
        time.sleep(0.65)
        keybd.key_press('0')
        if (flage==0):
            break

def mousemove():
    global flage
    M = PyMouse()
    time.sleep(1)
    while flage == 1:
        time.sleep(0.02)
        a = M.position()
        M.click(x=a[0],y=a[1],n=1)
        if (flage==0):
            break


def timec(t):
    global flage
    time.sleep(t)
    flage = 0
    pass

def exit():
    pass
if __name__ == '__main__':

    hot = pyhk.pyhk()
    hot.addHotkey(['mouse left','4'], fun)
    hot.addHotkey(['4'], fun)
    hot.addHotkey(['Ctrl','1'], exit)
    hot.start()