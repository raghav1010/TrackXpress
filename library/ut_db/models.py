import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.common.constants import DEFAULT_POSTGRES_URL, DEFAULT_POSTGRES_DBUSER, \
    DEFAULT_POSTGRES_DBPASS, DEFAULT_POSTGRES_PORT, DEFAULT_POSTGRES_DBNAME


class UtDb:
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.db_instance_uri = os.environ.get("POSTGRES_URL", DEFAULT_POSTGRES_URL)
        self.db_name = os.environ.get("POSTGRES_DB", DEFAULT_POSTGRES_DBNAME)
        self.db_user = os.environ.get("POSTGRES_USER", DEFAULT_POSTGRES_DBUSER)
        self.db_password = os.environ.get("POSTGRES_PASSWORD", DEFAULT_POSTGRES_DBPASS)

        self.db_port = os.environ.get("POSTGRES_PORT", DEFAULT_POSTGRES_PORT)

        self.db_instance_uri = (f"postgresql://{self.db_user}:{self.db_password}@{self.db_instance_uri}:" \
                                    f"{self.db_port}/{self.db_name}")

        self.engine = create_engine(
            self.db_instance_uri, connect_args={'connect_timeout': 10}
        )
        self.sessionmaker = sessionmaker(bind=self.engine)

    def validate_connection(self):
        if self.engine.url.database != self.db_name:
            raise ValueError(f'Incorrect db: {self.db_name}')

    def create_all_tables(self):
        self.validate_connection()
        self.base.metadata.create_all(self.engine)

    def drop_all_tables(self):
        self.validate_connection()
        session = self.sessionmaker()
        self.base.metadata.drop_all(self.engine)
        session.close()
        session.rollback()
