# -*- coding: utf-8 -*-
# @Time : 2021/1/20 20:12
# @Author : UestcXiye
# @File : BackEnd.py
# @Software: PyCharm

import pandas as pd
import random
from Config import *


def checkAccount(filename) -> tuple:
    """ 检验用户是否存在，账号密码是否正确 """
    path = getCurrentPath() + DataPath + filename
    fid = open(path, 'r+')
    accountList = []
    userNameList, userPasswordList = [], []
    line = fid.readlines()
    for child in line:
        # print('[Function checkAccount]: ' + child)
        # if not (line.startswith("@")):  # 注释行开头为@
        accountList.append(child.strip("\n").split('\t'))
        # print(accountList)
    for name, password in accountList:
        userNameList.append(name)
        userPasswordList.append(password)
        # print(userNameList)
        # print(userPasswordList)
    fid.close()
    return userNameList, userPasswordList


def addUser(filename, userName: str, userPassword: str) -> int:
    """ 添加新用户，在用户名不重读的情况下才会调用 """
    path = getCurrentPath() + DataPath + filename
    txtfile = open(path, 'a')
    data = '\n' + userName + '\t' + userPassword
    txtfile.write(data)
    txtfile.close()
    return 1


class SingleChoiceSubject:

    def __init__(self):
        self.scorePer = 3  # 每道题的分值
        self.totalNum = 10  # 总共10道单选
        self.subjectList = {}  # 存放所有题目信息
        self.path = getCurrentPath() + DataPath + 'question.xlsx'
        self.df = pd.read_excel(self.path, sheet_name='单选')
        self.tempList = []  # 存储一行信息
        self.randList = []  # 存储已经选用的题目，防止随机题目

    def generateRand(self):
        """ 产生随机题目序号 """
        count = 0
        while count < self.totalNum:
            randCount = random.randint(0, 519)  # 共520道单选题
            if randCount not in self.randList:
                self.randList.append(randCount)
                count = count + 1
            else:
                continue

    def getData(self):
        """ 获取题目，返回数据给前端 """
        self.generateRand()
        count = 0
        for randCount in self.randList:
            # 还有记得，是不是要canvas上面分布这些按钮，然后随着canvas销毁而消失
            self.subjectList[count] = {}
            self.subjectList[count]['题目内容'] = self.df['题目内容'][randCount]
            self.subjectList[count]['A'] = self.df['A'][randCount]
            self.subjectList[count]['B'] = self.df['B'][randCount]
            self.subjectList[count]['C'] = self.df['C'][randCount]
            self.subjectList[count]['D'] = self.df['D'][randCount]
            self.subjectList[count]['参考答案'] = self.df['参考答案'][randCount]
            count = count + 1
        return self.subjectList


class MultiChoiceSubject:

    def __init__(self):
        self.scorePer = 5  # 每道题的分值
        self.totalNum = 10  # 总共10道单选
        self.subjectList = {}  # 存放所有题目信息
        self.path = getCurrentPath() + DataPath + 'question.xlsx'
        self.df = pd.read_excel(self.path, sheet_name='多选')
        self.randList = []

    def generateRand(self):
        """ 产生随机题目序号 """
        count = 0
        while count < self.totalNum:
            randCount = random.randint(0, 265)  # 共520道单选题
            if randCount not in self.randList:
                self.randList.append(randCount)
                count = count + 1
            else:
                continue

    def getData(self):
        """ 获取题目，返回数据给前端 """
        self.generateRand()
        count = 0
        for randCount in self.randList:
            # 还有记得，是不是要canvas上面分布这些按钮，然后随着canvas销毁而消失
            self.subjectList[count] = {}
            self.subjectList[count]['题目内容'] = self.df['题目内容'][randCount]
            self.subjectList[count]['A'] = self.df['A'][randCount]
            self.subjectList[count]['B'] = self.df['B'][randCount]
            self.subjectList[count]['C'] = self.df['C'][randCount]
            self.subjectList[count]['D'] = self.df['D'][randCount]
            self.subjectList[count]['E'] = self.df['E'][randCount]
            self.subjectList[count]['参考答案'] = self.df['参考答案'][randCount]
            count = count + 1
        return self.subjectList


class JudgeSubject:

    def __init__(self):
        self.scorePer = 2  # 每道题的分值
        self.totalNum = 10  # 总共10道单选
        self.subjectList = {}  # 存放所有题目信息
        self.path = getCurrentPath() + DataPath + 'question.xlsx'
        self.df = pd.read_excel(self.path, sheet_name='判断')
        self.randList = []

    def generateRand(self):
        """ 产生随机题目序号 """
        count = 0
        while count < self.totalNum:
            randCount = random.randint(0, 362)  # 共520道单选题
            if randCount not in self.randList:
                self.randList.append(randCount)
                count = count + 1
            else:
                continue

    def getData(self):
        """ 获取题目，返回数据给前端 """
        self.generateRand()
        count = 0
        for randCount in self.randList:
            self.subjectList[count] = {}
            self.subjectList[count]['题目内容'] = self.df['题目内容'][randCount]
            self.subjectList[count]['参考答案'] = self.df['参考答案'][randCount]
            count = count + 1
        return self.subjectList


class BackEnd:
    """ 与前端的数据接口 """

    def __init__(self):
        self.Single = SingleChoiceSubject()
        self.Multi = MultiChoiceSubject()
        self.Judge = JudgeSubject()
        self.SingleList = self.Single.getData()
        self.MultiList = self.Multi.getData()
        self.JudgeList = self.Judge.getData()

    def test(self):
        print("SingleList:", self.SingleList)
        print("MultiList:", self.MultiList)
        print("JudgeList:", self.JudgeList)


if __name__ == '__main__':
    test = BackEnd()
    test.test()
    print(test.SingleList[0]['A'])
    print(test.MultiList[2]['参考答案'])
    print(test.JudgeList[9]['题目内容'])
    print(type(test.MultiList[2]['参考答案']))
    print(test.SingleList[2]['参考答案'])
    if test.SingleList[2]['参考答案'] == 'A':
        print('aaaa')
    if test.SingleList[2]['参考答案'] == 'B':
        print('bb')
    if test.SingleList[2]['参考答案'] == 'C':
        print('cc')
    if test.SingleList[2]['参考答案'] == 'D':
        print('dd')
