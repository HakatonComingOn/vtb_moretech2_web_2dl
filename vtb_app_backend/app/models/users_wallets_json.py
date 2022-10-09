

import os
USER_DATA_FILE="db/test.json"
USER_WALLETS_FILE="db/testwallets.json"
BANK_ADDRESS = os.environ.get("BANK_ADDRESS", "") ; BANK_WALLET = os.environ.get("BANK_WALLET", "") 


#users = None
class UserModel:
    def __init__(self, api): 
        self.users=api.db.read_file(USER_DATA_FILE)["users"] #"auth/db/test.json")
        self.wallets = api.db.read_file(USER_WALLETS_FILE) ; 
        w=self.wallets["global_wallets"]; w["bank_address"] = {}
        w["bank_address"]["privateKey"] = BANK_WALLET ; w["bank_address"]["privateKey"] = BANK_ADDRESS  #; print(self.wallets)
    #@staticmethod
    def get_users(self): return self.users #['users']
#model=Model()


    def find_user_by_public_key(self, pk):
        for i, userkey in enumerate(self.wallets["users_wallets"]): #print(userkey["publicKey"].upper() , pk.upper())
            if userkey["publicKey"].upper() == pk.upper(): #print("found user", i)
                return i

    def wallet_by_user_id(self,id): 
        return self.wallets['users_wallets'][id]
        
    def user_by_address(self, address):
        return self.users[self.find_user_by_public_key(address)]

    def address_by_user_id(self, id_user): 
        return self.wallet_by_user_id((int(id_user)-1) or -1)["publicKey"]

