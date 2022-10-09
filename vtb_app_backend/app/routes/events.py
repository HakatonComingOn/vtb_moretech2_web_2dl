
from fastapi import APIRouter, Request
router = APIRouter( prefix="", tags=[], dependencies=[], responses={},) ; api = None
#from service.processing import initProccessing; 
# processing=None

# /new_event post
# /get_members_event/event_id get
# /get_all_active_events get
# /get_all_inactive_events get
# /get_event/id get
# /set_user_to_event post body{user_id}
# /get_active_events/user_id get

from models.events import ItemEvent, Reward, Creator
import time

MONGO_EVENTS_COLLECTION = "events"

def mongo_events_n_days_limit(days, limit=1000, query=None):
    if not query: query= {}
    query["$where"] = "!this.CATEGORY || this.CATEGORY.length < 1" 
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

async def update_event__add_user_to_member(request, is_delete=False): #id_event, id_user):
    j=await request.json()
    id_event=j['id_event'] ; id_user=j['id_user']
    read = get_event_by_id(id_event)
    if is_delete:
        if id_user in read['all_members']: 
            del(read['all_members'][read['all_members'].index(id_user)])
            save_event_by_id(id_event, read)
    else: # add
        if not id_user in read['all_members']: 
            read['all_members'].append(id_user)
            save_event_by_id(id_event, read)
    return read

async def from_level_to_level(request, is_delete=False, FROM_LEVEL='all_members', TO_LEVEL='approved_members'):
    j=await request.json()
    id_event=j['id_event'] ; id_user=j['id_user']
    read = get_event_by_id(id_event)
    if is_delete:
        if id_user in read[TO_LEVEL]: 
            del(read[TO_LEVEL][read[TO_LEVEL].index(id_user)])
            save_event_by_id(id_event, read)
    else: # add
        if id_user in read[FROM_LEVEL] and not id_user in read[TO_LEVEL]: 
            read[TO_LEVEL].append(id_user)
            save_event_by_id(id_event, read)
    return read

# подтверждегние пользователя как участника события
# async def update_event__set_member_to_approved(request, is_delete=False): #id_event, id_user):
#     j=await request.json()
#     id_event=j['id_event'] ; id_user=j['id_user']
#     read = get_event_by_id(id_event)
#     if is_delete:
#         if id_user in read['approved_members']: 
#             del(read['approved_members'][read['approved_members'].index(id_user)])
#             save_event_by_id(id_event, read)
#     else: # add
#         if id_user in read['all_members'] and not id_user in read['approved_members']: 
#             read['approved_members'].append(id_user)
#             save_event_by_id(id_event, read)
#     return read

# # подтверждегние выполнения задания
# async def update_event__set_approved_to_successed(request, is_delete=False): #id_event, id_user):
#     j=await request.json()
#     id_event=j['id_event'] ; id_user=j['id_user']
#     read = get_event_by_id(id_event)
#     if is_delete:
#         if id_user in read['approved_members']: 
#             del(read['successed_members'][read['successed_members'].index(id_user)])
#             save_event_by_id(id_event, read)
#     else: # add
#         if id_user in read['all_members'] and not id_user in read['successed_members']: 
#             read['successed_members'].append(id_user)
#             save_event_by_id(id_event, read)
#     return read

# # подтверждегние выплаты награды
# async def update_event__set_member_to_approved(request, is_delete=False): #id_event, id_user):
#     j=await request.json()
#     id_event=j['id_event'] ; id_user=j['id_user']
#     read = get_event_by_id(id_event)
#     if is_delete:
#         if id_user in read['approved_members']: 
#             del(read['approved_members'][read['approved_members'].index(id_user)])
#             save_event_by_id(id_event, read)
#     else: # add
#         if id_user in read['all_members'] and not id_user in read['approved_members']: 
#             read['approved_members'].append(id_user)
#             save_event_by_id(id_event, read)
#     return read


