from fastapi import APIRouter, Request #, Depends, HTTPException, Header #, Form, Depends, UploadFile, File
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse, HTMLResponse, Response

router = APIRouter( prefix="", tags=[], dependencies=[], responses={},) ; api = None

from models.users_mongo import AddEdit_User

# import time, httpx

#from utils.storage import Storage; db = Storage()


#users=db.read_file("auth/db/test.json")

# /get_user post body {id} resp IUser

# /auth post body {id} resp IUser

# /transactions_all get 

# /user_transactions post body {id} resp IUserTransactions

# /create_event post

# users = None
# class Model:
#     @staticmethod
#     def get_users(): return users['users']

# from models.users_wallets_json import UserModel ; user_model=None

# from models.users_mongo import UserModel as Mark2 

#print(model.get_users())

# def def_response(obj):
#     return Response( content = '{"content":'+ db.def_json_dumps(obj) +'}', 
#                      media_type="application/json")
# def def_err(desc="Not Found", error=None, code=1):
#     return  '{"content":[], "error": {'+f'"code":{code}, "desc": "{desc}"'+\
#             ('' if not error else f',"info":"{error}"')+\
#             '}}'

def get_user_by_id(id): return api.def_err("Not Found") if not id else user_model.get_users()[id-1]

class Init:
    #@staticmethod
    #def get_router(): return router
    def __init__(self, obj = None): 
        global api, user_model ; api = obj # ; protects=[time.time()]; 
        user_model= api.user_model  #UserModel(api) #users=api.db.read_file("auth/db/test.json")
        self.router=router


        #x=Mark2(api)

    @router.get("/api/get_users")
    async def answer(r: Request): return api.return_or_error(user_model.get_users())
        # try: return api.def_response(user_model.get_users())
        # except Exception as e: return api.def_err("Somthing wrong", error=e)



    @router.get("/api/get_user/{id}")
    async def answer(id: int, r: Request): 
        #return api.return_or_error(lambda: api.def_err("Not Found") if not id else user_model.get_users()[id-1], err_text="Not Found")
        return api.return_or_error(lambda: get_user_by_id(id), err_text="Not Found")
        # try: return api.def_err("Not Found") if not id else api.def_response(user_model.get_users()[id-1])
        # except: return api.def_err("Not Found")

    @router.post("/api/auth/")
    async def answer(request: Request):  
        # return api.return_or_error(
        #     lambda: get_user_by_id(int((await request.json())['id'])), err_text="Not Found")
        try: 
            id=int((await request.json())['id']) # print(id) # body
            return api.return_or_error(lambda: get_user_by_id(id), err_text="Not Found")
        #return api.def_err("Not Found") if not id else api.def_response(user_model.get_users()[id-1])
        except: return api.def_err("Not Found")

    @router.post("/api/new_user_wallert")
    async def answer(item: AddEdit_User): 
        data = item.dict()
        if "id" in data: del(data["id"]) # запрет на редактирование
        #return api.user_model.create_user_wallet(data)
        return api.return_or_error(lambda: api.user_model.create_user_wallet(data), err_text="Error")
    
    @router.post("/api/edit_user_by_id/{id_user}")
    async def answer(item: AddEdit_User, id_user: int): 
        update_data = item.dict()
        try: old_data = api.user_model.get_user(id_user)
        except: old_data = None
        if not old_data or not 'user_id' in old_data: api.def_err("Not Found")
        else: 
            id = old_data["_id"]
            if "user_id" in update_data: del(update_data["user_id"]) # запрет на редактирование
            if "_id" in update_data: del(update_data["_id"]) # запрет на редактирование
            return api.return_or_error(lambda: api.user_model.update_user_by_mongoid(id, update_data), err_text="Error")
        api.def_err("Somthing wrong")

    