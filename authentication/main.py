import time
import json
import requests
from typing import List
import firebase_admin
from firebase_admin import auth
from fastapi.background import BackgroundTasks
from typing import Union
from redis_om import get_redis_connection
from fastapi import FastAPI, Depends, status, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from firebase_admin import tenant_mgt

from authentication import schemas, models, validations
from authentication.database.database import get_db
from authentication.utils import Hash
from authentication.jwk_token import create_access_token
from authentication.redis_app import redis
from shared.messages import LOGIN_ERROR

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

firebase_admin.initialize_app()


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

    # user = db.query(models.User).filter(
    #     models.User.email == request.username).first()
    
    data = {
        'email':request.username,
        'password':request.password,
        'returnSecureToken':True,
        'tenantId':'FirstTenant-uuhji'
    }
    response = requests.post(
        'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyBfsfVepPDBiCAD5LpLdjsZk-rvVhED6wM',
        data=data,
        timeout=10
    )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )
    
    decoded_token = auth.verify_id_token(response.json()['idToken'])
    decoded_token['key']='user-key'
    access_token = create_access_token(
        data=decoded_token
    )
    key = f'{decoded_token.get("uid")}-{access_token}'

    user_data = json.dumps(
        {'user': decoded_token.get("uid"), 'email': decoded_token.get("email"), 'permissions': ['can-see-products']}
    )
    redis.hset('USER_SESSION', key, user_data)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get(
    "/login1",
)
def login1():
    return {'data':LOGIN_ERROR}
    
    # uid = decoded_token['uid']
    return {'uid': uid}
