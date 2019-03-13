import json
import time 
import pandas as pd
import pymongo
 
import datetime
import threadpool
from lib import ying_db
from lib.interface.east import east_core 
from lib.fiter import ying_filter

class down_quote(object):

    '行情下载类'
    
    def __init__(self,conf):

        self.db=ying_db.getConn(conf.host,conf.post) 
    def down_daily(self, stock_code):
        '''下载分时行情且将分时行情存储到数据库 min_quote'''
        ec=east_core()
        ecrn=ec.get_quote(stock_code)
        self.db.min_quote.update({"code":ecrn['code']},{'$set':ecrn},True,False)
        
        print ('分时行情: %s 的分时行情已经更新.'%(ecrn['code']))

        pass
    def down_H_daily(self, stock_code):
        '''下载历史K线行情且将所下载下来的数据库存储到数据库 H_quote ''' 
        ec=east_core()
        ecrn=ec.get_H_quote(stock_code)
        #json_text=json.loads(ecrn)
        y1c=float(ecrn['data'][-1].split(',')[2])
        y2c=float(ecrn['data'][-2].split(',')[2])
        y3c=float(ecrn['data'][-3].split(',')[2])
       
        ##             O    C    H   L
        # #2019-03-08,6.19,6.52,6.9,6.12,455819,305968464,12.44%,16.60#
        ## 
        #y2c=float(ecrn['data'][-2].split(',')[2])
        
        #测试昨天的涨幅 正式使用的时候需要换成 Y1 
        data3=float(ecrn['data'][-4].split(',')[2])
        y1_zf=round((y1c-y2c)/y2c*100,2)
        testdata2=(y2c-y3c)/y3c*100 
        y3_zf=round((y1c-data3)/data3*100,2)
        #print('code:%s yc:%s 1:%s  3:%s info:%s  %s'%(stock_code,testdata2,y1_zf,y3_zf,data3,ecrn['data'][-1]))
        self.db.JK_quote.update({"code":ecrn['code']},{'$set':{'testdata2':testdata2,'y1_zf':y1_zf,'y3_zf':y3_zf}},True,False)
        self.db.H_quote.update({"code":ecrn['code']},{'$set':ecrn},True,False)
        self.db.stock_basics.update({"code":ecrn['code']},{'$set':{'h_is_updata':'yes'}},True,False)

        pass
    def down_js_daily(self,jkdf):
        '''下载即时行情信息，此方法是通过行情列表所下载  js_quote'''
        ec=east_core()
        df=ec.get_js_quote()
        #[self.__js_daily_to_mongodb__(i,df) for i in df.index] 
        jkdf=pd.DataFrame(list(jkdf))
        jkdf=jkdf[['code','ylw','y1_zf','y3_zf','testdata2']]
        df=pd.merge(df,jkdf)

        '''此处加入 filter 进行过滤 ''' 
        print('下载完毕进行过滤。')
        yf=ying_filter()
        df=yf.js_quote_filter(df) 
        #print(df)
        for index, row in df.iterrows():  
            #print(json.loads(row.to_json()))
            self.db.js_quote.update({"code":row['code']},{'$set':json.loads(row.to_json())},True,False)
        pass
    def down_yidong(self,code,sc,date):
        '''异动下载类 通过 股票池里面的股票提供代码进行下载 此处只有下载方法''' 
        ec=east_core()
        text=ec.get_yidong(code,sc,date) 
        if text=='': 
            print('股票%s 当天没有异动情况.'%(code))
        else:
            df=pd.DataFrame(json.loads(text))
            df = df.apply(pd.to_numeric, errors='ignore')
            yd_mod_count=len(df) #异动类型次数
            yd_count=df['Count'].sum()
            yd_d_count=df['BullOrBear'].sum() 
            yd_k_count=yd_mod_count-yd_d_count  
            dd_count=0
            kk_count=0
            dd_list=[]
            dd_time='15:30' #多方大单出现的第一时间
            for  index, row in df.iterrows(): 
                #print(row) 
                if str(row[3]) in ('64','8193'):
                    dd=row[2]
                    dd_count=dd_count+len(dd)
                    #dd_list.append(dd)
                    for x in dd:
                        dd_list.append(x.split(',')) 
                    #print('大买单:%s  类型:%s'%(dd,type(dd))) 
                    
                elif str(row[3]) in ('128','8194'): 
                    kk=row[2]
                    kk_count=kk_count+len(kk)
                    #print('大卖单:%s'%(row[2]))
            if len(dd_list)>0:          
                tmp_df=pd.DataFrame(dd_list,columns=['time', 'count','pice','zf','vol'])
                #,columns=['time', 'score']  .iloc[-1:0]
                tmp_df=tmp_df.sort_values(axis=0, ascending=False, by='time') 
                for index, row in tmp_df.iterrows(): 
                    one_time=row['time'] 
                dd_time=one_time[0:-3]
                #print(dd_time)
                 
            #
            print(dd_list)
            yd_count=df['Count'].sum() 
            self.db.jaodu.update({"code":code},{'$set':{'dd_time':dd_time,'dd_count':str(dd_count),'kk_count':str(kk_count),'yd_mod_count':str(yd_mod_count),'yd_count':str(yd_count),'yd_d_count':str(yd_d_count),'yd_k_count':str(yd_k_count),'yd_mes':text}},True,False)
            #print('股票  %s  异动类数是 %s   异动次数 %s 多方大笔买入%s 次    空方大笔卖出 %s  次'%(code,yd_mod_count,yd_count,dd_count, kk_count)) 
            pass

    def down_today_yidong(self,code,sc,date):
        '''当日 异动 下载类 通过 股票池里面的股票提供代码进行下载 此处只有下载方法''' 
        ec=east_core()
        text=ec.get_yidong(code,sc,date)
        if text=='':
            print('股票%s 当天没有异动情况.'%(code))
            self.db.y_yidong.update({"code":code},{'$set':{'code':code,'yd_y_d_count':'0','yd_y_k_count':'0','yd_mes':''}},True,False)
        else:
            df=pd.DataFrame(json.loads(text))
            df = df.apply(pd.to_numeric, errors='ignore')
            '''
            for index, row in df.iterrows(): 
            #for i in range(len(df)):
                if str(row['MoveCode']) in ('8193','8201','8202','64','8215','4','8207','32','8211','8209','8213'):
                    print('多方: 异动代码 %s  %s'%(row['MoveCode'],row['TranName']))
                elif str(row['MoveCode']) in('8194','8203','128','16','8212','8204','8','8210','8208','8216','8214',):
                    print('空方: 异动代码 %s  %s'%(row['MoveCode'],row['TranName']))
                else: pass  '''
            yd_mod_count=len(df) #异动类型次数

            #yd_count=df['Count'].sum()
            yd_y_d_count=df['BullOrBear'].sum() 
            yd_y_k_count=yd_mod_count-yd_y_d_count 
            #print(df) 
            self.db.y_yidong.update({"code":code},{'$set':{'code':code,'yd_y_d_count':str(yd_y_d_count),'yd_y_k_count':str(yd_y_k_count),'yd_mes':text}},True,False)
            print('股票  %s  多方异动 %s   空方异动 %s '%(code,yd_y_d_count,yd_y_k_count)) 
            pass

        

        


