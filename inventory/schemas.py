
from typing import List, Union

from pydantic import BaseModel, Field, constr

    
class ProductBaseSchema(BaseModel):
    name: str
    price: int
    quantity: int

class ProductSchema(ProductBaseSchema):
    id: int
    name: str
    price: int
    quantity: int
    
    class Config:
        """_summary_"""

        orm_mode = True
        
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