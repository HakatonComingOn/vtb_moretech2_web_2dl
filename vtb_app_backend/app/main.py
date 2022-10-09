import os, sys, time, datetime; from dotenv import load_dotenv; 
load_dotenv(verbose=True); os.environ['TZ'] = os.getenv("TZ") or 'Europe/Moscow' ; sys.path.append('./') ; sys.path.append('../')

import uvicorn
from fastapi import FastAPI #, Request, Response #, Form, Depends, UploadFile, File
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import Union
# from fastapi_utils.tasks import repeat_every
#from fastapi.staticfiles import StaticFiles
#from starlette.responses import StreamingResponse
#from fastapi.templating import Jinja2Templates

app = FastAPI() #docs_url=None, redoc_url=None, openapi_url=None); app.openapi = None
#app.mount("/static", StaticFiles(directory="dumps"), name="static"); #templates = Jinja2Templates(directory="templates"); #app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware( CORSMiddleware,
    allow_origins=["*"],  allow_credentials=True,  allow_methods=["*"],  allow_headers=["*"], )

# ROUTES
from utils.api.api import Api; api = Api() ; 
#from models.users_wallets_json import UserModel ; api.user_model=UserModel(api)
from models.users_mongo import UserModel as Mark2 ; api.user_model=Mark2(api)
from service.processing import InitProccessing; api.processing = InitProccessing(api) #processing=None 
from routes import processing, auth, events, market

app.include_router(auth.Init(api).router) # авторизация, пользователи, кошельки
app.include_router(processing.Init(api).router) # процессинг
app.include_router(events.Init(api).router)  # события, курсы итд
app.include_router(market.Init(api).router) # интерпретация маркета

if __name__ == '__main__':
    uvicorn.run(app,  host='0.0.0.0', 
                      port=int(os.getenv("API_PORT") or 3000))