class get_quote(object): 

    '''连接数据库后的操作类 ，通过此类进行获取数据库的操作。'''
    def __init__(self,conf):
        self.db=ying_db.getConn(conf.host,conf.post) 
    #
    #股票池 备份数据库
    #
    def bak_gubiaochi(self,df):
        t1=str(time.strftime('%Y-%m-%d  %H:%M',time.localtime(time.time())) ) 
        result=self.db.bak_gubiaochi.find({'time':t1}).count()  
        if result ==0:
           # self.db.bak_gubiaochi.update({"time":t1},{'$set':json.loads(df.to_json())},True,False)
            print(result) 
        #gq.get_all_js_quote().count()==0 
        
        pass
        #.strftime('%M'))  datetime.datetime.strftime(time1,'%Y-%m-%d %H:%M:%S')
        #time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))#(string,'%Y-%m-%d %H:%M')
        #self.db.bak_gubiaochi.update({"time":time]},{'$set':json.loads(df.to_json())},True,False)

    #####
    # y_yidong 数据库操作方法
    #####
    def get_y_yidong(self):
        ''' 查询昨日异动数据库'''
        return self.db.y_yidong.find()
    def clear_y_yidong(self): 
        '''清理昨日异动数据库'''
        self.db.y_yidong.remove()


    ##
    # 即时行情 数据库操作方法
    #
    def get_js_quote(self,stock):
        '''根据所提供的股票代码查询即时行情信息'''

        return self.db.js_quote.find_one({"code": stock})

    def get_js_quote_count(self):
        '''根据所提供的股票代码查询即时行情信息'''
        return self.db.js_quote.find().count()

    def get_all_js_quote(self):
        '''根据所提供的股票代码查询即时行情信息'''
        return self.db.js_quote.find()
    def clear_js_quote(self):
        '''清理即时行情数据库 '''
        self.db.js_quote.remove()


    #
    # 个股分时 行情数据库操方法
    #
   

    def get_min_quote(self,stock):
        '''获取个股分时行情'''
        return self.db.min_quote.find_one({'code':stock})
    def get_min_quote_count(self):
        '''获取所有个股分时行情'''
        return self.db.min_quote.find().count()
    def get_all_min_quote(self):
        '''获取所有个股分时行情'''
        return self.db.min_quote.find() 
    
    def get_one_min_quote(self,code):
        '''获取 单个股票 的分时行情'''
        return self.db.min_quote.find({'code':code}) 
    
    
    def clear_min_quote(self): 
        self.db.min_quote.remove({}) 
    
    #
    # 股票池 数据库操方法
    #
    def get_gubiaochi_count(self):
        '''获取股票池内的股票数量 '''
        return self.db.gubiaochi.find(  ).count()
    def get_all_gubiaochi(self):
        '''获取股票池内的股票 此方法只返回 代码 市场 日期 '''
        return self.db.gubiaochi.find( {}, { 'code': 1, 'sc': 1 ,'10':1} )

    def update_gubiaochi(self,df): 
        for index, row in df.iterrows():  
            #print(json.loads(row.to_json()))
            self.db.gubiaochi.update({"code":row['code']},{'$set':json.loads(row.to_json())},True,False)
    def clear_gubiaochi(self):
        self.db.gubiaochi.remove()
        


    #
    # 分时行情 均线角度数据库
    #print('%s  %s  %s  %s'%(minlist[0],ntime,ntimejd,jd)) 
    #
    
    def update_ONE_jaodu(self,code,ntime,yc,jd,nzdf):
        self.db.jaodu.update({'code':code},{'$set':{'code':code,'ntime':str(ntime),'yc':str(yc),'jd':str(jd),'nzdf':str(nzdf)}},True,False)

    def find_one_jaodu(self,code):
        return self.db.jaodu.find_one({'code':code})
    def get_jaodu_count(self):
        return self.db.jaodu.find().count()
    
    def get_all_jaodu(self):
        return self.db.jaodu.find() 

    def clear_jaodu(self):
        self.db.jaodu.remove()
    #
    # 压力位 监控数据库操作方法
    #
    def get_JK_quote(self):
        '''获取监控数据库信息 '''
        return self.db.JK_quote.find()
    def insert_ONE_JK_quote(self,code,tprq,ind,ylw):
        '''向监控数据库插入一条监控信息 '''
        self.db.JK_quote.update({'code':code},{'$set':{'tprq':str(tprq),'ind':str(ind),'ylw':str(ylw),'code':str(code)}},True,False)

    def insert_OONE_JK_quote(self,code,tprq,ind,ylw):
        '''向监控数据库插入一条监控信息 '''
        self.db.OJK_quote.update({'code':code},{'$set':{'tprq':str(tprq),'ind':str(ind),'ylw':str(ylw),'code':str(code)}},True,False)

    #
    # 历史K线 数据库操作方法
    #
    def update_ONE_H_quote(self,code,keylcindex,laucai,s,y): 
        '''更新一条日线数据信息 '''
        self.db.H_quote.update({'code':code},{'$set':{'keylcindex':str(keylcindex),'laucai':str(laucai),'s':s,'y':str(y)}},True,False)

    def del_ONE_H_quote(self, index):
        '''删除一条日线数据信息 '''
        #col.delete_one({'name':'Neil'})#删除名字为Neil的记录
        self.db.H_quote.delete_one({'_id':index})  
    
    def get_ONE_H_quote(self,code): 
        '''查询一条日线数据信息 '''
        data=self.db.H_quote.find_one({'code':code}) 
        return data
    def get_H_code_index(self):
        '''获取数据库中历史行情信息的代碼索引'''
        return  self.db.H_quote.find({}, { 'code': '1' }) 
    def get_name_H_quote(self): 
        '''获取数据库中历史行情信息的名称索引'''
         
        return self.db.H_quote.find({}, { 'name': '1' })     

    def get_H_quote_count(self):
        '''获取历史K线数据库中总共有多少条信息'''
        return self.db.H_quote.find().count()




