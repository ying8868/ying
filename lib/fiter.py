
import pandas as pd


class ying_filter(object):
    def js_quote_filter(self, df):
        print("过滤之前有%s条信息" % (len(df)))  
        
        dfcode = df['code'] 
        df = df.apply(pd.to_numeric, errors='ignore')
        df['yl']=df['pice']-df['ylw'] 
        df['code'] = dfcode 
        #df = df[df['zdf'] < 6]  # 条件过滤 涨跌幅小于6
        #df = df[df['zdf'] > -3]  # 条件过滤 涨跌幅大于-1
        #df = df[df['testdata2'] <8]  # 条件过滤 选出昨日涨幅小于8的股票

        #df = df[df['y3_zf']<20]  # 条件过滤 3日涨幅小于8的股票
        #df = df[df.y1_zf]<9]  #去除昨天涨停的股票
        df = df[df.y3_zf < 20]
        df = df[df.y1_zf < 9.9]
        df = df[df.pice<30]  #去除20元以上股票
        #df = df[df['lb'] > 2]  # 条件过滤 量比大于2
        #df=df[df['yl']>0]       #去除未突破压力位的股票
        df['boo']=df['name'].str.contains('ST') # bool = df.str.contains('Mr\.') #不要忘记正则表达式的写法，'.'在里面要用'\.'表示 
        df=df[df.boo==False]    #去除ST股
        print("过滤之后有%s条信息" % (len(df)))  
        #print(df)
        
        return df
    def gubiaochi_filter(self,df):
         
        dfcode = df['code'] 
        df = df.apply(pd.to_numeric, errors='ignore')
        df['code'] = dfcode
         
        #df = df[df['jd'] > 30] #条件过滤 选出均线角度大于30的股票
        df['zfc']=df['zdf']-df['ss']
        #df['zdfc']=df['nzdf']-df['zdf']
        df = df[df['zfc'] > 0] 
        df = df[df['yd_mod_count'] > 0] 
        df = df[df['dd_count'] > 0]
        df = df[df.y3_zf < 20]
        df = df[df.y1_zf < 9]

        #df=df['zfc']>0 #条件过滤 选出涨幅超过对应大盘的股票 
        #print(df)
        #df = df[['code', 'jd', 'yd_y_d_count', 'yd_y_k_count','ntime','nzdf','dd_count','name','pice','nzdf','yd_mod_count','yd_count','dd_count','kk_count','hsl','lb','ylw','yl','zhenf']]
        #df['zdfc']=df['nzdf']-df['zdf'] 
        #df.drop('_id',axis=1,inplace=True)
        #df.drop('nzdf',axis=1,inplace=True)
        #df.drop('hsl',axis=1,inplace=True)
        #df.drop('lb',axis=1,inplace=True)
        #df.drop('pice',axis=1,inplace=True)
        #df.drop('high',axis=1,inplace=True)
         

        #print(df)
        return df



    pass
