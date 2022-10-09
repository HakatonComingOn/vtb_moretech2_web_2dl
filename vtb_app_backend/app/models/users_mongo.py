

import os, time

USER_DATA_FILE="db/test.json"
USER_WALLETS_FILE="db/testwallets.json"
USER_ID_MONGO="db/testmongo_id.json"
BANK_ADDRESS = os.environ.get("BANK_ADDRESS", "") ; BANK_WALLET = os.environ.get("BANK_WALLET", "") 

api=None ; CACHE_USERS = {} ; wallets = None

MONGO_USERS_COLLECTION = "users"

def insert_user_to_mongo(v): return api.db.save_in_mongo(MONGO_USERS_COLLECTION, v)
def create_mongo_wallets(init_coins=0): return { "balance": { "coins": init_coins, "rub": init_coins, "nfts": [] }, "txs": [] }

# ПРЕДУСТАНОВЛЕННЫЕ ПОЛЬЗОВАТЕЛИ
def users_to_mongo():
    # кошельки
    global wallets
    wallets = api.db.read_file(USER_WALLETS_FILE) ; 
    w=wallets["global_wallets"]; w["bank_address"] = {}
    w["bank_address"]["privateKey"] = BANK_WALLET ; w["bank_address"]["publicKey"] = BANK_ADDRESS  
    # пользователи
    if not os.path.exists(USER_ID_MONGO):
        users=api.db.read_file(USER_DATA_FILE)["users"]
        try: mid=api.db.read_file(USER_ID_MONGO)
        except: mid=[]
        for i, user_data in enumerate(users):
            user_data.update({"user_id": i+1})
            user_data.update({"wallets": [wallets["users_wallets"][i]]})
            user_data["mongo_wallets"] = create_mongo_wallets(init_coins=1e6)
            if not i in mid:
                id = insert_user_to_mongo(user_data) ; mid.append(id)
        api.db.save_file(USER_ID_MONGO, mid)
    # get_users


from pydantic import BaseModel
from typing import Union, List, Optional

class Department(BaseModel):
    name: Union[ str, None] = None
    department_id: Union[ int, None] = None

class AddEdit_User(BaseModel):
    user_id:            Union[ int , None] = None
    name:               Union[ str , None] = None
    phone:              Union[ str, None] = None
    is_show_phone:      Union[ bool, None] = None
    telegram:           Union[ str, None] = None
    is_show_telegram:   Union[ bool, None] = None
    email:              Union[ str, None] = None
    is_show_email:      Union[ bool, None] = None
    role:               Union[ List[ str ], None] = None
    department:         Union[ Department, None] = Department()
    job_title:          Union[ str, None] = None

#  {
#             "date": "2022-10-09 02:22:26.668000",
#             "user_id": 3,
#             "name": "Имя",
#             "phone": "8-800-555-0000",
#             "is_show_phone": true,
#             "telegram": "@darya",
#             "is_show_telegram": false,
#             "email": "test@test.ru",
#             "is_show_email": true,
#             "role": [
#                 "user"
#             ],
#             "department": {
#                 "name": "design",
#                 "department_id": 2
#             },
#             "job_title": "designer",
#             ]
#         }


#users = None
class UserModel:
    def __init__(self, API): 
        global api ; api = API ; users_to_mongo() # default users to mongo
        #print(self.get_users())
        #print(self.get_user(1))
        #exit()
    @staticmethod
    def precache_users(res):
        CACHE_USERS=[ [el["user_id"], str(el["_id"])] for el in res]
        CACHE_USERS.sort(key=lambda x: x[0]) #, reverse=True)
        print(CACHE_USERS[-1], len(CACHE_USERS)) # last user
        return CACHE_USERS

    #@staticmethod
    def lastID(self): return len(self.get_users())

    #@staticmethod
    def get_users(self, x=None): 
        res = api.db.mongo_universal_search_x(MONGO_USERS_COLLECTION, x)
        if not x: self.precache_users(res)
        return res
    def get_user(self, id): return self.get_users({ "user_id": id })[0]
        #return self.users #['users']
