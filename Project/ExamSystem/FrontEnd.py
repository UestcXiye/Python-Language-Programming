# -*- coding: utf-8 -*-
# @Time : 2021/1/20 19:55
# @Author : UestcXiye
# @File : FrontEnd.py
# @Software: PyCharm

import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from threading import Timer
from playsound import playsound
from BackEnd import BackEnd, checkAccount, addUser
from Config import *
from pil import Image, ImageTk

dataList = BackEnd()  # 存储得到的考题

for i in range(5):
    print(dataList.SingleList[i]['参考答案'])
im = []  # 读取文件
img = []  # 转换格式后

for i in range(5):  # 初始化读取的图片列表
    im.append(None)
    img.append(None)


class FrontEnd:
    """ 前端类，完成注册和答题两个界面和数据调用 """

    def __init__(self):
        self.state = STATE_INIT  # 有限状态机，完成题目衔接和变化
        self.count = 0  # 计数到第几道题了
        self.minute = 60
        self.second = 0  # 设定考试时间60min
        self.ans = []  # 存放考生的结果，确认后判断
        self.score = 0  # 分数
        self.loginWindow = tk.Tk()
        self.initialLoginWindow(self.loginWindow)

    def initialLoginWindow(self, loginWindow):
        """for login"""
        loginWindow['bg'] = 'skyblue'  # background color
        loginWindow.title('考试系统登陆界面')
        loginWindow.resizable(width=True, height=True)

        width = loginWindow.winfo_screenwidth()
        height = loginWindow.winfo_screenheight()
        loginWindow.geometry(
            "400x200+%d+%d" %
            (width / 2 - 200, height / 2 - 200))

        self.varAccount = tk.StringVar()
        self.varAccount.set('')
        self.varKey = tk.StringVar()
        self.varKey.set('')

        # 创建标签
        self.labelAccount = tk.Label(
            loginWindow,
            text='用户名:',
            justify=tk.RIGHT,
            width=80)
        self.labelKey = tk.Label(
            loginWindow,
            text='密  码:',
            justify=tk.RIGHT,
            width=80)
        self.labelRegister = tk.Label(
            loginWindow, text='注  册', justify=tk.RIGHT, width=80)

        # 将标签放到窗口上
        self.labelAccount.place(x=20, y=10, width=160, height=40)
        self.labelKey.place(x=20, y=60, width=160, height=40)

        # 创建账号文本框，同时设置关联的变量
        self.account = tk.Entry(
            loginWindow,
            width=80,
            textvariable=self.varAccount)
        self.account.place(x=200, y=10, width=160, height=40)
        # 创建密码文本框
        self.key = tk.Entry(
            loginWindow,
            show='*',
            width=80,
            textvariable=self.varKey)
        self.key.place(x=200, y=60, width=160, height=40)

        # 创建按钮组件，同时设置按钮事件处理函数
        buttonOk = tk.Button(loginWindow, text='登录', command=self.login)
        buttonOk.place(x=20, y=140, width=100, height=40)
        buttonCancel = tk.Button(
            loginWindow,
            text='取消',
            command=self.cancelLogin)
        buttonCancel.place(x=140, y=140, width=100, height=40)
        buttonRegister = tk.Button(loginWindow, text='注册', command=self.regist)
        buttonRegister.place(x=260, y=140, width=100, height=40)

        # make Esc exit the program
        loginWindow.bind('<Escape>', lambda e: loginWindow.destroy())
        # 启动消息循环
        loginWindow.mainloop()

    def login(self):
        """ 获取用户名和密码 """
        name = self.account.get()
        passwd = self.key.get()

        nameList, passwordList = checkAccount('account_file.txt')
        # for test
        for i in range(len(nameList)):
            if name == nameList[i]:
                if passwd == passwordList[i]:
                    tk.messagebox.showinfo(title='提示', message='登录成功！')
                    self.loginWindow.destroy()
                    self.mainWindow = tk.Tk()
                    self.initialMainWindow(self.mainWindow)
                    return
        tk.messagebox.showerror('Python tk', message='账号或密码错误！')

    def cancelLogin(self):
        """ 清空用户输入的用户名和密码 """
        self.varAccount.set('')
        self.varKey.set('')

    def regist(self):
        name = self.account.get()
        passwd = self.key.get()
        userNameList, userPasswordList = checkAccount('account_file.txt')
        if not userNameList or not userPasswordList:
            addUser('account_file.txt', name, passwd)
            return
        for userName in userNameList:
            if name == userName:
                tk.messagebox.showerror('Python tk', message='已有该用户名！')
        registerSuccessful = addUser('account_file.txt', name, passwd)
        if registerSuccessful:
            messagebox.showinfo('提示信息', message='注册成功！')

    def initialMainWindow(self, mainWindow):
        """ initialize window and the window settings"""
        self.width = mainWindow.winfo_screenwidth()
        self.height = mainWindow.winfo_screenheight()

        print('[Function: initialMainWindow]')
        mainWindow.geometry("%dx%d" % (self.width, self.height))
        mainWindow['bg'] = 'skyblue'  # background color
        mainWindow.title('考试系统答题界面')
        mainWindow.resizable(width=True, height=True)

        mainWindow.protocol('WM_DELETE_WINDOW', self.closeMainWindow)
        self.setMenu(mainWindow)
        # make Esc exit the program
        mainWindow.bind('<Escape>', lambda e: mainWindow.destroy())

        self.totalCount = dataList.Single.totalNum + \
                          dataList.Multi.totalNum + dataList.Judge.totalNum

        self.showInitFsm()
        self.watchDog()
        mainWindow.mainloop()

    def showInitFsm(self):
        nextState = STATE_SINGLE
        print('[Function: Init_fsm] startup')

        self.varScore = tk.StringVar()  # 已获得分数
        self.varScore.set(str(self.score) + '\100')
        self.showScoreName = tk.Label(self.mainWindow,
                                      text='已获得分数： ',
                                      width=150,  # 设置label的宽度：30
                                      height=50,  # 设置label的高度：10
                                      justify='left',  # 设置文本对齐方式：左对齐
                                      anchor='nw',  # 设置文本在label的方位：西北方位
                                      font=('微软雅黑', 18),  # 设置字体：微软雅黑，字号：18
                                      fg='white',  # 设置前景色：白色
                                      bg='grey',  # 设置背景色：灰色
                                      )
        self.showScoreName.place(x=10, y=10, width=150, height=50)
        self.showScore = tk.Label(self.mainWindow, textvariable=self.varScore)
        self.showScore.place(x=10, y=70, width=150, height=50)
        self.varTimeLft = tk.StringVar()
        # self.varTimeLft.set(str(min) + '分' + str(sec) + '秒')
        self.timeLeft = tk.Label(self.mainWindow, textvariable=self.varTimeLft)
        self.timeLeft.place(x=self.width - 200, y=70, width=150, height=50)

        # 剩余时间见函数 watchDog
        # self.watchDog(10, 00)  # 考试时间10min

        self.showTimeLeft = tk.Label(self.mainWindow, text='剩余时间',  # 设置文本内容
                                     width=150,  # 设置label的宽度：30
                                     height=50,  # 设置label的高度：10
                                     justify='left',  # 设置文本对齐方式：左对齐
                                     anchor='ne',  # 设置文本在label的方位：西北方位
                                     font=('微软雅黑', 18),  # 设置字体：微软雅黑，字号：18
                                     fg='white',  # 设置前景色：白色
                                     bg='grey',  # 设置背景色：灰色
                                     padx=20,  # 设置x方向内边距：20
                                     pady=10)  # 设置y方向内边距：10
        self.showTimeLeft.place(x=self.width - 200, y=10, width=150, height=60)

        self.varButtonA = tk.StringVar()
        self.varButtonA.set(
            'A. ' + str(dataList.SingleList[self.count % 10]['A']))
        self.varButtonB = tk.StringVar()
        self.varButtonB.set(
            'B. ' + str(dataList.SingleList[self.count % 10]['B']))
        self.varButtonC = tk.StringVar()
        self.varButtonC.set(
            'C. ' + str(dataList.SingleList[self.count % 10]['C']))
        self.varButtonD = tk.StringVar()
        self.varButtonD.set(
            'D. ' + str(dataList.SingleList[self.count % 10]['D']))
        self.varButtonE = tk.StringVar()
        self.varButtonE.set('')

        self.buttonA = tk.Button(self.mainWindow,
                                 textvariable=self.varButtonA,
                                 command=self.buttonAFsm)
        self.buttonB = tk.Button(self.mainWindow,
                                 textvariable=self.varButtonB,
                                 command=self.buttonBFsm)
        self.buttonC = tk.Button(self.mainWindow,
                                 textvariable=self.varButtonC,
                                 command=self.buttonCFsm)
        self.buttonD = tk.Button(self.mainWindow,
                                 textvariable=self.varButtonD,
                                 command=self.buttonDFsm)
        self.buttonOK = tk.Button(self.mainWindow,
                                  text='确认',
                                  command=self.buttonOKFsm)  # 确认按钮，确认不再更改答案
        self.buttonA.place(x=100, y=400, width=750, height=50)
        self.buttonB.place(x=100, y=500, width=750, height=50)
        self.buttonC.place(x=100, y=600, width=750, height=50)
        self.buttonD.place(x=100, y=700, width=750, height=50)
        self.buttonOK.place(x=1000, y=400, width=300, height=50)

        self.varChoice = tk.StringVar()
        self.varChoice.set(list2str(self.ans))  # 显示考生选择的选项
        self.showChoice = tk.Label(
            self.mainWindow, textvariable=self.varChoice)
        self.showChoice.place(x=1000, y=600, width=150, height=50)
        self.subject = scrolledtext.ScrolledText(
            self.mainWindow, relief="solid")
        self.subject.place(x=self.width / 3, y=10)
        self.subject.insert('end', str(self.count + 1) + '. ' +
                            dataList.SingleList[self.count]['题目内容'] + '\n')

        self.count = 0
        print('[Function: Init_fsm] complicated')
        self.state = nextState

    def buttonAFsm(self):
        print('     [Event: buttonA clicked]')
        if self.state == STATE_SINGLE:  # 单选
            self.ans = []
            self.ans.append('A')
        elif self.state == STATE_MULTI:  # 多选
            if 'A' not in self.ans:
                self.ans.append('A')
                self.ans = sorted(self.ans)
            else:
                self.ans.remove('A')
        else:  # 判断题
            self.ans = []
            self.ans.append('对')
        self.varChoice.set(list2str(self.ans))

    def buttonBFsm(self):
        print('     [Event: buttonB clicked]')
        if self.state == STATE_SINGLE:  # 单选
            self.ans = []
            self.ans.append('B')
        elif self.state == STATE_MULTI:  # 多选
            if 'B' not in self.ans:
                self.ans.append('B')
                self.ans = sorted(self.ans)
            else:
                self.ans.remove('B')
                sorted(self.ans)
        else:
            self.ans = []
            self.ans.append('对')
        self.varChoice.set(list2str(self.ans))

    def buttonCFsm(self):
        print('     [Event: buttonC clicked]')
        if self.state == STATE_SINGLE:  # 单选
            self.ans = []
            self.ans.append('C')
        elif self.state == STATE_MULTI:  # 多选
            if 'C' not in self.ans:
                self.ans.append('C')
                self.ans = sorted(self.ans)
            else:
                self.ans.remove('C')
                sorted(self.ans)
        else:  # 判断
            self.ans = []
            self.ans.append('错')
        self.varChoice.set(list2str(self.ans))

    def buttonDFsm(self):
        print('     [Event: buttonD clicked]')
        if self.state == STATE_SINGLE:  # 单选
            self.ans = []
            self.ans.append('D')
        elif self.state == STATE_MULTI:  # 多选
            if 'D' not in self.ans:
                self.ans.append('D')
                self.ans = sorted(self.ans)
            else:
                self.ans.remove('D')
                sorted(self.ans)
        else:  # 判断
            self.ans = []
            self.ans.append('错')
        self.varChoice.set(list2str(self.ans))

    def buttonEFsm(self):
        print('     [Event: buttonE clicked]')
        if self.state == STATE_SINGLE:  # 单选
            self.ans = []
            self.ans.append('E')
        elif self.state == STATE_MULTI:  # 多选
            if 'E' not in self.ans:
                self.ans.append('E')
                self.ans = sorted(self.ans)
            else:
                self.ans.remove('E')
                sorted(self.ans)
        else:  # 判断
            self.ans = []
            self.ans.append('错')
        self.varChoice.set(list2str(self.ans))

    def buttonOKFsm(self):
        """ 确认按钮，点击后进入下一状态 """
        print('     [Event: buttonOK clicked]')

        self.score += self.checkAns()
        self.varScore.set(str(self.score) + '/100')  # 显示得分

        self.count = self.count + 1  # 下一题
        self.varChoice.set('')  # 清空显示的考生选项，准备下一题

        self.ans = []  # 清空内部存储的考生选项，准备下一题
        if self.state == STATE_SINGLE:
            self.showSingleFsm()
        elif self.state == STATE_MULTI:
            self.showMultiFsm()
        elif self.state == STATE_JUDGE:
            self.showJudgeFsm()
        else:  # 结束，分数不再变动
            self.showDoneFsm()

    def checkAns(self) -> int:
        """ 检查结果，返回本题得分 """
        if self.state == STATE_SINGLE:
            print('     [Debug: your choice:] ' + str(self.ans))
            if list2str(
                    self.ans) == dataList.SingleList[self.count % 10]['参考答案']:
                # self.score = self.score + 3  # 本题得分
                return 3
            else:
                return 0
        elif self.state == STATE_MULTI:
            print('     [Debug: your choice:] ' + str(self.ans))
            if list2str(
                    self.ans) == dataList.MultiList[self.count % 10]['参考答案']:
                # self.score += 5  # 本题得分
                return 5
            else:
                return 0
        else:
            print('     [Debug: your choice:] ' + str(self.ans))
            if list2str(
                    self.ans) == dataList.JudgeList[self.count % 10]['参考答案']:
                # self.score += 2  # 本题得分
                return 2
            else:
                return 0

    def updateSubject(self, listName):
        self.subject.delete(0.0, tk.END)
        self.subject.insert('end', str(self.count + 1) + '. ' +
                            listName[self.count % 10]['题目内容'] + '\n')
        self.varButtonA.set(
            'A. ' + str(listName[self.count % 10]['A']))
        self.varButtonB.set(
            'B. ' + str(listName[self.count % 10]['B']))
        self.varButtonC.set(
            'C. ' + str(listName[self.count % 10]['C']))
        self.varButtonD.set(
            'D. ' + str(listName[self.count % 10]['D']))
        if self.state == STATE_MULTI:
            self.varButtonE.set(
                'E. ' + str(listName[self.count % 10]['E']))

    def showSingleFsm(self):
        if self.count < self.totalCount / 3 - 1:
            nextState = STATE_SINGLE
        else:
            nextState = STATE_MULTI
            self.buttonE = tk.Button(self.mainWindow,
                                     textvariable=self.varButtonE,
                                     command=self.buttonEFsm)
            self.buttonA.place(x=100, y=400, width=750, height=50)
            self.buttonB.place(x=100, y=480, width=750, height=50)
            self.buttonC.place(x=100, y=560, width=750, height=50)
            self.buttonD.place(x=100, y=640, width=750, height=50)
            self.buttonE.place(x=100, y=720, width=750, height=50)

        self.updateSubject(dataList.SingleList)

        self.state = nextState

    def showMultiFsm(self):
        if self.totalCount / 3 <= self.count < 2 * self.totalCount / 3:
            nextState = STATE_MULTI
        else:
            nextState = STATE_JUDGE
            self.buttonA.destroy()
            self.buttonB.destroy()
            self.buttonC.destroy()
            self.buttonD.destroy()
            self.buttonE.destroy()
            self.buttonTrue = tk.Button(self.mainWindow,
                                        text='对',
                                        command=self.buttonAFsm)
            self.buttonFalse = tk.Button(self.mainWindow,
                                         text='错',
                                         command=self.buttonEFsm)
            self.buttonTrue.place(x=100, y=400, width=750, height=50)
            self.buttonFalse.place(x=100, y=600, width=750, height=50)

        self.updateSubject(dataList.MultiList)  # 刷新题目和选项

        self.state = nextState

    def showJudgeFsm(self):
        print('total count: ', self.totalCount)
        if self.count < self.totalCount:
            nextState = STATE_JUDGE
        else:
            nextState = STATE_DONE

        self.subject.delete(0.0, tk.END)  # 清空上一题
        self.subject.insert('end', str(self.count + 1) + '. ' +
                            dataList.JudgeList[self.count % 10]['题目内容'] + '\n')

        self.state = nextState

    def showDoneFsm(self):
        """ 结束状态 """

        # 清除所有无用控件
        self.buttonTrue.destroy()
        self.buttonFalse.destroy()
        self.buttonOK.destroy()
        self.showChoice.destroy()
        self.subject.destroy()

        # 播放音乐
        playsound(getCurrentPath() + DataPath + 'music.mp3', block=False)

        # 计时结束，清零
        self.timeCount.cancel()
        # self.varTimeLft.set('0:00')
        self.showScoreName = tk.Label(self.mainWindow,
                                      text='最终得分: ',
                                      width=150,  # 设置label的宽度：30
                                      height=50,  # 设置label的高度：10
                                      justify='left',  # 设置文本对齐方式：左对齐
                                      anchor='nw',  # 设置文本在label的方位：西北方位
                                      font=('微软雅黑', 18),  # 设置字体：微软雅黑，字号：18
                                      fg='white',  # 设置前景色：白色
                                      bg='grey',  # 设置背景色：灰色
                                      )
        self.showScoreName.place(x=10, y=10, width=150, height=50)
        # 加载图像
        global im
        global img

        if self.score < 60:
            im[0] = Image.open(getCurrentPath() + DataPath + "fail.png")
            img[0] = ImageTk.PhotoImage(im[0])
            imLabel = tk.Label(self.mainWindow, image=img[0]).pack()
        elif 60 <= self.score <= 85:
            im[1] = Image.open(getCurrentPath() + DataPath + "pass.png")
            img[1] = ImageTk.PhotoImage(im[1])
            imLabel = tk.Label(self.mainWindow, image=img[1]).pack()
        else:
            im[2] = Image.open(getCurrentPath() + DataPath + "great.png")
            img[2] = ImageTk.PhotoImage(im[2])
            imLabel = tk.Label(self.mainWindow, image=img[2]).pack()

    def setMenu(self, window):
        """create a menu bar with Exit command and version info"""
        menubar = tk.Menu(window)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=window.destroy)
        infoMenu = tk.Menu(menubar, tearoff=0)
        infoMenu.add_command(label="Version Info", command=self.menuInfo)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Info", menu=infoMenu)
        window.config(menu=menubar)

    def menuInfo(self):
        messagebox.showinfo(
            'info',
            'Created By UestcXiye \n version 1.0')

    def watchDog(self):
        """ 定时程序，考试时间最多一小时，结束终止答题，显示分数，播放音乐 """
        timeLeft = 60 * self.minute + self.second
        timeLeft -= 1
        self.second = self.second - 1
        if self.second < 0:
            self.minute = self.minute - 1
            self.second = 59
        if self.minute < 0 or timeLeft == 0:
            self.state = STATE_DONE
            playsound(
                getCurrentPath() + DataPath + 'music.mp3',
                block=False
            )  # 倒计时结束，播放提示音乐。
            self.showDoneFsm()
        self.varTimeLft.set(str(self.minute) + ':' + str(self.second))
        self.timeCount = Timer(1, self.watchDog, ())
        self.timeCount.start()  # 计时器启动

    def closeMainWindow(self):
        """ to check if you really wanna exit """
        ans = messagebox.askyesno(title='Quit', message='要关闭窗口吗？您所做的修改不会保存')
        if ans:
            self.mainWindow.destroy()
        else:
            pass


if __name__ == '__main__':
    test = FrontEnd()
