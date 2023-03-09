#!/usr/bin/env python3
"""This manages the API authentication
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth():
    """class definition
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ This returns false """
        if path and path[-1] != '/':
            path += '/'

        if path is None or excluded_paths is None:
            return True
        if excluded_paths == []:
            return True
        if path and path not in excluded_paths:
            return True
        if path and path in excluded_paths:
            return False
        return False

    def authorization_header(self, request=None) -> str:
        """ This returns None """
        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """This returns None"""
        return None

    def session_cookie(self, request=None):
        """This returns a session_id from a request
        """
        if request is None:
            return None
        _my_session_id = getenv('SESSION_NAME')
        return request.cookies.get(_my_session_id)
