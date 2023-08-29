import logging
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql.sqltypes import String, Integer


class TimestampMixin:
    dt_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    dt_updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow, default=datetime.utcnow)


class BaseSQLMixin:
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__

    @classmethod
    def get_one(cls, session, **kwargs):
        try:
            return session.query(cls).filter_by(**kwargs).first()
        except Exception as error:
            logging.exception("invalid query: {}".format(error))
            return None
