import json
from fastapi import status,HTTPException
from payment.redis_app import redis
def check_permission(user,permission):
    key = f'{user.id}-{user.token}'
    data = json.loads(redis.hget('USER_SESSION',key))
    authenticate_value = "Bearer"
    if permission not in data['permissions']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unautherised',
            headers={"WWW-Authenticate": authenticate_value},
        )
    