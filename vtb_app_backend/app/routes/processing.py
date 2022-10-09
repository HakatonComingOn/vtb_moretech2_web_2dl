from fastapi import APIRouter, Request
# import time, httpx

router = APIRouter( prefix="", tags=[], dependencies=[], responses={},) ; api = None

# /transactions_all get 

# /user_transactions post body {id} resp IUserTransactions

# /create_event post

#from service.processing import initProccessing; 

from pydantic import BaseModel
from typing import Union, List, Optional


class SendMongoCoin(BaseModel):
    fromPrivateKey:           Union[ str , None] = None
    toPublicKey:              Union[ str, None] = None
    amount:                   Union[ int , None] = 0

class SendMongoCoin_by_iduser(BaseModel):
    id_user_from:               Union[ int , None] = None
    id_user_to:                 Union[ int, None] = None
    amount:                     Union[ int , None] = 0

# def address_by_user_id(id_user): 
#     return processing.user_model.wallet_by_user_id((int(id_user)-1) or -1)["publicKey"]

def history_by_id(id_user, show_source=False):
    res=processing.route_matic_getpost( "history", {
                "address": processing.user_model.address_by_user_id(id_user), #"0x3D65Cc70Dd616E096f0580F7b2f4Bd3c2d0C6C44",
                "page": 0,
                "offset": 100,
                "sort": "asc"
    } )
    if not "error" in res or res["error"]==0: res=res["content"]["history"]
    return res if show_source else processing.format_history(res)

def balance_by_id(id_user, show_source=False):
    bal=processing.route_matic_getpost( "balance", { "address": processing.user_model.address_by_user_id(id_user),  } )
    bal_nft=processing.route_matic_getpost( "balance_nft", { "address": processing.user_model.address_by_user_id(id_user),  } )
    if not "error" in bal_nft or bal_nft["error"]==0: bal_nft=bal_nft["content"]["balance"]
    bal = { "balance": bal["content"] , "balance_nft": bal_nft }
    return bal



