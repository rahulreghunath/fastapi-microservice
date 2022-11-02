
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