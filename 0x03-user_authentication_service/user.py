#!/usr/bin/env python3
from sqlalchemy import Column, Integer, String

"""
Module Documentation
"""

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    hashed_passsword = Column(String)
    session_id = Column(String)
    reset_token = Column(String)
