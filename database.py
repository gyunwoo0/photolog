u"""데이터베이스모듈."""
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBManager:
    u"""DBManager class."""

    __engine = None
    __session = None

    @staticmethod
    def init(db_url, db_log_flag=True):
        u"""shashasha."""
        DBManager.__engine = create_engine(db_url, echo=db_log_flag)
        DBManager.__session = \
            scoped_session(sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=DBManager.__engine))

        global dao
        dao = DBManager.__session

    @staticmethod
    def init_db():
        u"""shashasha."""
        from photolog.model import *
        from photolog.model import Base
        Base.metadata.create_all(bind=DBManager.__engine)

dao = None
