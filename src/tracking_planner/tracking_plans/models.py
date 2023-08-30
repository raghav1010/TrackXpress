from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import validates

from library.sql.models import TimestampMixin, BaseSQLMixin
from library.sql.utils import BASE, sql_check_choices
from src.tracking_planner.tracking_plans.constants import TRACKING_PLAN_SOURCE_CHOICES


class TrackingPlan(BASE, TimestampMixin):
    __tablename__ = "tracking_plan"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String)
    source = Column(String(50), default="http")

    def __repr__(self):
        return "{}".format(self.name)

    # @validates("source")
    # def validate_req_type(self, key, source):
    #     return sql_check_choices(self, key, source, TRACKING_PLAN_SOURCE_CHOICES)

    @classmethod
    def create(cls, **kwargs):
        tracking_plan_record = cls()
        for key, value in kwargs.items():
            setattr(tracking_plan_record, key, value)
        return tracking_plan_record

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if value is None:
                continue
            setattr(self, key, value)
        return self

    @classmethod
    def get_by_id(cls, tracking_plan_id, session):
        tracking_plan_record = session.query(cls).filter(cls.id == tracking_plan_id).first()
        return tracking_plan_record

    @classmethod
    def get_by_source(cls, source, session):
        tracking_plan_record = session.query(cls).filter(cls.source == source).first()
        return tracking_plan_record

    @classmethod
    def get_by_name(cls, name, session):
        tracking_plan_record = session.query(cls).filter(cls.name == name).first()
        return tracking_plan_record
