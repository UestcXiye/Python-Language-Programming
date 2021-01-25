# -*- coding: utf-8 -*-
# @Time : 2021/1/20 21:01
# @Author : UestcXiye
# @File : ProjectTree.py
# @Software: PyCharm

from pathlib import Path

tree_str = ''


def generate_tree(pathname, n=0):
    """ 产生项目结构树图 """
    global tree_str
    if pathname.is_file():
        tree_str += '    |' * n + '-' * 4 + pathname.name + '\n'
    elif pathname.is_dir():
        tree_str += '    |' * n + '-' * 4 + \
                    str(pathname.relative_to(pathname.parent)) + '\\' + '\n'
        for cp in pathname.iterdir():
            generate_tree(cp, n + 1)


if __name__ == '__main__':
    generate_tree(Path.cwd())
    print(tree_str)
