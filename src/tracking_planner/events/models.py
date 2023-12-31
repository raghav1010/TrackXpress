from sqlalchemy import Column, String, JSON, Integer

from library.sql.models import TimestampMixin, BaseSQLMixin
from library.sql.utils import BASE


class Event(BASE, TimestampMixin):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String)
    property_details = Column(JSON)

    def __repr__(self):
        return "{}".format(self.name)

    @classmethod
    def create(cls, **kwargs):
        event_record = cls()
        for key, value in kwargs.items():
            setattr(event_record, key, value)
        return event_record

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if value is None:
                continue
            setattr(self, key, value)
        return self

    @classmethod
    def get_by_id(cls, event_id, session):
        event_record = session.query(cls).filter(cls.id == event_id).first()
        return event_record

    @classmethod
    def get_by_name(cls, event_name, session):
        event_record = session.query(cls).filter(cls.name == event_name).first()
        return event_record

    @classmethod
    def get_all(cls, session):
        event_records = session.query(cls).all()
        return event_records
