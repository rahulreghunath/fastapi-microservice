"""_summary_"""
# pylint: disable=unexpected-keyword-arg, no-value-for-parameter

from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from authentication.database.database import Base

class User(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    phone = Column(String)

