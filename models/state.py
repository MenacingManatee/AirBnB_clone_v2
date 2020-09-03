#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all,delete,delete-orphan",
                          backref="state")

    @property
    def cities(self):
        '''
        Returns a list of city objects with a state_id matching state.id
        '''
        #if getenv('HBNB_TYPE_STORAGE') != 'db':
        from models import storage
        from models.city import City

        objs = storage.all(City).items()
        return sorted([obj for key, obj in objs if obj.state_id == self.id],
                      key=lambda x: x.name)
