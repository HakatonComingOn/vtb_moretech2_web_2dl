
import httpx, os, pytz
from datetime import datetime
from dotenv import load_dotenv; load_dotenv(verbose=True); os.environ['TZ'] = os.getenv("TZ") or 'Europe/Moscow' ; 


def timestamp_to_date_with_tz(ts): #utc_dt = datetime.utcfromtimestamp(ts)
    tz = pytz.timezone(os.environ['TZ'])
    return datetime.fromtimestamp(ts, tz)

BASE_MATIC_API_URL = os.environ.get("MATIC_API", "https://hackathon.lsp.team/hk") ; wallets=None
MATIC_RUB_CONVERT = float(os.environ.get("MATIC_RUB_CONVERT",0.00000034))
MATIC_TO_FLOAT = 1e18

# interface
def matic_url(route, get=None, post=None):
    if route == "history": return "POST", f"{BASE_MATIC_API_URL}/v1/wallets/{get['address']}/history", post
    if route == "balance": return "GET", f"{BASE_MATIC_API_URL}/v1/wallets/{get['address']}/balance", post
    if route == "balance_nft": return "GET", f"{BASE_MATIC_API_URL}/v1/wallets/{get['address']}/nft/balance", post
    if route == "create_wallet": return "POST", f"{BASE_MATIC_API_URL}/v1/wallets/new" , post 
    if route == "generate_nfts": return "POST", f"{BASE_MATIC_API_URL}/v1/nft/generate" , post # {{baseUrl}}/v1/nft/generate
    if route == "tx_status_by_hash": return "GET", f"{BASE_MATIC_API_URL}/v1/wallets/status/{get['hash']}" , post # {{baseUrl}}/v1/transfers/status/:transactionHash
    if route == "check_list_nfts_by_hash": return "GET", f"{BASE_MATIC_API_URL}/v1/nft/generate/{get['hash']}" , post # {{baseUrl}}/v1/nft/generate/:transactionHash
    if route == "send_matic": return "POST", f"{BASE_MATIC_API_URL}/v1/transfers/matic", post # BAD
    if route == "send_ruble": return "POST", f"{BASE_MATIC_API_URL}/v1/transfers/ruble", post # GOOD
    if route == "send_nft": return "POST", f"{BASE_MATIC_API_URL}/v1/transfers/nft", post # GOOD
    if route == "nft_info_by_id": return "GET", f"{BASE_MATIC_API_URL}/v1/nft/{get['id']}", post # {{baseUrl}}/v1/nft/:tokenId

# wrapper
def req(req, timeout=120):
    try:
        try:
            if req[0] == "POST": r = httpx.post(req[1], data=req[2], timeout=timeout)
            else: r = httpx.get(req[1], timeout=timeout)
        except Exception as e: return {"error": 1, "info": e, "req": req }
        try: j = r.json()
        except: j = None
        return {"error": 0 if r.status_code==200 else 2, "code":r.status_code, "content": j, "req": req } 
    except Exception as e: return {"error": 3, "info": e, "req": req}
    
def route_matic(route, get=None, post=None): return req(matic_url(route, get, post))

        # {
        #     "hash": "0x139150444c3ecc1a939af0b4db9012376a51e4e53c4c9528d49b81b0893ba475",
        #     "blockNumber": 28498909,
        #     "timeStamp": 1665172570,
        #     "contractAddress": "",
        #     "from": "0xedaf4083f29753753d0cd6c3c50aceb08c87b5bd",
        #     "to": "0x3d65cc70dd616e096f0580f7b2f4bd3c2d0c6c44",
        #     "value": 500000000000000000,
        #     "tokenName": "MATIC",
        #     "tokenSymbol": "MATIC",
        #     "gasUsed": 21000,
        #     "confirmations": 12558,
        #     "isError": "0"
        # },

#from models.user_wallets import UserModel

