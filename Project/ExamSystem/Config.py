# -*- coding: utf-8 -*-
# @Time : 2021/1/20 20:23
# @Author : UestcXiye
# @File : Config.py
# @Software: PyCharm

import os

DataPath = '\\' + 'data' + '\\'

STATE_INIT = 1
STATE_SINGLE = 2
STATE_MULTI = 3
STATE_JUDGE = 4
STATE_DONE = 5


def getCurrentPath():
    """ 获取当前路径，找寻用户信息表和题库 """
    path = os.getcwd()  # 当前工作路径
    # path = os.path.abspath('..') #当前工作目录的父目录路径
    return path


def list2str(changList) -> str:
    """ 为tkinter的varString显示处理准备，可以显示考生选择的选项 """
    res = ''
    for index in range(len(changList)):
        res = res + str(changList[index])
    return res


if __name__ == '__main__':
    from pil import Image, ImageTk

    pilImage = Image.open(getCurrentPath() + DataPath + "fail.png")
    img = pilImage.resize((600, 500), Image.ANTIALIAS)
    tkImage = ImageTk.PhotoImage(image=img)
    print(pilImage[0])
