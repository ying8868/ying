#!/usr/bin/python3
'''
股票池推荐 守护程序  
'''
import time
import datetime 

import sys
import pandas as pd
import config as conf
import lib.util as u
from lib.ying_init import *
from lib.ying_quote import *

gq = get_quote(conf) 

#显示所有列
pd.set_option('display.max_columns', 500)

def tcData(): 
    js_df = pd.DataFrame(list(gq.get_all_js_quote()))
    js_df.drop('_id',axis=1,inplace=True)
    #print(js_df)

    jaodu_df = pd.DataFrame(list(gq.get_all_jaodu())) 
    jaodu_df.drop('_id',axis=1,inplace=True)
    #print(jaodu_df)
    y_yd_df = pd.DataFrame(list(gq.get_y_yidong()))[['code','yd_y_d_count','yd_y_k_count']]
     
   
    #print(y_yd_df)
    hf = u.get_sh_sz()
    
    js_df_sh = js_df[js_df['sc'] == 1]
    js_df_sh['ss'] = hf.iloc[0, 5][0:-1]
    js_df_sz = js_df[js_df['sc'] == 2]
    js_df_sz['ss'] = hf.iloc[1, 5][0:-1]
    
    js_df = pd.concat([js_df_sh, js_df_sz], axis=0)  # 对行操作，相当于水平连接 

    #js_df = pd.concat([jaodu_df, js_df], axis=1 ,join='inner') 
    js_df=pd.merge(js_df,jaodu_df) 
    js_df=pd.merge(js_df,y_yd_df) 
    #js_df = js_df.reset_index(drop=True) 
    #print(js_df) 
    
    '''此处加入 filter 进行过滤 '''
    yf = ying_filter()
    df = yf.gubiaochi_filter(js_df)
    
    #print(len(df))
    return df


def main(argv): 
    while True: 
        if  gq.get_js_quote_count()==0 or gq.get_jaodu_count()==0: 
            # 判断数据表是否为空 如果为空 则不进行操作
            s=3
            print("股票池:即时行情 或分时行情 数据库没有数据 %s 秒钟以后 继续查询"%(s))
            time.sleep(s)  
        else:
            d_time = datetime.datetime.strptime(str(datetime.datetime.now().date())+'9:30', '%Y-%m-%d%H:%M')
            d_time1 =  datetime.datetime.strptime(str(datetime.datetime.now().date())+'23:00', '%Y-%m-%d%H:%M')
            n_time = datetime.datetime.now()
            if n_time>d_time and n_time<d_time1:
            #if  True:    
                starttime = datetime.datetime.now()

                gubiaochi=tcData()
                
                gq.update_gubiaochi(gubiaochi)
                
                #print(gubiaochi.to_json(orient='index'))

                '''股票池 每隔两分钟做一个备份 '''
                t2 = int(datetime.datetime.now().strftime('%M'))
                if (t2 % 2) ==0:  
                    gq.bak_gubiaochi(gubiaochi)
                    print("股票池 備份 本次總共備份 %s 只股票 "%(len(gubiaochi)))

                print("最新的股票推荐信息已经更新到数据库共计 %s 只股票。"%(len(gubiaochi)))
               
                endtime = datetime.datetime.now()
                send=endtime-starttime 
                s=5-(send.seconds)
                print("荐股池 计算 %s 秒钟以后 继续下载  当前时间 %s" %(s,datetime.datetime.now()))
                if s>0:
                    time.sleep(s)

                #return #测试时加上 正式用时 把它没注释掉


            else:
                print('股票池:荐股池 计算 不在工作时间内，等待。。。。')
                time.sleep(30)
           
    '''

     if  jaodu_df_find.count()==0 or js_df_find.count()==0: 
        
        s=3  
        print("即时行情 或分时行情 数据库没有数据 %s   秒钟以后 继续查询"%(s))
        time.sleep(s) 
        return 
    
    '''
def test( ):
    gubiaochi=tcData()
    gq.update_gubiaochi(gubiaochi)
    print('end')
    
if __name__ == '__main__':
    #test()
    main(sys.argv)
   