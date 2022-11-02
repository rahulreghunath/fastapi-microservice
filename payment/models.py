"""_summary_"""
# pylint: disable=unexpected-keyword-arg, no-value-for-parameter

from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database.database import Base


class Order(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String)
    price = Column(Float)
    fee = Column(Float)
    total = Column(Float)
    quantity = Column(Float)
    status = Column(String)

