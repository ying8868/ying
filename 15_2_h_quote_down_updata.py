'''
 日K线行情下载或者更新程序 采用多线程的方式进行下载
'''

#!/usr/bin/python3 
import sys

import config as conf
from lib.ying_init import *
from lib.ying_quote import *

def Version():
    print ('日K线行情下载或者更新程序 1.0.0.0.1')

def main(argv):  
    '''
    历史 日K线行情下载或者更新程序 采用多线程的方式进行下载
    '''
    print('开始运行日K线下载程序。')
    qh =quote_hold(conf)
    qh.H_quote_down_run()
    
    #yi= east_core( ) 
   # yi.get_H_quote('300616') 

    #yi.run_update() 
def test():
    dq=down_quote(conf)
    dq.down_H_daily('601212')
    
if __name__ == '__main__':
    
    #test()
    main(sys.argv)
