import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import fastf1 as ff1
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    desc,
    func,
)
from sqlalchemy.orm import Query, lazyload, relationship

from analyzef1.constants import DRIVER_TEAM_MAPPING
from analyzef1.data_management import DataHandler
from analyzef1.persistance.base import _DECL_BASE
from utils import get_driver_abbreviation

logger = logging.getLogger(__name__)


class SessionResult(_DECL_BASE):
    """
    Session model
    Keeps a record of session results.
    """

    __tablename__ = "session_result"

    id = Column(Integer, primary_key=True)
    analyzef1_id = Column(Integer, ForeignKey("season.id"))
    season = relationship("Season", back_populates="session_result")
    round_number = Column(Integer, nullable=False)
    event_name = Column(String(50), nullable=False)
    event_format = Column(String(25), nullable=False)
    session_type = Column(String(25), nullable=False)
    date = Column(DateTime, nullable=False)

    p1_drv = Column(String(25), nullable=True)
    p1_points = Column(Integer, nullable=True, default=0)
    p2_drv = Column(String(25), nullable=True)
    p2_points = Column(Integer, nullable=True, default=0)
    p3_drv = Column(String(25), nullable=True)
    p3_points = Column(Integer, nullable=True, default=0)
    p4_drv = Column(String(25), nullable=True)
    p4_points = Column(Integer, nullable=True, default=0)
    p5_drv = Column(String(25), nullable=True)
    p5_points = Column(Integer, nullable=True, default=0)
    p6_drv = Column(String(25), nullable=True)
    p6_points = Column(Integer, nullable=True, default=0)
    p7_drv = Column(String(25), nullable=True)
    p7_points = Column(Integer, nullable=True, default=0)
    p8_drv = Column(String(25), nullable=True)
    p8_points = Column(Integer, nullable=True, default=0)
    p9_drv = Column(String(25), nullable=True)
    p9_points = Column(Integer, nullable=True, default=0)
    p10_drv = Column(String(25), nullable=True)
    p10_points = Column(Integer, nullable=True, default=0)

    def __repr__(self) -> str:
        return f"Round Number: {self.round_number}, EventFormat: {self.event_format}"


