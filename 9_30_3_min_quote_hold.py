'''
行情守护程序 采用多线程的方式进行下载
'''
import time
import datetime
#!/usr/bin/python3 
import sys

import config as conf
import lib.util as u
 
from lib.ying_quote import *

gq = get_quote(conf)
 
def main(argv):  
    '''
    此分时行情程序每天早上9点31分钟开启。
    分时行情守护程序 采用多线程的方式进行下载
    ''' 
    while True:
         
        #print(gq.get_js_quote_count())
         
        if  gq.get_jaodu_count()==0: 
            # 判断数据表是否为空 如果为空 则不进行操作
            s=3
            print("分时守护:即时行情数据库不存在数据 %s 秒钟以后 继续查询 当前时间 %s" %(s,datetime.datetime.now()))
            time.sleep(s) 
        else:
            d_time = datetime.datetime.strptime(str(datetime.datetime.now().date())+'9:30', '%Y-%m-%d%H:%M')
            d_time1 =  datetime.datetime.strptime(str(datetime.datetime.now().date())+'23:00', '%Y-%m-%d%H:%M')
            n_time = datetime.datetime.now()
            if n_time>d_time and n_time<d_time1:
                starttime = datetime.datetime.now()
                qh =quote_hold(conf)
                qh.quote_down_run()
                endtime = datetime.datetime.now()
                send=endtime-starttime 
                s=20-(send.seconds)
                print("分时守护:分时行情%s 秒钟以后 继续下载 当前时间 %s" %(s,datetime.datetime.now()))
                if s>1:
                    time.sleep(s)
            
            else:
                print('分时守护:分时行情  不在工作时间内，等待。。。。')
                time.sleep(30)
        #return #测试时加上 正式用时 把它没注释掉
         
        
def test():
    qh =quote_hold(conf)
    qh.quote_down_run() 
    print('end')
    
    
if __name__ == '__main__':
    #test()
    main(sys.argv)
