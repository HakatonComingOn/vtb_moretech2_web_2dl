

# маркетплейс реализован в событиях events

# мы решили применять технологию и принципы блокчейн 
# и создать уневерсальный обьект, который создает экосистему, 
# на подобии универсального trello, где функции , 
# условия, награды могут переплетаться между собой



# мы решили не заниматься копипастингом, т.к. обьекты и данные, 
# и возможности в нашей идее схожие у всех сущностей

# проект легко расширяем, но сейчас нам нужно показать лишь mvp и идею
# разработать продукт



from pydantic import BaseModel
from typing import Union, List, Optional


class SearchObject(BaseModel):
    # ТИП ЭЛЕМЕНТА / ТЕГ / КАТЕГОРИЯ ТОВАРА
    CATEGORY:           Union[ List[str] , None] = [].copy()
    TYPE:               Union[ List[str] , None] = [].copy()
    days_back:          Union[ int , None] = 0
    limit:              Union[ int , None] = 0
    id_user:            Union[ List[int] , None] = 0

    #time_start:         Union[int, None] = None
    #time_end:           Union[int, None] = None

    # другие опции для поиска ...