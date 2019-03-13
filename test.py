#!/usr/bin/python3 
'''
即时行情守护程序  
'''
import time
import datetime

import sys
import config as conf
import lib.util as u
from lib.ying_init import *
from lib.ying_quote import *


def Version():
    print('即时行情守护程序 ')


def main(argv):
    '''
    即时行情程序每天早上9:30开启。
    即时行情守护程序 采用多线程的方式进行下载
    '''
    while True:
        d_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '9:30', '%Y-%m-%d%H:%M')
        d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '23:55', '%Y-%m-%d%H:%M')
        n_time = datetime.datetime.now()
        if n_time > d_time and n_time < d_time1:
            starttime = datetime.datetime.now()
            qh = quote_hold(conf)
            qh.js_quote_down()
            endtime = datetime.datetime.now()
            send = endtime - starttime
            s = 20 - (send.seconds)
            print("即时行情 守护%s 秒钟以后 继续开始 当前时间 %s" % (s, datetime.datetime.now()))
            if s > 0:
                time.sleep(s)
        else:
            print('即时行情 守护 不在时间段内 请等待。。。。')
            time.sleep(10)

            # return


if __name__ == '__main__':
    main(sys.argv)
