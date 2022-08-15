import logging
from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from analyzef1.persistance.base import _DECL_BASE
from analyzef1.persistance.season_model import Season, SessionResult


logger = logging.getLogger(__name__)

DB_PATH = f"{Path().resolve()}/database"
DB_URL = f"sqlite:////{DB_PATH}/Season_{datetime.now().year}.sqlite"

def init_db() -> None:
    """
    Initialize the database with tables Season and SessionResult.
    """
    engine = create_engine(DB_URL, future=True)

    Season._db_session = scoped_session(sessionmaker(bind=engine, autoflush=True))
    Season.query = Season._db_session.query_property()
    SessionResult.query = Season._db_session.query_property()

    _DECL_BASE.metadata.create_all(engine)
    logger.info(f'Using database Season_{datetime.now().year}.sqlite')