
from typing import List, Union

from pydantic import BaseModel, Field, constr


class OrderBaseSchema(BaseModel):
    product_id: int
    quantity: int


class OrderSchema(OrderBaseSchema):
    id: int
    product_id: str
    price: Union[float, None] = None
    fee: Union[float, None] = None
    total: Union[float, None] = None
    quantity: Union[int, None] = None
    status: Union[str, None] = None
    price: Union[float, None] = None
    fee: Union[float, None] = None
    total: Union[float, None] = None
    status: Union[str, None] = None

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

    id: str
    token: str