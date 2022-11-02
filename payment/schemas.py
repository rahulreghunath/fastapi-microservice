
from typing import List, Union

from pydantic import BaseModel, Field, constr

    
class OrderBaseSchema(BaseModel):
    product_id: int
    quantity: int
   

class OrderSchema(OrderBaseSchema):
    id: int
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str
    price: float
    fee: float
    total: float
    status: str
    
    class Config:
        """_summary_"""

        orm_mode = True