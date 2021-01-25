# -*- coding: utf-8 -*-
# @Time : 2021/1/20 18:34
# @Author : UestcXiye
# @File : AntiCheating.py
# @Software: PyCharm

import os
import time
import tkinter
import threading
import ctypes
import psutil

root = tkinter.Tk()

root.title('防作弊演示')

# 窗口初始大小和位置
root.geometry('250x80+300+100')

# 不允许改变窗口大小
root.resizable(False, False)

ban = tkinter.IntVar(root, 0)


def funcBan():
    while ban.get() == 1:
        # 强行关闭主流文本编辑器和网页浏览器
        for pid in psutil.pids():
            try:
                p = psutil.Process(pid)
                exeName = os.path.basename(p.exe()).lower()
                if exeName in ('notepad.exe', 'winword.exe', 'wps.exe', 'wordpad.exe', 'iexplore.exe',
                               'chrome.exe', 'qqbrowser.exe', '360chrome.exe', '360se.exe',
                               'sogouexplorer.exe', 'firefox.exe', 'opera.exe', 'maxthon.exe',
                               'netscape.exe', 'baidubrowser.exe', '2345Explorer.exe'):
                    p.kill()
            except:
                pass

        # 清空系统剪切板
        ctypes.windll.user32.OpenClipboard(None)
        ctypes.windll.user32.EmptyClipboard()
        ctypes.windll.user32.CloseClipboard()
        time.sleep(1)


def start():
    ban.set(1)
    t = threading.Thread(target=funcBan)
    t.start()


buttonStart = tkinter.Button(root, text='开始考试', command=start)
buttonStart.place(x=20, y=10, width=100, height=20)


def stop():
    ban.set(0)


buttonStop = tkinter.Button(root, text='结束考试', command=stop)
buttonStop.place(x=130, y=10, width=100, height=20)
# 模拟用，开启考试模式以后，所有内容都不再允许复制
entryMessage = tkinter.Entry(root)
entryMessage.place(x=10, y=40, width=230, height=20)
root.mainloop()
