#!/usr/bin/env python3
"""
Stores user sessions
"""
from sqlalchemy import Column, String, DateTime
from models.sql_base import Base
from datetime import datetime


class UserSession(Base):
    """UserSession model to store session information in the database"""
    __tablename__ = 'user_sessions'
    user_id = Column(String(60), nullable=False)
    session_id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
