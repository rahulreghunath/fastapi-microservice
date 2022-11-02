"""_summary_"""
# pylint: disable=unexpected-keyword-arg, no-value-for-parameter

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database.database import Base


class Product(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)

