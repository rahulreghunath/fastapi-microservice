"""_summary_

Raises:
    credentials_exception: _description_
    HTTPException: _description_
    credentials_exception: _description_

Returns:
    _type_: _description_
"""
import requests
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from fastapi.security import SecurityScopes
from jose import JWTError, jwt, jwk, jws
from sqlalchemy.orm import Session

from payment import models
from payment.schemas import TokenData

# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
SECRET_KEY = "my-secret-key"
ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 150


PBK="-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA5flmwW+ZY0rLz3Y9pRfC\nsJ43ucdJiBQe7kkUGfGOdzD/WtAarMnSuqpC0n3RKxIk7TxwIS1xdDlL2rneNrlo\n12Uljmyr5TDCXtE0FjYIzfb/Z7c/spAEsC25A7S2QhcsRcjW5GzPBVeOU0F7saJ9\n5LZhYn6tK/ux+l6VNylbldTzl52HDQ43U/P+oT9wkXvCr0LW71p++OcmrcqAFB0l\nzCqVd3DUHCxZ76Yi5n9/2G4L+RGBvQZbIsvc3zvNnTsK+0W5qnGdW1RKZ+ou7g3u\n2/r27csSyEHU0e/+nmrXXq/CgO8BC5QJBmkpRyZRB62Jh9jpbK0pHjXmDuiWDt8Q\nU/x6dna5PrrY36VVAuSNEPFJaBFpFj4v6oQi6juHaFm+HG0tq9LBumg0vL0ZgLY0\nDYDtjwkNd1NMbJFpEm7Ad6qVEMMzymJMYkaQF5y76wMNTk2EMYrrISVT5ZXAZ0qj\nDQZOTfc50TSoFqbyEvyrx7CUPMyE05atpXOPaWhAeXhQKN5eRjTWJLHXNEN5DyG5\n1TQJwwx2EAg8MeuZ/fPkjfdJgEzV1qoLyJBRwrWJswc1BeodoSGnMbkrRICZVZW2\nEaJwLJ7m2PpG6HI232N5biuOs4Mmd17ZmlqoouIRyajHWxV7DXtfPF29+HK4/qhE\ne+sX/I1k3HJKni8CkXvFXC0CAwEAAQ==\n-----END PUBLIC KEY-----"


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
        payload = jwt.decode(token, PBK, algorithms=[ALGORITHM], audience="cloudium-test")
        
        uid: str = payload.get("uid")
        
        if uid is None:
            raise credentials_exception
        return TokenData(id=uid,token=token)
    except JWTError as e:
        raise credentials_exception from e
