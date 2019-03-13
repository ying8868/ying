#!/usr/bin/python3
'''
股票异动 监控 守护程序  
'''
import time
import datetime

import sys

import config as conf
import lib.util as u
from lib.ying_init import *
from lib.ying_quote import *
from turtledemo import yinyang

gq=get_quote(conf) 
def main(argv): 
    while True: 
        if  gq.get_js_quote_count()<1: 
            # 判断数据表是否为空 如果为空 则不进行操作
            s=3
            print("股票异动:js_quote 数据库没有数据 %s 秒钟以后 继续查询"%(s))
            time.sleep(s)  
        else:
            #if u.is_opentime()==True:
            d_time = datetime.datetime.strptime(str(datetime.datetime.now().date())+'9:30', '%Y-%m-%d%H:%M')
            d_time1 =  datetime.datetime.strptime(str(datetime.datetime.now().date())+'23:59', '%Y-%m-%d%H:%M')
            n_time = datetime.datetime.now()
            if  n_time>d_time and n_time<d_time1:   
                starttime = datetime.datetime.now()

                qh=quote_hold(conf)
                qh.down_yidong_run() 
                
                #gq.update_gubiaochi(yidong)
                
                #print(gubiaochi.to_json(orient='index'))
 
                endtime = datetime.datetime.now()
                send=endtime-starttime 
                s=3-(send.seconds)
                print("股票异动 监控 %s 秒钟以后 继续下载  当前时间 %s" %(s,datetime.datetime.now()))
                if s>0:
                    time.sleep(s)
            
            else:
                print('股票异动: 监控 不在工作时间内，等待。。。。')
                time.sleep(30)
        #return #测试时加上 正式用时 把它没注释掉
    '''

     if  jaodu_df_find.count()==0 or js_df_find.count()==0: 
        
        s=3
        print("即时行情 或分时行情 数据库没有数据 %s 秒钟以后 继续查询"%(s))
        time.sleep(s) 
        return 
    
    '''
                
def test():
    dq=down_quote(conf)
    #  600651  600651  603958
    dq.down_yidong('600651','1','2019-03-07')
    print('end')

if __name__ == '__main__':
    #test()
    main(sys.argv)