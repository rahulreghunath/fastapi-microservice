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
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 150


def create_access_token(data: dict):
    """_summary_

    Args:
        data (dict): _description_

    Returns:
        _type_: _description_
    """
    ppk = "-----BEGIN RSA PRIVATE KEY-----\n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\n-----END RSA PRIVATE KEY-----\n"
    pbk="-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA2vCYgxT3sPNqkL0OfViU\n9IPzmyR/uZIsrsac7vm/bZpl616r98rx84vaGssd9md1sz9c1fm2hh6Op6QNL5QH\nu10lxve+wxfVWbKqiJWmMhKyem9SYXnYRhGqL9zGjQFMf8Zh7t0bbOB2Y9tjxOIE\nFA6+YJ/MOricTm347JDtIz8Zo+si449Tz8W58+Hw8fYDEyXgjTsRZDPCReUqmw2V\nTRgEXdwPxxo5RLaRe5Y3GzSxNkoYHNRrw1u8JqgGYehoruT0oh2k3Jb+kYP2gNQe\n+cDdBAmpdiQfuifSTXz9VZJ+j+HIuoTph1vIoLxTHdGeGQi6AK5qA7WfBCTkFr2U\neYsRsE/e7UXYSJBATmYLMIdnUOHMMPxnokZRHXJk/WTHQXHyez9KtwopwNNaQymZ\nRFsmWv8s010R461c0N21nkLCTdpTMoHQ/JrxuTnCai/0TItmc0EGiqs4pJKokVQC\nj/EL+VSTXk7kbUMIyismvnJ/wnERmOZAwYeXCk1y5CH4Gz+oafBSUfzXIAuDnzVT\njRhwZtIaijHGYgUjlPbIj7gEgt38pctveSxjOjwsapKARfbxMmtGdthyXnPT/Pqn\nKvDHix8Jt7N80rpbNis789krXVta0uvbnLiRnuCR2d1ike6/5E/Qh5LcSXLqJEsF\n9oJZ5iHz2/906IP1OCnUqU8CAwEAAQ==\n-----END PUBLIC KEY-----\n"
    key_string = requests.get('https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com')
    public_keys = key_string.json()
    
    # rsa_public_key = public_keys.get(list(public_keys.keys())[1])
    # print(rsa_public_key)
    # token = jwt.encode({"hello": "world","key": "user-key"}, ppk, algorithm="RS256")
    # print(token)
    # token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ3YjE5MTI0MGZjZmYzMDdkYzQ3NTg1OWEyYmUzNzgzZGMxYWY4OWYiLCJ0eXAiOiJKV1QifQ.eyJrZXkiOiJ1c2VyLWtleSIsImxldmVsIjoyLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vY2xvdWRpdW0tdGVzdCIsImF1ZCI6ImNsb3VkaXVtLXRlc3QiLCJhdXRoX3RpbWUiOjE2Njc5OTAyMDUsInVzZXJfaWQiOiJmNUlxNFp1dnJsZ3FtVExUTzB3ZktvTVF2MzAzIiwic3ViIjoiZjVJcTRadXZybGdxbVRMVE8wd2ZLb01RdjMwMyIsImlhdCI6MTY2Nzk5MDIwNiwiZXhwIjoxNjY3OTkzODA2LCJlbWFpbCI6InByYXZlZW5zYW5qYXkxOTk4QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJwcmF2ZWVuc2FuamF5MTk5OEBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCIsInRlbmFudCI6IkZpcnN0VGVuYW50LXV1aGppIn19.iRje0ediPwkSJbffFG-EQu8GEq9IvgocIFReWeYm62S04PBQ1ba9zxbrA71WEZ61DJk8TBN7V-cqLIO6KJke8I6qBGbTwlIoLXT89v2bfCHl-VTy_nAHS6PyGoA3mIneQ7h_v-yHu95_CzHb0xuPMzhwzPNd155bhDZn6B2LyZtl0o9xH-UoXQX804sTCFc0hD8XoOkWcoYcmqsMRUHERx7dYYTTVpDfxAJHTRuOzgtRhn0sLHN8UNwALYkU2f_v74s_h5LP6rgXRCRMKmUXpY_sO4ak9Upa8iP1AYjw4UgjerMWHjz8KyEeQL3y0rLtikgUDotUWrM3i9j1HxUwHQ"
    
    # print(jwt.decode(token, public_keys, "RS256",audience='cloudium-test'))
    
    # return token
    
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user")
        
        if user_id is None:
            raise credentials_exception
        return TokenData(id=id,token=token)
    except JWTError as e:
        raise credentials_exception from e
