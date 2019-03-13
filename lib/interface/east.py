import json
import sys

import numpy as np
import pandas as pd
import pandas
import requests
 
from pandas.compat import StringIO 
 
from lib.interface.requests_helper import httphelper
import lib.interface.east_env as ee

class east_core(object):  
    def __init__(self):
        self.req=httphelper()
    def get_sh_h_quote(self):
        ''' 获取上证指数日线行情 主要是用来获取异动信息'''
        #http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=0000011&TYPE=k&js=fsData1551859520124_93029276((x))&rtntype=5&isCR=false&authorityType=fa&fsData1551859520124_93029276=fsData1551859520124_93029276
        url='http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=0000011&TYPE=k&js=fsData1551859520124_93029276((x))&rtntype=5&isCR=false&authorityType=fa&fsData1551859520124_93029276=fsData1551859520124_93029276'



    def get_sh_sz(self):
        '''获取上证指数行情 '''
        #http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=0000011,3990012&sty=DFPIU&st=z&sr=&p=&ps=&cb=&js=var%20C1Cache={quotation:[(x)]}&token=44c9d251add88e27b65ed86506f6e5da&0.919304481310702
        url="http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=0000011,3990012&sty=DFPIU&st=z&sr=&p=&ps=&cb=&js=var%20C1Cache={quotation:[(x)]}&token=44c9d251add88e27b65ed86506f6e5da&0.919304481310702"
        text=self.req.get(url).text[25:-3]
        lis=text.split('","')
        rl=[]
        rl.append(lis[0].split(','))
        rl.append(lis[1].split(','))  
        return pd.DataFrame(rl)

    
    def get_quote(self,code):
        '''
        获取分时行情
        http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=4f1862fc3b5e77c150a2b985b12db0fd&id=0000022&type=r&iscr=true&cb=jsonp1532881188320
        
        '''
        if code[0]=='6':
            sc='1'
        else:
            sc='2'
        url='http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=4f1862fc3b5e77c150a2b985b12db0fd&id='+code+sc+'&type=r&iscr=true&cb=jsonp1532881188320'
        text=self.req.get(url).text[19:-1]
        r=json.loads(text)
        ''' 
         setting = json.load(f)
 6     family = setting['BaseSettings']['size']   //注意多重结构的读取语法
 7     size = setting['fontSize']   
 8     return family
        '''
        # r['info']['c'])

        #sys.exit(1)
        return r 
    
    '''
    def get_yidong(self,code,sc,date):
        
        # 'http://nuyd.eastmoney.com/EM_UBG_PositionChange/api/Js/Get?sty=DETAIL&type=tp&callback=jQuery1720599923922416312_1551687739285&cmd=3004912&filter=(tradeDate%3D^2019-02-28^)&_=1551690068641'
        url="http://nuyd.eastmoney.com/EM_UBG_PositionChange/api/Js/Get?sty=DETAIL&type=tp&callback=jQuery1720599923922416312_1551687739285&cmd="+code+sc'&filter=(tradeDate%3D^'+str(date)+'^)&_=1551690068641'
        
        
    ''' 

    def get_yidong(self,code,sc,date): 
        '''股票异动下载　 股票池里面的股票提供代码进行下载  '''
        url="http://nuyd.eastmoney.com/EM_UBG_PositionChange/api/Js/Get?sty=DETAIL&type=tp&callback=jQuery1720599923922416312_1551687739285&cmd="+str(code)+str(sc)+"&filter=(tradeDate%3D^"+str(date)+"^)&_=1551690068641"
        print(url)
        text=self.req.get(url).text[40:-1]
        return text


    def get_H_quote(self,code):
        '''
        获取历史K线行情
        return: 数组结构   日期  开盘价  现价  最高价  最低价  成交量 成交额  振幅  换手
http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=4f1862fc3b5e77c150a2b985b12db0fd&cb=jQuery18305628199241932036_1548084568740&id='+code+sc+'&type=k&authorityType=&_=1548085170706        
        '''
        if code[0]=='6':
            sc='1'
        else:
            sc='2'  
        url='http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=4f1862fc3b5e77c150a2b985b12db0fd&cb=jQuery18305628199241932036_1548084568740&id='+code+sc+'&type=k&authorityType=&_=1548085170706 '
        text=self.req.get(url).text[41:-1]
        
        r=json.loads(text)
        ''' 
         setting = json.load(f)
 6     family = setting['BaseSettings']['size']   //注意多重结构的读取语法
 7     size = setting['fontSize']   
 8     return family
        '''
        # r['info']['c'])

        #sys.exit(1)
        #print(r) 
        return r 
    
    def get_one_js_quote(self,code,sc):
        #hper=httphelper()
        '''
        获取单只股票的即时行情信息
        http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?token=beb0a0047196124721f56b0f0ff5a27c&cb=jQuery17205911308372721681_1551933373541&id=6010681&_=1551933374119
        ''' 
        #url='http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=4f1862fc3b5e77c150a2b985b12db0fd&cb=jQuery18305628199241932036_1548084568740&id='+code+sc+'&type=k&authorityType=&_=1548085170706 '
        url='http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?token=beb0a0047196124721f56b0f0ff5a27c&cb=jQuery17205911308372721681_1551933373541&id='+code+sc+'&_=1551933374119'
        text=self.req.get(url).text[41:-1] 
        #r=json.loads(text)
        ''' 
         setting = json.load(f)
 6     family = setting['BaseSettings']['size']   //注意多重结构的读取语法
 7     size = setting['fontSize']   
 8     return family
        '''
        # r['info']['c'])

        #sys.exit(1)
        #print(r) 
        return text



    def get_js_quote(self):
        ''' 获取即时行情列表 通过即时行情列表分析出每只股票的行情'''
        page='1'
        size='200'
        url='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery112400687705920710221_1529902563309&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&js=({data%3A[(x)]%2CrecordsTotal%3A(tot)%2CrecordsFiltered%3A(tot)})&cmd=C._A&sty=FCOIATC&st=(ChangePercent)&sr=-1&p='+page+'&ps='+size+'&_=1529902563327'
        text=self.req.get(url).text
        recordsTotal=int(text[-6:-2])
        text_for='' 
        #for i  in range(int(recordsTotal/int(size))+1):
        for i  in range(1,int(recordsTotal/int(size))+1):
            page1=str(i) 
            url1='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery112400687705920710221_1529902563309&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&js=({data%3A[(x)]%2CrecordsTotal%3A(tot)%2CrecordsFiltered%3A(tot)})&cmd=C._A&sty=FCOIATC&st=(ChangePercent)&sr=-1&p='+page1+'&ps='+size+'&_=1529902563327'

            text_for=text_for+self.req.get(url1).text[50:-43]+'","' 
        #print(text_for[0:-3])

        stock_list=text_for[0:-3].rstrip().split('","')
        l1=[]
        for i in stock_list:
            l1.append(i.split(','))
            ##print(i)   
        df=pd.DataFrame(l1,columns=ee.ENV_EAST_HQ_ZF ) 

        df[['pice', 'zdr',
                 'zdf', 'cjl', 'cjr','zhenf','high','low',
                 'open','close','lb','hsl','syl','sjl'
                 ,'sz','ltsz']] = df[['pice', 'zdr',
                 'zdf', 'cjl', 'cjr','zhenf','high','low',
                 'open','close','lb','hsl','syl','sjl'
                 ,'sz','ltsz']].convert_objects(convert_numeric=True)  
        #print(df) 
        return df

    def get_js_quote_baseuse(self):
        ''' 获取即时行情列表 通过即时行情列表分析出每只股票的行情'''
        page='1'
        size='200'
        url='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery112400687705920710221_1529902563309&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&js=({data%3A[(x)]%2CrecordsTotal%3A(tot)%2CrecordsFiltered%3A(tot)})&cmd=C._A&sty=FCOIATC&st=(ChangePercent)&sr=-1&p='+page+'&ps='+size+'&_=1529902563327'
        text=self.req.get(url).text
        recordsTotal=int(text[-6:-2])
        text_for='' 
        #for i  in range(int(recordsTotal/int(size))+1):
        for i  in range(1,int(recordsTotal/int(size))+1):
            page1=str(i) 
            url1='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery112400687705920710221_1529902563309&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&js=({data%3A[(x)]%2CrecordsTotal%3A(tot)%2CrecordsFiltered%3A(tot)})&cmd=C._A&sty=FCOIATC&st=(ChangePercent)&sr=-1&p='+page1+'&ps='+size+'&_=1529902563327'

            text_for=text_for+self.req.get(url1).text[50:-43]+'","' 
        #print(text_for[0:-3])

        stock_list=text_for[0:-3].rstrip().split('","')
        l1=[]
        for i in stock_list:
            l1.append(i.split(','))
            ##print(i)   
        df=pd.DataFrame(l1,columns=ee.ENV_EAST_HQ_ZF ) 

        df[['pice', 'zdr',
                 'zdf', 'cjl', 'cjr','zhenf','high','low',
                 'open','close','lb','hsl','syl','sjl'
                 ,'sz','ltsz']] = df[['pice', 'zdr',
                 'zdf', 'cjl', 'cjr','zhenf','high','low',
                 'open','close','lb','hsl','syl','sjl'
                 ,'sz','ltsz']].convert_objects(convert_numeric=True)  
        
       
        return df