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

from authentication import models
from authentication.schemas import TokenData

# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
SECRET_KEY = "my-secret-key"
ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 150

PPK = """-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----"""

PBK="-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA5flmwW+ZY0rLz3Y9pRfC\nsJ43ucdJiBQe7kkUGfGOdzD/WtAarMnSuqpC0n3RKxIk7TxwIS1xdDlL2rneNrlo\n12Uljmyr5TDCXtE0FjYIzfb/Z7c/spAEsC25A7S2QhcsRcjW5GzPBVeOU0F7saJ9\n5LZhYn6tK/ux+l6VNylbldTzl52HDQ43U/P+oT9wkXvCr0LW71p++OcmrcqAFB0l\nzCqVd3DUHCxZ76Yi5n9/2G4L+RGBvQZbIsvc3zvNnTsK+0W5qnGdW1RKZ+ou7g3u\n2/r27csSyEHU0e/+nmrXXq/CgO8BC5QJBmkpRyZRB62Jh9jpbK0pHjXmDuiWDt8Q\nU/x6dna5PrrY36VVAuSNEPFJaBFpFj4v6oQi6juHaFm+HG0tq9LBumg0vL0ZgLY0\nDYDtjwkNd1NMbJFpEm7Ad6qVEMMzymJMYkaQF5y76wMNTk2EMYrrISVT5ZXAZ0qj\nDQZOTfc50TSoFqbyEvyrx7CUPMyE05atpXOPaWhAeXhQKN5eRjTWJLHXNEN5DyG5\n1TQJwwx2EAg8MeuZ/fPkjfdJgEzV1qoLyJBRwrWJswc1BeodoSGnMbkrRICZVZW2\nEaJwLJ7m2PpG6HI232N5biuOs4Mmd17ZmlqoouIRyajHWxV7DXtfPF29+HK4/qhE\ne+sX/I1k3HJKni8CkXvFXC0CAwEAAQ==\n-----END PUBLIC KEY-----"

def create_access_token(data: dict):
    """_summary_

    Args:
        data (dict): _description_

    Returns:
        _type_: _description_
    """
    
    

   
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, PPK, algorithm=ALGORITHM)

    return encoded_jwt


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
        payload = jwt.decode(token, PBK, algorithms=[ALGORITHM])
        user_id: str = payload.get("user")
        
        if user_id is None:
            raise credentials_exception
        return TokenData(id=id,token=token)
    except JWTError as e:
        raise credentials_exception from e
