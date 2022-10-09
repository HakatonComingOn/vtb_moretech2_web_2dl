


from pydantic import BaseModel
from typing import Union, List, Optional




class Creator(BaseModel):
    id:     Union[int, None] = None
    role:   Union[str, None] = None

class Reward(BaseModel):
    rub:    Union[float, None] = 0
    nfts:   Union[ List[int], None ] = [].copy()


class UserMessage(BaseModel):
    timestamp:    Union[float, None] = None    
    text:   Union[ str, None ] = ""

class UserReport(BaseModel):
    id_user: Union[ int, None ] = None
    messages: Union[ List[ UserMessage ] , None ] = [].copy()

# class UsersReports(BaseModel):
#     reports: Union[ List[ UserReport ], None ] = [].copy()

# ЭЛЕМЕНТ МАРКЕТПЛЕЙСА
class Image(BaseModel):
    id: Union[str, None] = None
    title: Union[str, None] = None
    type: Union[str, None] = None
    url: Union[str, None] = None

class Albom(BaseModel):
    id: Union[str, None] = None
    title: Union[str, None] = None
    imgs: Union[ List[ Image ], None ] = [].copy()

class Price(BaseModel):
    coins: Union[float, None] = None
    rub: Union[float, None] = None
    nfts: Union[ List[int] , None] = None

class ItemEvent(BaseModel):
    # info
    id:                 Union[str, None] = None
    title:              Union[str, None] = None
    description:        Union[str, None] = None
    text:               Union[str, None] = None
    # ТИП ЭЛЕМЕНТА / ТЕГ / КАТЕГОРИЯ ТОВАРА
    # категория - разделитель данных
    CATEGORY:           Union[ List[str] , None] = [].copy()
    TYPE:               Union[ List[str] , None] = [].copy()
    # ЭЛЕМЕНТЫ МАРКЕТПЛЕЙСА
    imgs_urls_alboms:        Union[ List[Albom] , None] = [].copy()
    # ПОДДЕРЖКА краудфайндинга, раздееления ценны
    PRICES:             Union[ List[Price] , None] = [].copy()
    # ПРАВА получения товара, события, обучения
    ACCESS_RULES:       Union[ List[str] , None] = [].copy()
    # связность с NFT
    LINK_TO_NFT:        Union[ List[str] , None] = [].copy()
    # access
    filter_params:      Union[ List[str], None ] = [].copy() #float, None] = None  #(ALL, DEPARTMENT, BY_USER)  
    max_count_members:  Union[int, None] = 0
    all_members:        Union[ List[int], None ] = [].copy() 
    approved_members:   Union[ List[int], None ] = [].copy()
    successed_members:  Union[ List[int], None ] = [].copy()
    awarded_members:    Union[ List[int], None ] = [].copy()
    # deadline
    date_start:         Union[str, None] = None 
    date_end:           Union[str, None] = None
    timestamp_start:    Union[float, None] = None 
    timestamp_end:      Union[float, None] = None
    # controls
    creator:            Union[ Creator, None ] = Creator() #= None
    # creator
    rewards:            Union[ List[ Reward ], None] = [].copy() # = True 
    user_reports:       Union[ List[ UserReport ], None ] = [].copy()
    # s
    user_must_send_reports:  Union[bool, None] = False # необходимы отчеты
    # statuses
    status:                  Union[str, None] = None # string (offline / online);




# /new_event post
# /get_members_event/event_id get
# /get_all_active_events get
# /get_all_inactive_events get
# /get_event/id get
# /set_user_to_event post body{user_id}
# /get_active_events/user_id get

# event {

# // info
#   id: number;
#   title: string;
#   description: string;
#   text: string;

# // access
#   filter_params: string[]; (ALL, DEPARTMENT, BY_USER)  
#   max_count_members: number;
#   all_members: user_id[];
#   approved_members: user_id[];


# // deadline
#   date_start: string;
#   date_end: string;

# // control
#   creator: {
#     id: user_id;
#     role: string (user_role);
#   };

# // rewards
#   reward: {
#     rub: number;
#     nft: nft_id;
#   }[];

#   user_must_reports: true, // необходимы отчеты

# // statuses
#   status: string (offline / online);
  
# }


# {

#   "id": 1,
#   "title": "title",
#   "description": "desc",
#   "text": "text",
#   "filter_params": ["test"],  
#   "max_count_members": 10,
#   "all_members": [1],
#   "approved_members": [1],
#   "date_start": "",
#   "date_end": "",
#   "creator": {
#     "id": 1,
#     "role": "test"
#   },
#   "rewards": [{
#     "rub": 1.1,
#     "nfts": [1,2,3]
#   }],
#   "user_must_send_reports": true, 
#   "status": "test"
# }