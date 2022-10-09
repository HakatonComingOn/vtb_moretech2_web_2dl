from fastapi import Response #, Form, Depends, UploadFile, File

from utils.storage import Storage; #db = Storage()
from utils.storage.mongo import Mongo #; m=Mongo()

class DB(Storage, Mongo): pass 
db = DB() 

#def FUNC(): 0
LAMBDA = lambda:0 ; type_lambda = type(LAMBDA); #type_func =  type(FUNC);
check_lambda_or_func = lambda v: isinstance(v, type_lambda) and v.__name__ == LAMBDA.__name__ or hasattr(v, '__call__') #isinstance(v, type_func)
lambda_or_content = lambda c: c if not check_lambda_or_func(c) else c()


class Api(Storage):
    def __init__(self): self.db = db

    @staticmethod
    def def_response(obj, ignore_string=False):
        return Response( content = '{"content":'+\
                    (obj if ignore_string and isinstance(obj, str) else db.def_json_dumps(obj)) +\
                    '}', media_type="application/json")

    @staticmethod
    def def_err(desc="Not Found", error=None, code=1):
        return  '{"content":[], "error": {'+f'"code":{code}, "desc": "{desc}"'+\
            ('' if not error else f',"info":"{error}"')+\
            '}}'
    #@staticmethod
    def return_or_error(self,content, err_text="Somthing wrong"):
        try: return self.def_response(lambda_or_content(content), ignore_string=True)
        except Exception as e: return self.def_err(err_text, error=e)