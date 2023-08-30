import unittest
from library.sql import BASE
from library.sql import utils as sql_utils
from library.sql.utils import session_wrap
from library.ut_db.models import UtDb
from src.tracking_planner.events.model_utils import create_event_record


class TestUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ut_db = UtDb(BASE)
        ut_db.create_all_tables()

        sql_utils.SESSION = ut_db.sessionmaker
        sql_utils.ENGINE = ut_db.engine

    @session_wrap
    def test_event_creation(self, session=None):

        self.setUpClass()

        event_record, error = create_event_record({
            "name": "Order Viewed Test",
            "description": "Whose order viewed",
            "property_details": {
                "product": "ap1",
                "price": "10",
                "currency": "INR"
            }
        }, session=session)
        self.assertEqual(event_record.name, "Order Viewed Test")