class Init:
    #@staticmethod
    #def get_router(): return router
    def __init__(self, obj = None): 
        global api ; api = obj # ; protects=[time.time()]; 
        global processing ; processing = api.processing #initProccessing(api)
        self.router = router #return router

        #print("create_wallet",api.processing.create_wallet())
        rub_from = api.user_model.bank_wallet()["privateKey"]; print(rub_from)
        rub_to = api.user_model.get_user(id=3)["wallets"][0]["publicKey"] ; print(rub_to)
        nft_from = api.user_model.get_user(id=3)["wallets"][0]["privateKey"] ; print(nft_from)
        nft_from_address = rub_to
        nft_to = api.user_model.get_user(id=1)["wallets"][0]["publicKey"] ; print(nft_to)
        matic_from = api.user_model.get_user(id=1)["wallets"][0]["privateKey"] ; print(matic_from)
        matic_to = nft_to ; print(matic_to)
        mongo_coin_from = nft_from
        mongo_coin_to = nft_to
        hash = "0x03f78d396047b5829a5401ed5ca6abc53c952e2204a21aa432ff6b90a008b183"  #"0xb70a15e68d07b792785921d13e0bd677231b24d4b3e33aef45427c19de01bf99"))
        user_publicAddress = api.user_model.address_by_user_id(1)
        nft_url = "http://"
        nft_len = 5
        nft_id = 2421 # 10

        ###################################
        # # SEND NFT CHECK
        # res = api.processing.balance_nft(nft_from_address)
        # # balance_nft {'error': 0, 'code': 200, 'content': {'balance': [{'uri': 'http://', 'tokens': 
        # # [2406, 2407, 2408, 2409, 2410, 2411, 2412, 2413, 2414, 2415, 2416, 2417, 2418, 2419, 2420, 2421, 2422, 2423, 2424, 2425, 2426, 2427, 2428, 2429, 2430, 2433, 2434, 2435, 2436, 2437, 2438, 2439, 2440, 2441, 2442, 2443, 2444, 2445, 2446, 2447, 2448, 2449, 2450, 2451, 2452, 2454, 2455, 2456, 2457, 2458, 2459, 2460, 2461, 2462, 2463, 2464, 2465, 2466, 2467, 2468]}]}, 'req': ('GET', 'https://hackathon.lsp.team/hk/v1/wallets/0x3D65Cc70Dd616E096f0580F7b2f4Bd3c2d0C6C44/nft/balance', {'address': '0x3D65Cc70Dd616E096f0580F7b2f4Bd3c2d0C6C44'})}
        # res = api.processing.send_nft(nft_from, nft_to, 2410) # 'content': {'transaction_hash'
        # print('send_nft', res) 
        # print("tx_status",api.processing.tx_status(res["content"]["transaction_hash"]))
        # print('balance_nft', api.processing.balance_nft(nft_to))
        ###################################

        ###################################
        # # # SEND RUB CHECK
        # res = processing.send_ruble(rub_from, rub_to, 100)
        # print("send_ruble", res)
        # print("tx_status",api.processing.tx_status(res["content"]["transaction"]))
        # print("balance",  processing.balance(rub_to))
        # exit()
        ###################################

        # ##################################
        # # # SEND MATIC CHECK
        # res = processing.send_matic(matic_from, matic_to, 0.00034) # 1000 р
        # print("send_matic", res)
        # print("tx_status",api.processing.tx_status(res["content"]["transaction"]))
        # print("balance",  processing.balance(matic_to))
        # exit()
        # ##################################

        # work
        # ##################################
        # # # SEND MONGO COIN
        # res = processing.send_mongo_coin(mongo_coin_from, mongo_coin_to, 1) # 1000 р
        # print("send_mongo_coin", res)
        # print("balance_mongo_coin",api.user_model.balance_mongo_coin_by_address(mongo_coin_to))
        # exit()
        # ##################################

        # print("tx_status",api.processing.tx_status(hash)) #["status"] # 404 500
        # print("check_list_nfts_by_hash",api.processing.check_list_nfts_by_hash(hash)) # ["content"] 'wallet_id': 'tokens': [2421, 2422, 2423, 2424, 2425]
        # print("generate_nfts",api.processing.generate_nfts(nft_url, user_publicAddress, nft_len)) #['content']['transaction_hash']
        # print("nft_info_by_id",api.processing.nft_info_by_id( nft_id )) # ["content"] #{'tokenId': '10', 'uri': 'https://bafkreiet3nm3cny4hpvzki5645645fpnl57ehy.ipfs.nftstorage.link11', 'publicKey': '0x691533f28F603abB1c76F8AC8134176dCA76fbD5'}
        # exit()

        #print('balance_nft', res)
        #exit()



        # send_nft(nft_from, nft_to, )
        # send_matic()
        # send_mongo_coin()

    @router.get("/api/history/{id_user}")
    async def answer(id_user: int, r: Request): 
        return api.return_or_error(lambda: history_by_id(id_user))
    
    @router.get("/api/history_source/{id_user}")
    async def answer(id_user: int, r: Request): 
        return api.return_or_error(lambda: history_by_id(id_user,  show_source=True))
    
    @router.get("/api/balance/{id_user}")
    async def answer(id_user: int, r: Request): 
        return api.return_or_error(lambda: balance_by_id(id_user))

    ############################

    # отправка через БД
    @router.get("/api/mongo_coin/balance_by_id_user/{id_user}")
    async def answer(id_user: int, r: Request): 
        return api.return_or_error(
            lambda: api.user_model.balance_mongo_coin_by_user_id(id_user)) #balance_by_id(id_user))

    # отправка через БД
    @router.get("/api/mongo_coin/balance_by_public_key/{address}")
    async def answer(address: str, r: Request): 
        return api.return_or_error(
            lambda: api.user_model.balance_mongo_coin_by_address(address)) #balance_by_id(id_user))


    # отправка через БД
    @router.post("/api/mongo_coin/send_coin_by_keys")
    async def answer(obj: SendMongoCoin, r: Request): 
        try:
            data=obj.dict()
            res=processing.send_mongo_coin( data['fromPrivateKey'], 
                                            data['toPublicKey'], 
                                            data['amount'])
            return api.return_or_error(res) #balance_by_id(id_user))
        except Exception as e: return api.def_err("Faild", error=e)

    # отправка через БД
    @router.post("/api/mongo_coin/send_coin_by_id_user")
    async def answer(obj: SendMongoCoin_by_iduser, r: Request): 
        try:
            data=obj.dict()
            res=processing.send_mongo_coin_by_iduser( data['id_user_from'], 
                                                      data['id_user_to'], 
                                                      data['amount'])
            return api.return_or_error(res) #balance_by_id(id_user))
        except Exception as e: return api.def_err("Faild", error=e)

    # отправка через БД
    @router.get("/api/mongo_coin/history_by_id_user/{id_user}")
    async def answer(id_user: int, r: Request): 
        try: return api.return_or_error(lambda: api.user_model.history_mongo_coin_by_iduser( id_user , by_id = True))
        except Exception as e: return api.def_err("Faild", error=e)

    #}/api/mongo_coin/history_by_id_user_with_fullinfo/:id_user
    # отправка через БД
    @router.get("/api/mongo_coin/history_by_id_user_with_fullinfo/{id_user}")
    async def answer(id_user: int, r: Request): 
        try: return api.return_or_error(lambda: api.user_model.history_mongo_coin_by_iduser( 
                                        id_user , 
                                        by_id = True, 
                                        full_user_info=True ))
        except Exception as e: return api.def_err("Faild", error=e)




    # отправка через БД
    @router.get("/api/mongo_coin/history_by_id_address/{address}")
    async def answer(address: str, r: Request): 
        try: return api.return_or_error(lambda: api.user_model.history_mongo_coin_by_iduser( address , by_id = False))
        except Exception as e: return api.def_err("Faild", error=e)

     # отправка через БД
    @router.post("/api/mongo_coin/recharge_by_id_user")
    async def answer( r: Request): 
        #try: 
        try: 
            amount = (await r.json())
            id_user=amount['id_user']
            amount=amount['amount']
            return api.return_or_error(lambda: api.user_model.recharge_mongo_coin_by_iduser( id_user , amount=amount))
        except Exception as e: return api.def_err("Faild", error=e)

 