#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime

Base = declarative_base()

class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not all(key in kwargs for key in ['updated_at', 'created_at', '__class__']):
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

            for key, value in kwargs.items():
               setattr(self, key, value)
        else:
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            del kwargs['__class__']
            
            for key, value in kwargs.items():
                setattr(self, key, value)

            self.__dict__.update(kwargs)

    def __str__(self):
        """ Returns string representation of desired output """

        class_name = self.__class__.__name__
        return ("[{}] ({}) {}".format(class_name, self.id, self.to_dict()))

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        if "_sa_instance_state" in dictionary.keys():
            del dictionary["_sa_instance_state"]

        return dictionary

    def delete(self):
        """ Deletes current instance from the storage objects """

        storage.delete(self)
