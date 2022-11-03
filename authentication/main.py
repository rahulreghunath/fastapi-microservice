import time,json
import requests
from typing import List
from fastapi.background import BackgroundTasks
from typing import Union
from redis_om import get_redis_connection
from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from authentication import schemas, models, validations
from authentication.database.database import get_db
from authentication.utils import Hash
from authentication.jwk_token import create_access_token
from authentication.redis_app import redis

app = FastAPI()

# cross origin resource sharing
origins = [
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    "/users",
    tags=["users"],
    status_code=status.HTTP_201_CREATED
)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    """_summary_

    Args:
        request (schemas.User): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """
    validations.user.check_if_exist(request, db)
    new_user = models.User(
        name=request.name, email=request.email, password=Hash.bcrypt(
            request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"details": 'User added'}


@app.post(
    "/login",
    response_model=schemas.Token,
)
def login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """_summary_

    Args:
        request (OAuth2PasswordRequestForm, optional): _description_.
            Defaults to Depends().
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """

    user = db.query(models.User).filter(
        models.User.email == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )
    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password"
        )

    access_token = create_access_token(data={"user": user.id})
    key = f'{user.id}-{access_token}'
    
    user_data = json.dumps({'user':user.id,'email':user.email,'permissions':['can-add-order','can-see-products']})
    redis.hset('USER_SESSION', key,user_data)
 
    # redis.set(key, user_data)   

    return {"access_token": access_token, "token_type": "bearer"}
