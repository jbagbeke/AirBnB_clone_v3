#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
import os


class State(BaseModel, Base):
    """ State class """

    __tablename__ = "states"

    if os.environ.get("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City",
                              back_populates="state",
                              cascade="all, delete")
    else:
        name = ""

    if os.environ.get('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """
                Returns list of City instances where state_id == State.id
                                                                          """
            from models import storage
            from models.city import City

            city_list = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
