import unittest
from library.sql import BASE
from library.sql import utils as sql_utils
from library.ut_db.models import UtDb
from src.tracking_planner.events.model_utils import create_event_record


class TestUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ut_db = UtDb(BASE)
        ut_db.create_all_tables()

        sql_utils.SESSION = ut_db.sessionmaker
        sql_utils.ENGINE = ut_db.engine

    def test_event_creation(self):

        self.setUpClass()

        event_record, error = create_event_record({
            "name": "Order Viewed",
            "description": "Whose order viewed",
            "property_details": {
                "product": "ap1",
                "price": "10",
                "currency": "INR"
            }
        })
        self.assertEqual(event_record.name, "Order Viewed")
