#!/usr/bin/env python3
"""The hashes a password
"""
import bcrypt
import uuid
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password):
    """ The returned byte is a salted hash of the input password
    """
    password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email, password):
        """This adds a user to the database"""
        user_dict = {"email": email}
        try:
            user = self._db.find_user_by(**user_dict)
            raise ValueError("User " + email + " already exists")
        except NoResultFound:
            passwd = _hash_password(password)
            user = self._db.add_user(email, passwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """This validates login inputs and return boolean
        """
        try:
            user_dict = {"email": email}
        except NoResultFound:
            return False
        user = self._db.find_user_by(**user_dict)
        password = password.encode()
        if bcrypt.checkpw(password, user.hashed_password):
            return True
        return False

    def _generate_uuid(self) -> str:
        """This generates a uuid"""
        return str(uuid.uuid4())

    def create_session(self, email):
        """This returns the user session id
        """
        user_dict = {"email": email}
        try:
            user = self._db.find_user_by(**user_dict)
            newId = self._generate_uuid()
            user_dict = {"session_id": newId}
            self._db.update_user(user.id, **user_dict)
            return newId
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str):
        """This retrieves a user based on session_id
        """
        if session_id is None:
            return None
        user_dict = {"session_id": session_id}
        try:
            user = self._db.find_user_by(**user_dict)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id) -> None:
        """This updates the user's sessin_id to None
        """
        user_dict = {"id": user_id}
        try:
            user = self._db.find_user_by(**user_dict)
            new_dict = {'session_id': None}
            self._db.update_user(user.id, **new_dict)
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email):
        """This generates a reset_token for a user
        """
        try:
            user = self._db.find_user_by(email=email)
            token = self._generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token, password) -> None:
        """This resets a user password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed)
            return None
        except NoResultFound:
            raise ValueError