#users=None ; user_model = None
class InitProccessing:
    def __init__(self, api):
        # global wallets ; wallets = api.db.read_file("db/testwallets.json") ; 
        # w=wallets["global_wallets"]; w["bank_address"] = {}
        # w["bank_address"]["privateKey"] = BANK_WALLET ; w["bank_address"]["privateKey"] = BANK_ADDRESS
        # global users ; users = api.db.read_file("db/test.json")
        #global user_model ; 
        self.user_model = api.user_model #UserModel(api)
        #self.users = user_model.get_users()
    @staticmethod
    def route_matic_getpost(route, obj=None): return route_matic(route, obj, obj)
    
    # баланс с таймаутом, (> 60 сек)
    def balance_nft(self,address): return self.route_matic_getpost("balance_nft", {"address": address}) 
    def balance(self,address): return self.route_matic_getpost("balance", {"address": address})

    def create_wallet(self): return self.route_matic_getpost("create_wallet")
    def tx_status(self, hash): return self.route_matic_getpost("tx_status_by_hash",{"hash":hash}) # status
    def check_list_nfts_by_hash(self, hash): return self.route_matic_getpost("check_list_nfts_by_hash",{"hash":hash}) # list
    def nft_info_by_id(self, id): return self.route_matic_getpost("nft_info_by_id",{"id":id}) # info
    def generate_nfts(self, url,  address, count=5,): return self.route_matic_getpost("generate_nfts",{
                                                "toPublicKey": address,
                                                "uri": url,
                                                "nftCount": min(int(count), 20)
                                                }) # info
    def send_ruble(self, from_, to_, amount): return self.route_matic_getpost("send_ruble",{
                                                    "fromPrivateKey": from_,
                                                    "toPublicKey": to_,
                                                    "amount": int(amount)
                                                }) # info
    def send_nft(self, from_, to_, amount): return self.route_matic_getpost("send_nft",{
                                                    "fromPrivateKey": from_,
                                                    "toPublicKey": to_,
                                                    "amount": int(amount)
                                                }) # info
    def send_matic(self, from_, to_, amount): return self.route_matic_getpost("send_matic",{
                                                    "fromPrivateKey": from_,
                                                    "toPublicKey": to_,
                                                    "amount": int(amount)
                                                }) # info
    def send_mongo_coin(self, from_, to_, amount): return self.user_model.send_mongo_coin({
                                                    "fromPrivateKey": from_,
                                                    "toPublicKey": to_,
                                                    "amount": amount
                                                }) # info
    def send_mongo_coin_by_iduser(self, from_, to_, amount): return self.user_model.send_mongo_coin({
                                                    "id_user_from": from_,
                                                    "id_user_to": to_,
                                                    "amount": amount,
                                                    
                                                }, by_id=True) # info

    # @staticmethod
    # def route_matic_getpost_format(route, obj=None): return format_history(route_matic(route, obj, obj))
    #@staticmethod
    #def wallet_by_user(id): return user_model.wallet_by_user_id(int(id)-1) #wallets['users_wallets'][int(id)-1]
    #@staticmethod
    def format_history(self,history):
        history_formated=[]
        for tx in history: # print(tx)
            try:
                user_from = None; user_to = None
                try: user_from = self.user_model.user_by_address(tx["from"])
                except: pass
                try: user_to = self.user_model.user_by_address(tx["to"])
                except: pass
                val_matic = float(tx["value"]) / MATIC_TO_FLOAT
                val_drub = ( val_matic / MATIC_RUB_CONVERT ) 
                history_formated.append({
                    "user_from": user_from,
                    "user_to": user_to,
                    "value_matic": val_matic,
                    "value_rub": val_drub,
                    "error": tx["isError"],
                    "timestamp": tx["timeStamp"],
                    "date": timestamp_to_date_with_tz(tx["timeStamp"]),
                })
            except: pass
        return history_formated


# print(req(matic_url(route ="send_matic")))
# print( route_matic( # req(matic_url(
#                     route ="history", 
#                     get={
#                         "address":"0x3D65Cc70Dd616E096f0580F7b2f4Bd3c2d0C6C44"
#                         },
#                     post={
#                         "page": 0,
#                         "offset": 100,
#                         "sort": "asc"
#                     }
#                     )) #)