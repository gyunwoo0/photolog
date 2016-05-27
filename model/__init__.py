u"""데이터베이스 모듈."""
# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

__all__ = ["user", "photo"]
