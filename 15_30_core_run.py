#!/usr/bin/python3 
import itertools
import sys
from itertools import *


import threadpool

import config as conf
from lib.ying_quote import *
import talib as ta
import string 
gq =get_quote(conf)

def fiter(df):  
    #print(df)
    '''清理所有ST股票 '''
    for i in range(1,len(df)) :
        s=str(df.iloc[i,1]).find('S') 
        #print() 
        if s!=-1:
            gq.del_ONE_H_quote(df.iloc[i,0])  
    pass

def talibjs(d):
    ''' 压力位计算的方法'''
    print('正在计算'+d+"的压力位")
    gq =get_quote(conf)
    gd=gq.get_ONE_H_quote(d)
    #yc=float(gd['info']['yc'])*1.1
    
     

    #
    
    data=gd['data']
    datalen=len(data)
    if datalen<30:
        return
    #print(data)
    l=[]
    for i in  product(data): 
        t=list(i)[0].split(',')
        l.append(t)
    df=pd.DataFrame(l) 
    #tdxred(df) 

    tmdf=df.iloc[-25:-3,0:-1]

    tmdf['h']=0
    tmdf['s']=0
    tmdf=tmdf.apply(pd.to_numeric, errors='ignore')
    for i in range(1,len(tmdf)-1):
        a=tmdf.iloc[i-1,3]
        b=tmdf.iloc[i,3]
        c=tmdf.iloc[i+1,3]
        if b>a and b>c:
            tmdf.iloc[i,8]=b  
    tm2=tmdf.loc[tmdf.h>0]
    l1=tm2._stat_axis.values.tolist()
    tm2['ind'] = l1
    if len(tm2)<2:
        return

    #print(len(df))
    changdu=abs(tm2.iloc[0,-1]-tm2.iloc[-1,-1])
    '两个高点间的长度'
    #print(changdu)
    gaodicai=tm2.iloc[0,-3]-tm2.iloc[-1,-3]
    '两个高点间的高度差' 
    qgao=tm2.iloc[0,-3]
    '前高点'
    hgao=tm2.iloc[-1,-3]
    '后高点'
    yl=0
     
    xd=''
    if qgao>hgao:
        lcai=(qgao-hgao)/changdu #前高点大于后高点的落差
        #print(lcai)

        for i in range(1,len(tm2)-1):#进行判断中间的点是否有超出压力线的
            cd1=tm2.iloc[i,-1]-tm2.iloc[i-1,-1]#此高点与前高点间的长度
            cylw=qgao-cd1*lcai#此时压力位
            tm2.iloc[i,-2]=tm2.iloc[i,-3]-cylw 
        
        t2=tm2.s.max()    
        y=tm2.iloc[-1,-3]
        if t2>0: 
            y=(t2+y) 
            pass
        '下面计算明天压力位' 
        jg=tm2.iloc[-1,-1]
        y=(y-(datalen-1-tm2.iloc[-1,-1])*lcai) 
        xd='x'
        gq.update_ONE_H_quote(d,jg,lcai,xd,y)
        yl=y
 
    elif qgao<hgao:
        lcai=(hgao-qgao)/changdu #后高点大于前高点的落差
        #print('hxs lca')
        #print(lcai)
        for i in range(1,len(tm2)-1):#进行判断中间的点是否有超出压力线的
            cd1=tm2.iloc[i,-1]-tm2.iloc[i-1,-1]#此高点与前高点间的长度
            #print(cd1)
            cylw=qgao+cd1*lcai#此时压力位
            #print(cylw)
            tm2.iloc[i,-2]=tm2.iloc[i,-3]-cylw 
        t2=tm2.s.max()    
        y=tm2.iloc[-1,-3]
        if t2>0: 
            y=(t2+y) 
            pass  
        '下面计算明天压力位'
        jg=tm2.iloc[-1,-1]  
        y=((datalen-1-jg)*lcai+y)
        xd='d'
        gq.update_ONE_H_quote(d,jg,lcai,xd,y)
        yl=y
    #print(tm2)

    tmdf=df.iloc[-7:-1,0:-1]
    l1=tmdf._stat_axis.values.tolist()
    tmdf['ind']=l1
    tmdf['a']=0
    tmdf['b']=0
    
    tmdf=tmdf.apply(pd.to_numeric, errors='ignore')
    tmdf['a']=tmdf['ind']-jg
    
    if xd=='d':
        tmdf['b']=tmdf['a']*lcai+yl
        #print("if")
    else: 
        #print("else")
        tmdf['b']=yl-tmdf['a']*lcai
        
    for i in range(0,len(tmdf)):

        a=tmdf.iloc[i,3]
        if a>tmdf.iloc[i,10]: 
            
            gq.insert_ONE_JK_quote(d,tmdf.iloc[i,0],tmdf.iloc[i,8],yl) 
            return 

    if yl>a : 
        gq.insert_ONE_JK_quote(d,tmdf.iloc[-1,0],tmdf.iloc[-1,8],tmdf.iloc[-1,10])
        

             
    

    
def saixuanjiankung():
    '''选出需要进行监控的股票 '''
    pass

def main(argv):

    '''清理ST股票 '''   
    print('清理ST')
    fiter(pd.DataFrame(list(gq.get_name_H_quote())))
    

    '''下面是多线程方法进行计算 '''
    index=gq.get_H_code_index()
    df = pd.DataFrame(list(index))
    
    code_list=df['code'].tolist()
    
    pool = threadpool.ThreadPool(20)  
    requests = threadpool.makeRequests(talibjs, code_list) 
    [pool.putRequest(req) for req in requests] 
    pool.wait()  



if __name__ == '__main__':
    #talibjs(d='002372')
     #talibjs(d='603558')
    main(sys.argv)
