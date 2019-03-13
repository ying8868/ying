from datetime import datetime
import time
class east_core(object): 
 
    #判断是否为工作日,工作日返回1，非工作日返回0
    def is_Work_Time(self):
        workTime=['09:00:00','18:00:00']
        dayOfWeek = datetime.datetime.now().weekday()
        #dayOfWeek = datetime.today().weekday()
        beginWork=datetime.datetime.now().strftime("%Y-%m-%d")+' '+workTime[0]
        endWork=datetime.datetime.now().strftime("%Y-%m-%d")+' '+workTime[1]
        beginWorkSeconds=time.time()-time.mktime(time.strptime(beginWork, '%Y-%m-%d %H:%M:%S'))
        endWorkSeconds=time.time()-time.mktime(time.strptime(endWork, '%Y-%m-%d %H:%M:%S'))
        if (int(dayOfWeek) in range(5)) and int(beginWorkSeconds)>0 and int(endWorkSeconds)<0:
            return 1
        else:
            return 0