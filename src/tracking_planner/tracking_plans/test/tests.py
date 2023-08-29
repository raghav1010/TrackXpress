import unittest
from library.sql import BASE
from library.sql import utils as sql_utils
from library.ut_db.models import UtDb
from src.tracking_planner.tracking_plans.model_utils import create_tracking_plan_record


class TestUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ut_db = UtDb(BASE)
        ut_db.create_all_tables()

        sql_utils.SESSION = ut_db.sessionmaker
        sql_utils.ENGINE = ut_db.engine

    def test_tracking_plan_creation(self):
        self.setUpClass()

        tracking_record, error = create_tracking_plan_record({
            "name": "Tracking Plan 1",
            "description": "tracking plan desc"})
        self.assertEqual(tracking_record.name, "Tracking Plan 1")
