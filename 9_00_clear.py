#!/usr/bin/python3
import datetime
import sys
import time

import config as conf
 
from lib.ying_init import *
from lib.ying_quote import *

gq = get_quote(conf)
  

def main(argv):
        while True: 
                d_time = datetime.datetime.strptime(str(datetime.datetime.now().date())+'8:30', '%Y-%m-%d%H:%M')
                d_time1 =  datetime.datetime.strptime(str(datetime.datetime.now().date())+'9:25', '%Y-%m-%d%H:%M')
                n_time = datetime.datetime.now()
                if n_time>d_time and n_time<d_time1:  #判断当前时间是否在 9：10 到 9：25分之间 如果在 则进行清理工作
                        gq.clear_js_quote()     #清理即时行情数据库
                        print("清理  即时行情  数据库") 
                        gq.clear_min_quote()    #清理分时行情数据库
                        print("清理  分时行情  数据库")
                        gq.clear_jaodu()        #清理角度数据库
                        print("清理  角度  数据库")                        
                        gq.clear_gubiaochi()    #清理股票池数据库
                        print("清理  股票池  数据库")
                        print("清理完毕！")
                        return  #数据库清理完毕后退出本程序
                        
                else:
                        print('不在 数据库定时清理 时间内，等待。。。。')
                        time.sleep(30) 

if __name__ == '__main__':
    main(sys.argv)
