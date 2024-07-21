#!/usr/bin/env python3
"""
Stores user sessions
"""
from models.base import Base
from sqlalchemy import Column, String


class UserSession(Base):
    """ UserSession class to store user sessions """
    __tablename__ = 'user_sessions'

    user_id = Column(String(60), nullable=False)
    session_id = Column(String(60), primary_key=True, nullable=False)

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize UserSession instance"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
