#!/usr/bin/env python3

from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """This adds an expiration data to a session id"""

    def __init__(self):
        """This initialises the class"""
        try:
            duration = int(getenv('SESSION_DURATION'))
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        """This creates a session id"""
        try:
            session_id = super().create_session(user_id)
        except Exception:
            return None

        self.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now()
                }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """This retrieves a user id from a session_id
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration == 0:
            return self.user_id_by_session_id[session_id]["user_id"]
        if "created_at" not in self.user_id_by_session_id[session_id]:
            return None
        created_at = self.user_id_by_session_id[session_id]['created_at']
        valid_period = created_at + timedelta(seconds = self.session_duration)
        if valid_period < datetime.now():
            return None
        return self.user_id_by_session_id[session_id]["user_id"]
