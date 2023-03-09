#!/usr/bin/env python3
"""This stores the sessions
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ The class definition
    """
    def __init__(self):
        """Class initialization
        """
        super().__init__()

    def create_session(self, user_id=None):
        """This creates and stores a new instance
        of user session and returns the session id
        """
        session_id = super().create_session(user_id)
        session_dict = { "user_id": user_id, "session_id": session_id }
        model = UserSession(**session_dict)
        model.save()
        return session_id

    def user_id_for_Session_id(self, session_id=None):
        """This returns the user_id from session_id
        """
        session = UserSession.search({ "session_id": session_id })
        if len(session) == 0:
            return None
        valid_period = session[0]['created_at'] + timedelta(
                seconds = self.session_duration)
        if valid_period < datetime.now():
            return None
        return session[0]['user_id']

    def destroy_session(self, request=None):
        """This destroys a session
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) == 0:
            return False
        sessions[0].remove()
        return True
