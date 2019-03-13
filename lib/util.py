import datetime
from lib.interface.east import east_core 
# 当前时间
n_time = datetime.datetime.now()
 
# 判断当前时间是否在开盘时间范围内 

def is_opentime(): 
    # 范围时间
    #上午开盘时间
    d_time = datetime.datetime.strptime(str(datetime.datetime.now().date())+'9:30', '%Y-%m-%d%H:%M')
    d_time1 =  datetime.datetime.strptime(str(datetime.datetime.now().date())+'11:33', '%Y-%m-%d%H:%M')

    #上午开盘时间
    d_time3 = datetime.datetime.strptime(str(datetime.datetime.now().date())+'13:00', '%Y-%m-%d%H:%M')
    d_time4 =  datetime.datetime.strptime(str(datetime.datetime.now().date())+'23:33', '%Y-%m-%d%H:%M')
 
    if (n_time > d_time and n_time<d_time1)or(n_time > d_time3 and n_time<d_time4):
        return True
    else :
        return False

def jaodu_is_opentime():
    jaodu_time = datetime.datetime.strptime(str(datetime.datetime.now().date())+'9:36', '%Y-%m-%d%H:%M')
    jaodu_time1 =  datetime.datetime.strptime(str(datetime.datetime.now().date())+'23:33', '%Y-%m-%d%H:%M')

    if (n_time > jaodu_time and n_time<jaodu_time1):
        return True
    else :
        return False
    pass

def min_is_opentime():
    min_time = datetime.datetime.strptime(str(datetime.datetime.now().date())+'9:35', '%Y-%m-%d%H:%M')
    min_time1 =  datetime.datetime.strptime(str(datetime.datetime.now().date())+'23:33', '%Y-%m-%d%H:%M')

    if (n_time > min_time and n_time<min_time1):
        return True
    else :
        return False
    pass

def get_sh_sz():
    ec=east_core()
    return ec.get_sh_sz()