#model=Model()
        

    def find_user_by_public_key(self, pk):
        return self.get_user({"wallets.0.publicKey": pk.upper()})
    def find_user_by_private_key(self, pk):
        return self.get_user({"wallets.0.privateKey": pk.upper()})
        # for i, userkey in enumerate(self.wallets["users_wallets"]): #print(userkey["publicKey"].upper() , pk.upper())
        #     if userkey["publicKey"].upper() == pk.upper(): #print("found user", i)
        #         return i

    def wallet_by_user_id(self,id): 
        #return self.wallets['users_wallets'][id]
        return self.get_user(id)['wallets'][0]
        
    def user_by_address(self, address):
        return self.find_user_by_public_key(address) #self.users[self.find_user_by_public_key(address)]

    def address_by_user_id(self, id_user): 
        return self.wallet_by_user_id((int(id_user)-1) or -1)["publicKey"]

    def create_users(self, objs):
        lastid = self.lastID() ; inserted = []
        for user_data in objs:
            lastid += 1 ; user_data.update({"user_id": lastid})
            wallet = api.processing.create_wallet() #print(wallet)
            if wallet["error"] == 0 and wallet:
                wallet = wallet["content"]
                user_data["wallets"]=[wallet]
                user_data["mongo_wallets"]= create_mongo_wallets() # virtual wallets
                id = insert_user_to_mongo(user_data)
                inserted.append({"id":{ "user_id":lastid, "mongoId":id, "name":user_data["name"]}, "wallet": wallet, "mongo_wallets": user_data["mongo_wallets"] })
        return inserted
    
    @staticmethod
    def global_wallets(): return wallets["global_wallets"]
    def bank_wallet(self): return self.global_wallets()['bank_address'] 
    def create_user_wallet(self, user): return self.create_users([user])
    def update_user_by_mongoid(self, id, update_data):
        api.db.save_all_to_mongo( coll=MONGO_USERS_COLLECTION,
                                                update_by_id=id,
                                                value=update_data)
        return update_data

    def balance_mongo_coin(self, user):
        return user["mongo_wallets"]["balance"]["coins"]
    def balance_mongo_coin_by_address(self, user_address):
        return self.balance_mongo_coin(self.user_by_address(user_address))
    def balance_mongo_coin_by_user_id(self, user_id):
        return self.balance_mongo_coin(self.get_user(user_id))
    # def balance_mongo_coin(self, user, n):
    #     return user["mongo_wallets"][0]["coin"]
    # самописная отправка транзакций
    def send_mongo_coin(self, obj, by_id=False):
        tx = {}
        if by_id:
            from_ = self.get_user(obj['id_user_from'])
            to_ = self.get_user(obj['id_user_to'])
        else: # by_address
            from_ = self.find_user_by_private_key(obj['fromPrivateKey'])
            to_ = self.find_user_by_public_key(obj['toPublicKey'])
        amount = obj['amount']
        balance = self.balance_mongo_coin(from_)
        obj["timestamp"] = time.time()
        tx["info"] = obj
        tx["before"] = [from_["mongo_wallets"]["balance"], to_["mongo_wallets"]["balance"]]
        if balance > amount: # условие отправки
            from_["mongo_wallets"]["balance"]["coins"] -= amount
            to_["mongo_wallets"]["balance"]["coins"] += amount
            # сохранение транзакции в системе
            err = False
            try:
                # TODO: контроль записи в бд
                res = self.update_user_by_mongoid(from_["_id"], from_)
                res = self.update_user_by_mongoid(to_["_id"], to_)
            except Exception as e:
                print(e)
                err=True
            tx["after"]=[from_["mongo_wallets"]["balance"], to_["mongo_wallets"]["balance"]]
            tx["error"]=err

             # save tx
            to_["mongo_wallets"]["txs"].insert(0, tx)
            from_["mongo_wallets"]["txs"].insert(0, tx)
            try:
                # TODO: контроль записи в бд
                res = self.update_user_by_mongoid(from_["_id"], from_)
                res = self.update_user_by_mongoid(to_["_id"], to_)
            except Exception as e:
                print(e)
                err=True   
            return tx
    def recharge_mongo_coin_by_iduser(self, id_user, amount):
        print("recharge_mongo_coin_by_iduser")
        tx={}
        to_ = self.get_user(id_user)
        to_["mongo_wallets"]["balance"]["coins"] += amount
        err = False
        tx["info"] = { "amount": amount , "timestamp": time.time() }
        tx["before"] = [ to_["mongo_wallets"]["balance"] ]
        try:
            # TODO: контроль записи в бд
            res = self.update_user_by_mongoid(to_["_id"], to_)
            pass
        except Exception as e:
            print(e)
            err=True
        tx["after"]=[ to_["mongo_wallets"]["balance"] ]
        tx["error"]=err
        
        # save tx
        to_["mongo_wallets"]["txs"].insert(0, tx)
        try:
            # TODO: контроль записи в бд
            res = self.update_user_by_mongoid(to_["_id"], to_)
            pass
        except Exception as e:
            print(e)
            err=True
        return tx

    def find_user_in_users_list_by_id(self, users, id, by_id=True, limit=300):
        count = 0
        for el in users:
            count +=1
            if by_id:
                if el['user_id'] == id: return el
            else:
                if el['wallets'][0]['publicKey'] == id or el['wallets'][0]['privateKey'] == id:
                    return el
            if count >= limit: return 

    def history_mongo_coin_by_iduser(self, id_user, by_id=True, full_user_info=True, limit=200):
        if by_id:
            to_ = self.get_user(id_user)
        else: # by_address
            to_ = self.find_user_by_public_key(id_user)
        txs=to_["mongo_wallets"]["txs"]
        if full_user_info:
            users=self.get_users()
            txs_user_full_info=[]
            count=0
            for tx in txs:
                count+=1
                user_from= None ; user_to=None
                try:
                    if 'id_user_from' in tx['info']: # by id
                        user_from = self.find_user_in_users_list_by_id(users, tx['info']['id_user_from'])
                        user_to = self.find_user_in_users_list_by_id(users, tx['info']['id_user_to'])
                    elif 'toPublicKey' in tx['info']: # by hash
                        user_from = self.find_user_in_users_list_by_id(users, tx['info']['fromPrivateKey'], by_id=False)
                        user_to = self.find_user_in_users_list_by_id(users, tx['info']['toPublicKey'], by_id=False)
                except: pass
                tx['users']={ "from": user_from, "to": user_to}
                txs_user_full_info.append(tx)
                if count>limit: break

            return txs_user_full_info
        return txs