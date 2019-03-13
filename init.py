#!/usr/bin/python3 
import sys
from  lib.ying_init import *
from  lib.ying_quote import *
import config as conf


def Version():
    print (' 初始化股票基础代码库程序 1.0.0.0.1')

def main(argv):  
    '''
    本程序只能执行一次 初始化 其它时间用 更新 或者同步
    '''
    yi= init(conf) 
    yi.run_init()
    #yi.run_update()


if __name__ == '__main__':
    main(sys.argv)