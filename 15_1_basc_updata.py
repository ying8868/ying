#!/usr/bin/python3 
import sys
from  lib.ying_init import *
from  lib.ying_quote import *
import config as conf


def Version():
    print ('更新股票基础代码库 1.0.0.0.1')

def main(argv):  
    '''
    更新 请用 此方法
    '''
    yi= init(conf) 
    #yi.run_init()
    yi.run_update()


if __name__ == '__main__':
    main(sys.argv)