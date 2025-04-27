# File: /resume-analyzer/resume-analyzer/src/models/__init__.py

from .database import db
from .user import User
from .resume import Resume

__all__ = ['db', 'User', 'Resume']