async def update_event__user_report_event(request): #id_event, id_user):
    j=await request.json()
    id_event=j['id_event'] ; id_user=j['id_user'] ; text=j['text'] 
    read = get_event_by_id(id_event)
    if read and text and len(text)>5:
        message={ "timestamp": time.time() , "text": text }
        if not 'user_reports' in read: #print("set report", id_event)
            read['user_reports']=[]
            read['user_reports'].append( {"id_user": id_user, "messages":[message]} )
            save_event_by_id(id_event, read)
        else: # print("upd report", id_event)
            found=False
            for el in read["user_reports"]: #print(el["id_user"])
                if el["id_user"] == id_user: # print(el)
                    el["messages"].insert(0, message ) # print("updated      report", id_event)
                    found=True
                    save_event_by_id(id_event, read)
                    break
            if not found: #print("not found", id_user)
                read['user_reports'].append( {"id_user": id_user, "messages":[message]} )
                save_event_by_id(id_event, read)

    return read

def timestamp_Active(filter_today):
    return { "timestamp_end": { "$gt": int(filter_today)  }}
def timestamp_Inactive(filter_today):
    return { "timestamp_end": { "$lt": int(filter_today)  }}

def get_events_by_user_id(id_user, filter_today=None, reverse=False): #print(filter_today, 1667022171)
    filter={
                "all_members": { "$in": [ id_user ] },
              
            }
    if filter_today: 
        if reverse: filter.update(timestamp_Inactive(filter_today)) 
        else: filter.update(timestamp_Active(filter_today)) #{ "timestamp_end": { "$gt": int(filter_today)  }}) # только активные
    return [el for el in mongo_events_n_days_limit(30, 1000, 
                                            query=filter)]

