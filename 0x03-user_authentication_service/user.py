#!/usr/bin/env python3
"""This defines the user class model
"""

from sqlalchemy import String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()


class User(Base):
    """User class
    """
    __tablename__ = 'users'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __init__(self, **kwargs):
        """This sets the attributes of the user object
        """
        for key, val in kwargs.items():
            setattr(self, key, val)
