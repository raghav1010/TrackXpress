import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from library.ut_db.constants import DEFAULT_POSTGRES_UT_DB, DEFAULT_POSTGRES_UT_USER, DEFAULT_POSTGRES_UT_PASSWORD
from src.common.env import POSTGRES_URL


class UtDb:
    def __init__(self, base):
        super().__init__()
        self.base = base

        self.db_name = os.environ.get("POSTGRES_UT_DB", DEFAULT_POSTGRES_UT_DB)
        self.db_user = os.environ.get("POSTGRES_UT_USER", DEFAULT_POSTGRES_UT_USER)
        self.db_password = os.environ.get("POSTGRES_UT_PASSWORD", DEFAULT_POSTGRES_UT_PASSWORD)
        self.db_instance_uri = (
            f'postgresql://{self.db_user}:{self.db_password}@{POSTGRES_URL}:5432/{self.db_name}'
        )
        self.sql_engine = create_engine(
            self.db_instance_uri, connect_args={'connect_timeout': 10}
        )
        self.sessionmaker = sessionmaker(bind=self.sql_engine)

    def validate_connection(self):
        if self.sql_engine.url.database != self.sql_dbname:
            raise ValueError(f'Incorrect db: {self.sql_dbname}')

    def create_all_tables(self):
        self.validate_connection()
        self.sql_base.metadata.create_all(self.sql_engine)

    def drop_all_tables(self):
        self.validate_connection()
        session = self.sessionmaker()
        self.sql_base.metadata.drop_all(self.sql_engine)
        session.close()
        session.rollback()
