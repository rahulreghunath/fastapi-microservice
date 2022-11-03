
from typing import List, Union

from pydantic import BaseModel, Field, constr

class BaseUser(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """

    name: str
    email: str

class ResponseUser(BaseUser):
    """_summary_

    Args:
        BaseUser (_type_): _description_
    """

    class Config:
        """_summary_"""

        orm_mode = True


class User(BaseUser):
    """_summary_

    Args:
        BaseUser (_type_): _description_
    """

    password: str

        
class Login(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """

    username: str
    password: str


class Token(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """

    id: int
    token: str