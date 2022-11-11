import time
import json
import requests
from typing import List
import firebase_admin
from firebase_admin import auth
from fastapi.background import BackgroundTasks
from typing import Union
from redis_om import get_redis_connection
from fastapi import FastAPI, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from authentication import schemas, models, validations
from authentication.database.database import get_db
from authentication.utils import Hash
from authentication.jwk_token import create_access_token
from authentication.redis_app import redis
from firebase_admin import tenant_mgt
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

    access_token = create_access_token(
        data={"user": user.id, 'key': 'user-key'})
    key = f'{user.id}-{access_token}'

    user_data = json.dumps(
        {'user': user.id, 'email': user.email, 'permissions': ['can-see-products']})
    redis.hset('USER_SESSION', key, user_data)

    # redis.set(key, user_data)

    return {"access_token": access_token, "token_type": "bearer"}


@app.get(
    "/login1",
)
def login1():
    default_app = firebase_admin.initialize_app()
    # cred = credentials.Certificate('path/to/serviceAccountKey.json')
    # token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImRjMzdkNTkzNjVjNjIyOGI4Y2NkYWNhNTM2MGFjMjRkMDQxNWMxZWEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vY2xvdWRpdW0tdGVzdCIsImF1ZCI6ImNsb3VkaXVtLXRlc3QiLCJhdXRoX3RpbWUiOjE2Njc5MTA3OTUsInVzZXJfaWQiOiJmNUlxNFp1dnJsZ3FtVExUTzB3ZktvTVF2MzAzIiwic3ViIjoiZjVJcTRadXZybGdxbVRMVE8wd2ZLb01RdjMwMyIsImlhdCI6MTY2NzkxMDc5NywiZXhwIjoxNjY3OTE0Mzk3LCJlbWFpbCI6InByYXZlZW5zYW5qYXkxOTk4QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJwcmF2ZWVuc2FuamF5MTk5OEBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCIsInRlbmFudCI6IkZpcnN0VGVuYW50LXV1aGppIn19.mUWmIxP8qAbSaW603mGa-kq6ufwHdwSHH8OhyeMQrMGPIjFgceREZks-ujXOA47OmjekTodO2zNHSKTEULDvyWvdIhlCnDpWHfmDL9JWEczOFC25Pya04yKyeWVv9VGrCw63x2VL47lTrqwPSyxBr9WbtwaZ5BbXq6Fz4r-5ykbjnsORDw9nsRQIhvnqJHFLFcqCXC1ycr6X1MAs_6bRBHjTYAyNqo7VWxBuFOUF6dpN0QaW7gzF9wJ2lGlTxphbdqgh0EFkAh1baCa53DZo4TMeJlfLfNR0DHNuuETbJwmB_wI2pzAS55CaM-KWqj1WDcql9bI49LKDd6bprejr4A'
    # decoded_token = auth.verify_id_token(token)
    uid = 'f5Iq4ZuvrlgqmTLTO0wfKoMQv303'
    # user = auth.get_user_by_email(uid)
    
    tenant_client = tenant_mgt.auth_for_tenant('FirstTenant-uuhji')
    user = tenant_client.get_user(uid)
    print(user.uid)
    data = tenant_client.set_custom_user_claims(uid, {"key": "user-key","level":2})
    print('claims')
    print(user.custom_claims)
    
    

    # uid = decoded_token['uid']
    return {'uid': uid}
