#!/usr/bin/python3
'''Defines a new engine using a sql db'''


class DBStorage:
    '''Contains the methods used in this engine'''
    __engine = None
    __session = None

    def __init__(self):
        '''Initializes the engine'''
        from sqlalchemy import create_engine
        from os import getenv
        user = getenv('HBNB_MYSQL_USER')
        pw = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://' + user + ':' + pw +
                                      '@' + host + ':3306/' + db,
                                      pool_pre_ping=True)
        conc = self.__engine.connect()
        if getenv('HBNB_ENV') == 'test':
            from models.base_model import Base
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        '''query on the current database session all objects depending
        on the class name'''
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        from models.place import Place
        from models.user import User
        import console
        if cls is None:
            res = []
            for clas in console.HBNBCommand.classes:
                if clas != BaseModel:
                    res.extend(self.__session.query(eval(clas)).all())
            res_dct = {}
            for obj in res:
                res_dct.update({"{}.{}".format(obj.__class__.name, obj.id):
                                obj})
            return res_dct
        else:
            d_list = (self.__session.query(cls).all())
            return ({obj.to_dict()['__class__'] + '.' + obj.id: obj for
                     obj in d_list})

    def new(self, obj):
        '''Adds an object to the database'''
        self.__session.add(obj)
        self.save()
        self.reload()

    def save(self):
        '''commit all changes of the current database session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''delete from the current database session obj if not None'''
        if obj is None:
            return
        self.__session.delete(obj)
        self.save()

    def reload(self):
        '''create all tables in the database'''
        from sqlalchemy.orm import scoped_session
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import MetaData
        from models.base_model import BaseModel, Base
        from models.amenity import Amenity
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.state import State
        from models.user import User
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        self.__session.close()
