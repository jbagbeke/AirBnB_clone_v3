#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os


class User(BaseModel, Base):
    """This class defines a user by various attributes"""

    __tablename__ = 'users'

    if os.environ.get("HBNB_TYPE_STORAGE") == "db":
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True, default='NULL')
        last_name = Column(String(128), nullable=True, default='NULL')
        places = relationship('Place', back_populates='user', cascade='all, delete')
        reviews = relationship('Review', back_populates='user', cascade='all, delete')
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
