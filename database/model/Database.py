from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import create_database, database_exists


class Database:
    """Class for general postgre database generation."""

    DH_PATH_MODEL = "postgresql+psycopg2://{user}:{password}@{host}/{database}"
    BASE = declarative_base()

    def __init__(self, settings: dict[str:str]):
        self._engine = None
        self._settings = settings

    def _create_engine(self) -> None:
        db_url = self.DH_PATH_MODEL.format(**self._settings)
        self._engine = create_engine(db_url, echo=False)

    def _create_database(self) -> None:
        """Database creation method"""
        db_url = self._engine.url

        if not database_exists(db_url):
            create_database(db_url)

        self.BASE.metadata.create_all(self._engine)

    def setup_database_environment(self) -> None:
        """Method to set up the database environment"""
        self._create_engine()
        self._create_database()
