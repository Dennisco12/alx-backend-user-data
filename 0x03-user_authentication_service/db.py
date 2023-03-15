#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email, hashed_password):
        """This saves users to the database
        """
        user_dict = {"email": email, "hashed_password": hashed_password}
        model = User(**user_dict)
        self._session.add(model)
        self._session.commit()
        return model

    def find_user_by(self, **kwargs):
        """This returns the first row found for the argument
        """
        objList = []
        if not kwargs:
            raise InvalidRequestError

        column_names = ['email', 'hashed_password', 'session_id',
                        'reset_token', 'id']
        for key, val in kwargs.items():
            if key not in column_names:
                raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound

        return user

    def update_user(self, user_id, **kwargs):
        """This update a user attribute
        """
        user_dict = {"id": user_id}
        user = self.find_user_by(**user_dict)
        for key, val in kwargs.items():
            try:
                setattr(user, key, val)
                self._session.commit()
            except Exception:
                raise ValueError
