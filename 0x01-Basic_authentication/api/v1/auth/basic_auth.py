#!/usr/bin/env python3
""" This defines the basic auth """

from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ This defines the class
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """This returns the encoded part of
        the authorization header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """This returns the decoded value of a Base64 string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            data = base64.b64decode(base64_authorization_header)
            return data.decode('utf-8')
        except Exception as e:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ This returns the user email and password from the base64
        decoded value
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        credential = decoded_base64_authorization_header.split(':')
        return (credential[0], credential[1])

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ This returns the user instance based on his email
        and password
        """
        if user_email is None or not isinstance(user_email, str):
            print("Mail not str")
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            print("pwd not str")
            return None
        if not user_pwd:
            print("no pwd")
            return None
        credential = {"email": user_email}
        try:
            all_users = User.search(credential)
            for user in all_users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """This retrieves the user instance for a request"""
        header = super().authorization_header(request)
        auth = self.extract_base64_authorization_header(header)
        credential_header = self.decode_base64_authorization_header(auth)
        credential = self.extract_user_credentials(credential_header)
        user = self.user_object_from_credentials(credential[0], credential[1])
        return user
