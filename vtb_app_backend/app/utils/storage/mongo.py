
# -*- coding: utf-8 -*-
import os, sys, time ; from dotenv import load_dotenv ; load_dotenv(verbose=True); 
os.environ['TZ'] = os.getenv("TZ") or 'Europe/Moscow' ; sys.path.append('./') ; sys.path.append('../') #load libs
from datetime import datetime, timedelta ; from pytz import timezone

from utils.tools.log_timer import LogTimer;t = LogTimer(); log_time = t.log_time ; spent_time = t.spent_time; rps_count = t.rps_count

# import redis
# import psycopg2
from pymongo import MongoClient
#from pymongo.objectid import ObjectId
from bson.objectid import ObjectId
import pymongo
#from pymongo import ObjectId

hours = {};minutes = {}
hours['24'] = 86400
hours['1'] = hours['24'] / 24
minutes['15'] = hours['1'] / 4

try: PRINT_EVENTS = int(os.getenv('DB_PRINT_EVENTS'))
except: PRINT_EVENTS = None
# try: SAVE_DIR = os.getenv('FILE_DUMP_DIR') #'dumps/'
# except: SAVE_DIR = ''
# try: ONLY_REDIS = int(os.getenv('DB_ONLdY_REDIS'))
# except: ONLY_REDIS = None


class Mongo:
    @staticmethod
    def objectId(hash): return ObjectId(hash)
    # MONGO
    def check_mongo(self):
        if not 'mongo' in vars(self): return self.get_mongo() 
        return self.mongo
    def get_mongo(self, MONGO_DB='test'):
        CONNECTION_STRING = os.getenv("mongo")
        if PRINT_EVENTS: print(CONNECTION_STRING)
        #CONNECTION_STRING = "mongodb://root:mongopass@localhost:27018/test?authSource=admin"
        client = MongoClient(CONNECTION_STRING)
        self.mongo = client[MONGO_DB]#'test']
        return self.mongo
    def read_mongo(self,col,key):
        if PRINT_EVENTS: print('read m '+str(col)+" "+ key)
        self.check_mongo()
        db = self.mongo
        find = None
        find = db[col].find_one(  {'key':key},  sort=[( '_id', pymongo.DESCENDING )]   )
        return find
    def read_mongo_by_id(self,col, id):
        if PRINT_EVENTS: print('read m '+str(col)+" "+ id)
        self.check_mongo()
        db = self.mongo
        find = None
        find = db[col].find_one(  {'_id': self.objectId(id)},  sort=[( '_id', pymongo.DESCENDING )]   )
        return find
    def save_mongo_by_id(self, coll, id, data):
        self.check_mongo(); db = self.mongo
        return db[coll].update_one(
            {'_id': self.objectId(id)}, 
            {"$set": data }, upsert=True)
    @staticmethod
    def date_go_past_days_utc(d=1):
        return datetime.today() - timedelta(days=d)
    def select_mongo_by_datefromto_many(self,coll,start=None,end=None,query=None, sort = None, limit=0):
        db = self.check_mongo()
        today = datetime.today()
        if not end: end = today
        #if not start: start = today - timedelta(days=1)
        find = {}
        if start: find = {'date': {'$lt': end, '$gte': start}, }
        if query: find.update(query )
        if not sort: sort = [( '_id', pymongo.DESCENDING )]
        if sort: res = db[coll].find( find, sort=sort )
        else: res = db[coll].find( find )
        if limit: res = res.limit(limit)
        return res
    def mongo_close(self):
        try: return self.mongo.close()
        except: pass
    def save_all_to_mongo(self, coll, key=None, value=None, only_insert = None, only_update = None, update_by_id=None, need_raplace=False):
        if PRINT_EVENTS: print('save m '+str(coll) +" "+ key)
        self.check_mongo()
        today = datetime.today()
        db = self.mongo
        #print('save mongo: '+str(key))
        #find = db.exnode_log.find_one(  {},  sort=[( '_id', pymongo.DESCENDING )]   )
        find = None
        if not key: key = str(today)
        # id or key
        if update_by_id: find = self.read_mongo_by_id(coll, update_by_id)
        elif not only_insert: find = db[coll].find_one(  {'key':key},  sort=[( '_id', pymongo.DESCENDING )]   )
        #
        if find:
            
            if need_raplace: obj = value # replace
            else: # update
                obj = find
                obj.update(value)
            obj.update({'upated':today})
            # id or key
            try:
                if update_by_id: db[coll].update_one({'_id':self.objectId(update_by_id)}, {
                    "$set": obj #{'data':value}
                },upsert=True)
                else: db[coll].update_one({'key':key,}, {
                    "$set": obj #{'data':value}
                },upsert=True)
            except Exception as e:
                print(e)
                return e
            if PRINT_EVENTS: print(value)
            if PRINT_EVENTS: print('updated to mongo')
            return obj
        elif not only_update and not update_by_id:
            obj = {'key':key,'date':today}
            obj.update(value)
            ins_id = db[str(coll)].insert_one( obj #{'key':key,'date':today,'data':value}
            ).inserted_id
            if PRINT_EVENTS: print('saved to mongo: '+str(ins_id))
            return ins_id

    def save_in_mongo(self, coll, value):  return self.save_all_to_mongo(coll, key=None, value=value)
    def mongo_items_n_days_limit(self, coll, days=365, limit=1000, query=None):
        return [el for el in self.select_mongo_by_datefromto_many(
                    coll,
                    start=self.date_go_past_days_utc(days), # last 30 days
                    limit=limit,
                    query=query
                    )]
    def mongo_universal_search_x(self, coll,x, days=365, limit=1000): # x = {"aaa":["bbb","ccc"], }
        query={}; filter_list=lambda x, f: {} if not(isinstance(x[f], list) and len(x[f])>0) else query.update({f: {"$in":x[f]}})
        if x and len(list(x))>0: [( filter_list(x,f) if not(x[f] and isinstance(x[f], str)) else query.update({x:x[f]})) for f in x]
        return self.mongo_items_n_days_limit(coll, query=query, days=days, limit=limit)

    def save_mongo(self,coll,key,value):
        return self.save_all_to_mongo(coll,key,value)