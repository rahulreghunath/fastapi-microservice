"""_summary_

Raises:
    credentials_exception: _description_
    HTTPException: _description_
    credentials_exception: _description_

Returns:
    _type_: _description_
"""
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from fastapi.security import SecurityScopes
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from payment import models
from payment.schemas import TokenData

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 150


def verify_token(
    token: str, credentials_exception, db: Session
):
    """_summary_

    Args:
        token (str): _description_
        security_scopes (SecurityScopes): _description_
        credentials_exception (_type_): _description_
        db (Session): _description_

    Raises:
        credentials_exception: _description_
        HTTPException: _description_
        credentials_exception: _description_

    Returns:
        _type_: _description_
    """
    
    authenticate_value = "Bearer"
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user")
        
        if user_id is None:
            raise credentials_exception
        
        return TokenData(id=user_id,token=token)
    except JWTError as e:
        raise credentials_exception from e