class Season(_DECL_BASE):
    """
    Season model
    Keeps a record of all Sprints/Races results of the season
    """

    __tablename__ = "season"

    id = Column(Integer, primary_key=True)
    session_result = relationship(
        "SessionResult", order_by="SessionResult.id", cascade="all, delete-orphan"
    )
    round_number = Column(Integer, nullable=False)
    country = Column(String(25), nullable=False)
    location = Column(String(25), nullable=False)
    season_year = Column(Integer, nullable=False, default=datetime.now().year)
    event_name = Column(String(50), nullable=False)
    event_format = Column(String(25), nullable=False)
    date = Column(DateTime, nullable=False)

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __repr__(self) -> str:
        return f" Event Name: {self.event_name}, Event Format: {self.event_format}, Round Number: {self.round_number}"

    def delete(self):
        Season.query.session.delete(self)

    @staticmethod
    def rollback():
        Season.query.session.rollback()

    @staticmethod
    def add(session) -> None:
        logger.info(f"Adding {session} to database")
        Season.query.session.add(session)
        Season.query.session.commit()

    @staticmethod
    def get_db_season():
        return Season.query.all()

    @staticmethod
    def get_db_sessionresult():
        return SessionResult.query.all()

    @staticmethod
    def filter_drivers(driver_pos: int) -> List:
        """
        Get driver name and point based on the placement
        """
        driver = getattr(SessionResult, f"p{driver_pos}_drv")
        points = getattr(SessionResult, f"p{driver_pos}_points")
        return SessionResult.query.with_entities(driver, points).all()

    @staticmethod
    def leaderboard() -> Dict[str, int]:
        """
        Return the current drivers leaderboard for the seaon
        """
        drivers_list = get_driver_abbreviation(DRIVER_TEAM_MAPPING)
        drivers = {drv: 0 for drv in drivers_list}
        for j in range(1, 11):
            results = Season.filter_drivers(j)
            for result in results:
                drivers[result[0]] += result[1]

        return dict(sorted(drivers.items(), key=lambda item: item[1], reverse=True))

    @staticmethod
    def check_new_session():
        df = DataHandler.get_upcoming_events(type="past")
        # Remove training sessions where no points are givens
        df = df[~(df["EventFormat"] == "testing")]
        logger.info("Checking Events ...")
        for event in df.itertuples(name="Event"):
            if (
                Season.query.filter(Season.round_number == event.RoundNumber).first()
                == None
            ):
                logger.info(
                    f"RoundNumber {event.RoundNumber} not in database, adding now ..."
                )
                new_event = Season(
                    round_number=event.RoundNumber,
                    country=event.Country,
                    location=event.Location,
                    season_year=datetime.now().year,
                    event_name=event.EventName,
                    event_format=event.EventFormat,
                    date=event.Index,
                )
                Season.add(new_event)

                if event.EventFormat == "sprint":
                    session_sprint = ff1.get_session(
                        datetime.now().year, event.RoundNumber, "S"
                    )
                    session_sprint.load()
                    session_result = session_sprint.results
                    session_result = session_result.reset_index(drop=True)
                    new_session_sprint = SessionResult(
                        round_number=event.RoundNumber,
                        event_name=event.EventName,
                        event_format=event.EventFormat,
                        session_type="Sprint",
                        date=event.Session4Date,
                        p1_drv=session_result.loc[0, "Abbreviation"],
                        p1_points=session_result.loc[0, "Points"],
                        p2_drv=session_result.loc[1, "Abbreviation"],
                        p2_points=session_result.loc[1, "Points"],
                        p3_drv=session_result.loc[2, "Abbreviation"],
                        p3_points=session_result.loc[2, "Points"],
                        p4_drv=session_result.loc[3, "Abbreviation"],
                        p4_points=session_result.loc[3, "Points"],
                        p5_drv=session_result.loc[4, "Abbreviation"],
                        p5_points=session_result.loc[4, "Points"],
                        p6_drv=session_result.loc[5, "Abbreviation"],
                        p6_points=session_result.loc[5, "Points"],
                        p7_drv=session_result.loc[6, "Abbreviation"],
                        p7_points=session_result.loc[6, "Points"],
                        p8_drv=session_result.loc[7, "Abbreviation"],
                        p8_points=session_result.loc[7, "Points"],
                        p9_drv=session_result.loc[8, "Abbreviation"],
                        p9_points=session_result.loc[8, "Points"],
                        p10_drv=session_result.loc[9, "Abbreviation"],
                        p10_points=session_result.loc[9, "Points"],
                    )
                    Season.add(new_session_sprint)
                session_race = ff1.get_session(
                    datetime.now().year, event.RoundNumber, "R"
                )
                session_race.load()
                session_result = session_race.results
                session_result = session_result.reset_index(drop=True)
                new_session_race = SessionResult(
                    round_number=event.RoundNumber,
                    event_name=event.EventName,
                    event_format=event.EventFormat,
                    session_type="Race",
                    date=event.Session5Date,
                    p1_drv=session_result.loc[0, "Abbreviation"],
                    p1_points=session_result.loc[0, "Points"],
                    p2_drv=session_result.loc[1, "Abbreviation"],
                    p2_points=session_result.loc[1, "Points"],
                    p3_drv=session_result.loc[2, "Abbreviation"],
                    p3_points=session_result.loc[2, "Points"],
                    p4_drv=session_result.loc[3, "Abbreviation"],
                    p4_points=session_result.loc[3, "Points"],
                    p5_drv=session_result.loc[4, "Abbreviation"],
                    p5_points=session_result.loc[4, "Points"],
                    p6_drv=session_result.loc[5, "Abbreviation"],
                    p6_points=session_result.loc[5, "Points"],
                    p7_drv=session_result.loc[6, "Abbreviation"],
                    p7_points=session_result.loc[6, "Points"],
                    p8_drv=session_result.loc[7, "Abbreviation"],
                    p8_points=session_result.loc[7, "Points"],
                    p9_drv=session_result.loc[8, "Abbreviation"],
                    p9_points=session_result.loc[8, "Points"],
                    p10_drv=session_result.loc[9, "Abbreviation"],
                    p10_points=session_result.loc[9, "Points"],
                )
                Season.add(new_session_race)
