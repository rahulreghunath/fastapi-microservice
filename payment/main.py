import time
import requests
from typing import List
from fastapi.background import BackgroundTasks
from typing import Union
from redis_om import get_redis_connection
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from payment import schemas, models, permission,routes
from payment.oauth2 import get_current_user
from payment.database.database import get_db
from payment.redis_app import redis

app = FastAPI()



# cross origin resource sharing
origins = [
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)