class quote_hold(object): 
     
    def __init__(self,conf):
        self.dq= down_quote(conf)
        self.gq=get_quote(conf) 
        self.db=ying_db.getConn(conf.host,conf.post)

    def __threadpool_down__(self,code):
        '内部方法 多线程下载 分时 行情时 使用'
        
        self.dq.down_daily(code) 
        #print(code)

    def __threadpool_down_H_quote__(self,code):
        '内部方法 多线程下载 历史 行情时 使用'
        

        self.dq.down_H_daily(code)
        print("正在下载"+code+"的日K线")
    def __threadpool_down_yidong__(self,codelist):
        '异动下载多线程辅助方法' 
        #3004912  2019-02-28
        #dq.down_yidong('300072','2','2019-03-04')
        #dq.down_yidong(codelist[1],codelist[0])   
        #print("正在下载"+codelist[2]+ "的异动信息")

        d=time.strftime("%Y-%m-%d", time.localtime())
        #d='2019-03-04'
        s=str(codelist) 
        if  s.find('6',0,len(s))==0: 
            sc=1
        else:
            sc=2 
        self.dq.down_yidong(codelist,sc,d)


    def __threadpool_down_today_yidong__(self,code):
        d=time.strftime("%Y-%m-%d", time.localtime())
        s=str(code) 
        if code[0]=='6':
            sc='1'
        else:
            sc='2' 
        self.dq.down_today_yidong(code,sc,d)
        pass  
         

    def quote_down_run(self):
        '多线程下载分时行情数据。'
        #dq= down_quote(self.conf)
        stock_chi=self.db.js_quote.find({})
        '连接数据库 并查找出  yidong  行情过滤后 所有股票的代码'
        #stock_chi=self.db.min_quote.find({}) 
        # 
               
        df = pd.DataFrame(list(stock_chi))
        
        dfcode = df['code'] 
        df = df.apply(pd.to_numeric, errors='ignore') 
        df['code'] = dfcode 
       
        #df=df[df['dd_count']>0]
        #print(df)
        
         
        code_list=df['code'].tolist()
        '多线程时需要传递的参数'
        pool = threadpool.ThreadPool(8) 
        
        requests = threadpool.makeRequests(self.__threadpool_down__, code_list) 
        [pool.putRequest(req) for req in requests] 
        pool.wait()  
        #print(code_list)
        
    
    def js_quote_down(self): 
        '''即时行情下载 ，通过行情列表进行下载'''
        
        yldf=self.gq.get_JK_quote()

         
        self.dq.down_js_daily(yldf)

    def yi_dong_down_run(self):
        '''当日异动 下载 多线程'''
        #self.__threadpool_down_today_yidong__('002437')
        #gq=get_quote(self.conf)
        self.gq.clear_y_yidong() #首先要把昨日的异动数据库清理掉

        stock_chi=self.db.stock_basics.find({}, { 'code': '1' }) 
        df=pd.DataFrame(list(stock_chi) ) 
        code_list = df['code'].tolist() 
        pool = threadpool.ThreadPool(10) 
        requests = threadpool.makeRequests(self.__threadpool_down_today_yidong__,code_list) 
        [pool.putRequest(req) for req in requests] 
        pool.wait()
         
        pass


    def H_quote_down_run(self):
        '历史行情 多线程下载方法， 此方法每天运行一次'
        #dq= down_quote(self.conf)

        stock_chi=self.db.stock_basics.find({'h_is_updata':'no'}, { 'code': '1' })

        #stock_chi=self.db.min_quote.find({})
        # 
        l=self.db.stock_basics.find({'h_is_updata':'no'}).count()
        
        while  l > 1:     
            df = pd.DataFrame(list(stock_chi))
            code_list=df['code'].tolist()
            pool = threadpool.ThreadPool(10) 
            requests = threadpool.makeRequests(self.__threadpool_down_H_quote__, code_list) 
            [pool.putRequest(req) for req in requests] 
            pool.wait()
            stock_chi=self.db.stock_basics.find({'h_is_updata':'no'}, { 'code': '1' })
            l=self.db.stock_basics.find({'h_is_updata':'no'}).count() 
            print('15h_quote_down 下载日K线程序运行完毕 还有%s条数据未下载'%(l))
        
    def down_yidong_run(self):
        ''' 异动下载多线程方法 '''
        self.__threadpool_down_yidong__('')
        #gq=get_quote(self.conf)
        df=pd.DataFrame(list(self.gq.get_all_js_quote()) )  
        code_list = df['code'].tolist() 
        pool = threadpool.ThreadPool(10) 
        requests = threadpool.makeRequests(self.__threadpool_down_yidong__,code_list) 
        [pool.putRequest(req) for req in requests] 
        pool.wait() 
        
        #print('down_yidong_run(self)')
        

        





        #print(code_list)
 

