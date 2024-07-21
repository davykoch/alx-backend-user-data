#!/usr/bin/env python3
"""SessionDBAuth module for handling session authentication
with database storage"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
from flask import abort


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""

    def create_session(self, user_id=None):
        """Create and store new instance of UserSession"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        kwargs = {'user_id': user_id, 'session_id': session_id}
        user_session = UserSession(**kwargs)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the User ID by requesting UserSession in the database"""
        if session_id is None:
            return None
        UserSession.load_from_file()
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return None
        user_session = user_sessions[0]

        # Check if the session has expired
        created_at = user_session.created_at
        if created_at is None:
            return None

        if self.session_duration <= 0:
            return user_session.user_id

        expired_time = created_at + timedelta(seconds=self.session_duration)
        if expired_time < datetime.utcnow():
            abort(403)

        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroys the UserSession based on the Session ID
        from the request cookie"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        user_sessions = UserSession.search({'session_id': session_id})
        if user_sessions:
            user_sessions[0].remove()
            UserSession.save_to_file()
            return True
        return False
