from sqlalchemy import Column, String, ForeignKey, Integer

from library.sql.models import TimestampMixin, BaseSQLMixin
from library.sql.utils import BASE


class TrackingPlanTransaction(BASE, TimestampMixin):
    __tablename__ = "tracking_plan_transaction"
    id = Column(Integer, primary_key=True)
    ref_id = Column(String, nullable=False)
    tracking_plan_id = Column(Integer, ForeignKey("tracking_plan.id"))
    event_id = Column(Integer, ForeignKey("event.id"))

    def __repr__(self):
        return "{}".format(self.ref_id)

    @classmethod
    def create(cls, **kwargs):
        tracking_plan_transaction_record = cls()
        for key, value in kwargs.items():
            setattr(tracking_plan_transaction_record, key, value)
        return tracking_plan_transaction_record

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if value is None:
                continue
            setattr(self, key, value)
        return self

    @classmethod
    def get_by_ref_id(cls, ref_id, session):
        tracking_plan_transaction_record = session.query(cls).filter(cls.ref_id == ref_id).first()
        return tracking_plan_transaction_record

    @classmethod
    def get_all_events_per_tracking_plan(cls, tracking_plan_id, session):
        event_records = session.query(cls).filter(cls.tracking_plan_id == tracking_plan_id).order_by(
            cls.dt_created.desc()).all()
        return event_records

    @classmethod
    def get_all_tracking_plan_per_event(cls, event_id, session):
        tracking_plan_records = session.query(cls).filter(cls.event_id == event_id).order_by(
            cls.dt_created.desc()).all()
        return tracking_plan_records
