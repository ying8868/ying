import pymongo
 
import pandas 
import json
from lib import ying_db
from lib.interface.east import * 

class init(object):

    def __init__(self,conf):
        self.db=ying_db.getConn(conf.host,conf.post)

    def run_init(self): 
        try:
            ec=east_core()
            df=ec.get_js_quote_baseuse()
            df = df[np.isnan(df['pice']) == False]
            df['h_is_updata']='no'
            print(df) 
            self.db.stock_basics.insert(json.loads(df.to_json(orient='records')))
            return  1  
        except  Exception as e : 
            return 0 
        
    def run_update(self):
        try:
            self.db.stock_basics.remove({})
            self.run_init()
            return  1  
        except  Exception as e : 
            return 0 
        
         



    
