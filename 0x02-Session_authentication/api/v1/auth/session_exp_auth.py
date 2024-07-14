#!/usr/bin/env python3
"""
0x02-Session_authentication
"""
from api.v1.auth.session_auth import SessionAuth
import uuid
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """A class where to practice session based authentication."""

    def __init__(self):
        """The init method of the class."""
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """A method that creates a session."""
        try:
            new_session = super().create_session(user_id)
        except Exception:
            return None
        if not new_session:
            return None
        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[new_session] = session_dictionary
        return new_session

    def user_id_for_session_id(self, session_id=None):
        """A method that returns a user id based on a session id."""
        if session_id and session_id in self.user_id_by_session_id:
            user = self.user_id_by_session_id.get(session_id)
            if self.session_duration <= 0:
                return user.get("user_id")
            if "created_at" in user:
                time = user.get("created_at") + timedelta(
                    seconds=self.session_duration)
                if time < datetime.now():
                    return None
                return user.get("user_id")
            return None
        return None
