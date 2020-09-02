#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs or 'updated_at' not in kwargs\
           and 'created_at' not in kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        if kwargs:
            for keys in kwargs.keys():
                if keys == 'created_at' or keys == 'updated_at':
                    dt = kwargs[keys]
                    form = '%Y-%m-%dT%H:%M:%S.%f'
                    if type(kwargs[keys]) is str:
                        kwargs[keys] = datetime.strptime(kwargs[keys], form)
                if not hasattr(self, keys):
                    raise KeyError
            if '__class__' in kwargs.keys():
                del kwargs['__class__']
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        dct = self.to_dict()
        if '__class__' in dct:
            del dct['__class__']
        return '[{}] ({}) {}'.format(cls, self.id, dct)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models.__init__ import storage
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
        if '_sa_instance_state' in dictionary.keys():
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        '''delete the current instance from the storage'''
        import models
        models.storage.delete(self)
