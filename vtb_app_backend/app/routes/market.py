

# маркетплейс реализован в событиях events

# мы решили применять технологию и принципы блокчейн 
# и создать уневерсальный обьект, который создает экосистему, 
# на подобии универсального trello, где функции , 
# условия, награды могут переплетаться между собой



# мы решили не заниматься копипастингом, т.к. обьекты и данные, 
# и возможности в нашей идее схожие у всех сущностей

# проект легко расширяем, но сейчас нам нужно показать лишь mvp и идею
# разработать продукт




from fastapi import APIRouter, Request
router = APIRouter( prefix="", tags=[], dependencies=[], responses={},) ; api = None
#from service.processing import initProccessing; processing=None

# /find_event Post


from models.market import SearchObject
import time

MONGO_EVENTS_COLLECTION = "events"

def mongo_events_n_days_limit(days, limit=1000, query=None):
    return [el for el in api.db.select_mongo_by_datefromto_many(
                MONGO_EVENTS_COLLECTION,
                start=api.db.date_go_past_days_utc(days), # last 30 days
                limit=limit,
                query=query
                )]

def get_event_by_id(id_event):
    return api.db.read_mongo_by_id(MONGO_EVENTS_COLLECTION, id_event)

def save_event_by_id(id_event, data):
    print("save report",id_event)
    res=api.db.save_mongo_by_id(MONGO_EVENTS_COLLECTION, id_event, data)
    print("saved",res)





def timestamp_Active(filter_today):
    return { "timestamp_end": { "$gt": int(filter_today)  }}
def timestamp_Inactive(filter_today):
    return { "timestamp_end": { "$lt": int(filter_today)  }}

def get_events_by_query(days= None,
                        limit= None,
                        filter_today=None, 
                        reverse =False, 
                        query=None): #print(filter_today, 1667022171)
    filter={
               # "all_members": { "$in": [ id_user ] },
            }
    # if filter_today: 
    #     if reverse: filter.update(timestamp_Inactive(filter_today)) 
    #     else: filter.update(timestamp_Active(filter_today)) #{ "timestamp_end": { "$gt": int(filter_today)  }}) # только активные
    if query: filter.update(query)
    return [el for el in mongo_events_n_days_limit( days or 30, 
                                                    limit or 1000, 
                                                    query=filter)]

class Init:
    def __init__(self, obj = None): 
        global api ; api = obj ; global processing ; processing = api.processing #initProccessing(api)
        self.router = router # ; protects=[time.time()]; 

    @router.post("/api/find_events") 
    async def answer(search: SearchObject, r: Request): # print(item)
        d = search.dict()
        query={}
        if d['CATEGORY'] and len(d["CATEGORY"])>0: query["CATEGORY"] = {"$in": d["CATEGORY"]}
        if d['TYPE'] and len(d["TYPE"])>0: query["TYPE"] = {"$in": d["TYPE"]}
        if d['id_user'] and len(d["id_user"])>0: query["approved_members"] = {"$in": d["id_user"]}
        return api.return_or_error(lambda: get_events_by_query(
            days=d["days_back"],
            limit=d["limit"],
            query=query
        ))