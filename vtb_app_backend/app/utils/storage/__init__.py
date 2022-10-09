
from utils.storage.save_file import AsyncFiles
import ujson

class Storage(AsyncFiles):
    @staticmethod
    def def_json_dumps(data): #, ignore_string=False):
        #if ignore_string and isinstance(data, str): return data # string
        return ujson.dumps(data, ensure_ascii=False, default=str) # or json