class Init:
    def __init__(self, obj = None): 
        global api ; api = obj ; global processing ; processing = api.processing #initProccessing(api)
        self.router = router # ; protects=[time.time()]; 

    @router.post("/api/new_event") 
    async def answer(item: ItemEvent, r: Request): # print(item)
        return api.return_or_error(lambda: { "inserted_id": api.db.save_all_to_mongo(
                                            coll=MONGO_EVENTS_COLLECTION,
                                            key=None, # insert
                                            value=item.dict()) })
    @router.post("/api/update_event/{id_event}") 
    async def answer(item: ItemEvent, id_event: str, r: Request): # print(item)
        if id_event:
            update_data = item.dict()
            clear=["all_members", "approved_members","successed_members", "awarded_members", "user_reports", "_id"] # не редактируемые поля
            for t in clear:
                if t in update_data: del(update_data[t])
            return api.return_or_error(lambda: api.db.save_all_to_mongo(
                                                coll=MONGO_EVENTS_COLLECTION,
                                                #key=None, # insert
                                                update_by_id=id_event,
                                                value=update_data) )

    @router.get("/api/get_members_event/{id_event}")
    async def answer(id_event: str, r: Request): 
        return api.return_or_error(lambda: get_event_by_id(id_event) , err_text="Not Found")

    @router.get("/api/get_all_active_events")
    async def answer(): return api.return_or_error(
        lambda: mongo_events_n_days_limit(30,1000, 
                    query=timestamp_Active(time.time())
                ))

    @router.get("/api/get_all_inactive_events")
    async def answer(): return api.return_or_error(
        lambda: mongo_events_n_days_limit(30,1000, 
                    query=timestamp_Inactive(time.time())
                ))
    @router.get("/api/get_all_events")
    async def answer(): return api.return_or_error(
        lambda: mongo_events_n_days_limit(365,10000, #query=timestamp_Inactive(time.time())
                ))
    @router.get("/api/get_event/{id_event}")
    async def answer(id_event: str, r: Request): 
        return api.return_or_error(lambda: get_event_by_id(id_event), err_text="Not Found")

    # подписка пользователя на событие
    @router.post("/api/set_user_to_event")
    async def answer(request: Request): 
        try: return api.return_or_error(await update_event__add_user_to_member(request))
        except Exception as e: return api.def_err("Faild", error=e)
    # отписка пользователя от события
    @router.post("/api/del_user_from_event")
    async def answer(request: Request): 
        try: return api.return_or_error(await update_event__add_user_to_member(request, is_delete=True))
        except Exception as e: return api.def_err("Faild", error=e)

    # подтвердить пользователя как участника события
    @router.post("/api/set_member_to_approved")
    async def answer(request: Request): 
        try: return api.return_or_error(await from_level_to_level(request,
                                                                FROM_LEVEL='all_members',
                                                                TO_LEVEL='approved_members')) #await update_event__set_member_to_approved(request))
        except Exception as e: return api.def_err("Faild", error=e)
    # удалить пользователя как участника события
    @router.post("/api/del_member_from_approved")
    async def answer(request: Request): 
        try: return api.return_or_error(await from_level_to_level(request, is_delete=True,
                                                                FROM_LEVEL='all_members',
                                                                TO_LEVEL='approved_members')) #await update_event__set_member_to_approved(request, is_delete=True))
        except Exception as e: return api.def_err("Faild", error=e)
    # подтвердить что пользователь выполнил задание
    @router.post("/api/set_approved_to_success")
    async def answer(request: Request): 
        try: return api.return_or_error(await from_level_to_level(request, 
                                                            FROM_LEVEL='approved_members',
                                                            TO_LEVEL='successed_members')) #await update_event__set_member_to_approved(request))
        except Exception as e: return api.def_err("Faild", error=e)
    # отменить факт выполнения задания пользователем
    @router.post("/api/del_approved_from_successed")
    async def answer(request: Request): 
        try: return api.return_or_error(await from_level_to_level(request, is_delete=True,
                                                            FROM_LEVEL='approved_members',
                                                            TO_LEVEL='successed_members')) #await update_event__set_member_to_approved(request, is_delete=True))
        except Exception as e: return api.def_err("Faild", error=e)
    # подтвердить что награда выполенна пользователю
    @router.post("/api/set_successed_to_awarded")
    async def answer(request: Request): 
        try: return api.return_or_error(await from_level_to_level(request,
                                                            FROM_LEVEL='successed_members',
                                                            TO_LEVEL='awarded_members')) #await update_event__set_member_to_approved(request))
        except Exception as e: return api.def_err("Faild", error=e)
    # отменить факт выплаты награды пользователю
    @router.post("/api/del_successed_from_awarded")
    async def answer(request: Request): 
        try: return api.return_or_error(await from_level_to_level(request, is_delete=True,
                                                            FROM_LEVEL='successed_members',
                                                            TO_LEVEL='awarded_members')) #await update_event__set_member_to_approved(request, is_delete=True))
        except Exception as e: return api.def_err("Faild", error=e)

    # отчет по события
    @router.post("/api/user_report_event")
    async def answer(request: Request): 
        return api.return_or_error(await update_event__user_report_event(request))
        #except Exception as e: return api.def_err("Faild", error=e)
    # только активные пользоватя
    @router.get("/api/get_active_events/{id_user}")
    async def answer(id_user: int, r: Request): 
        return api.return_or_error(lambda: get_events_by_user_id(id_user, 
                                                                filter_today=time.time()))
                                                            
    # только НЕактивные пользователя
    @router.get("/api/get_inactive_events/{id_user}")
    async def answer(id_user: int, r: Request): 
        return api.return_or_error(lambda: get_events_by_user_id(id_user, 
                                                                filter_today=time.time(), 
                                                                reverse=True)) # неактивные
    # все события пользователя
    @router.get("/api/get_active_events_all/{id_user}")
    async def answer(id_user: int, r: Request): 
        return api.return_or_error(lambda: get_events_by_user_id(id_user))