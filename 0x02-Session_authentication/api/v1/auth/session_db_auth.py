#!/usr/bin/env python3
"""
Stores sessions in a database
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from models.sql_base import Base
import uuid


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class that stores sessions in a database """

    def __init__(self):
        """Initialize SessionDBAuth instance"""
        super().__init__()
        self.engine = create_engine('sqlite:///user_sessions.db')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def create_session(self, user_id=None):
        """Create and store a new session in the database"""
        if not user_id:
            return None
        session_id = str(uuid.uuid4())
        created_at = datetime.utcnow()
        session = UserSession(
            user_id=user_id,
            session_id=session_id,
            created_at=created_at)

        db_session = self.Session()
        db_session.add(session)
        db_session.commit()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve the User ID from the database"""
        if not session_id:
            return None
        db_session = self.Session()
        try:
            session = db_session.query(UserSession).filter_by(
                session_id=session_id).one()
        except NoResultFound:
            return None
        if self.session_duration and (
                datetime.utcnow() -
                session.created_at) > timedelta(
                seconds=self.session_duration):
            db_session.delete(session)
            db_session.commit()
            return None
        return session.user_id

    def destroy_session(self, request=None):
        """Destroy the session based on the request cookie"""
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        db_session = self.Session()
        session = db_session.query(UserSession).filter_by(
            session_id=session_id).first()
        if not session:
            return False
        db_session.delete(session)
        db_session.commit()
        return True
