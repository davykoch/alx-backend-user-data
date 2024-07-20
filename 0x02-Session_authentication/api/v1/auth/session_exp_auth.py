#!/usr/bin/env python3
"""SessionExpAuth module for the API"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class to manage session expiration"""

    def __init__(self):
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0
        print(f"[DEBUG] session_duration: {self.session_duration}")

    def create_session(self, user_id=None):
        """Creates a Session ID for a user_id with expiration"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        print(f"[DEBUG] Created session: {session_id} -> {session_dict}")
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns a User ID based on a Session ID with expiration"""
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            print(f"[DEBUG] No session found for session_id: {session_id}")
            return None

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        created_at = session_dict.get("created_at")
        if created_at is None:
            print(f"[DEBUG] No created_at found for session_id: {session_id}")
            return None

        if created_at + \
                timedelta(seconds=self.session_duration) < datetime.now():
            print(f"[DEBUG] Session expired for session_id: {session_id}")
            return None

        print(f"[DEBUG] Session valid for session_id: {session_id}")
        return session_dict.get("user_id")
