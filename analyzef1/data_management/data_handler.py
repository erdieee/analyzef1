import logging
from datetime import datetime


import fastf1 as ff1
import pandas as pd
from fastf1.core import Laps


logger = logging.getLogger(__name__)


class DataHandler:
    """
    Class responsable for getting and manipulating data
    """

    @staticmethod
    def get_drivers_fastest_lap(session):
        drivers = pd.unique(session.laps["Driver"])
        list_fastest_laps = list()
        for drv in drivers:
            drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
            list_fastest_laps.append(drvs_fastest_lap)
        fastest_laps = (
            Laps(list_fastest_laps).sort_values(by="LapTime").reset_index(drop=True)
        )
        pole_lap = fastest_laps.pick_fastest()
        fastest_laps["LapTimeDelta"] = fastest_laps["LapTime"] - pole_lap["LapTime"]
        return fastest_laps

    @staticmethod
    def get_drivers_laps(session):
        drivers = pd.unique(session.laps["Driver"])
        list_laps = list()
        for drv in drivers:
            drvs_laps = session.laps.pick_driver(drv)
            list_laps.append(drvs_laps)
        return list_laps

    @staticmethod
    def get_upcoming_events(type: str = None):
        df = ff1.get_event_schedule(datetime.now().year)
        filter_upcoming = df["EventDate"] > pd.to_datetime("today")
        past_events = df.loc[~filter_upcoming]
        df = df.loc[filter_upcoming]
        df.drop(columns="F1ApiSupport", inplace=True)
        df.set_index("EventDate", inplace=True)
        past_events.drop(columns="F1ApiSupport", inplace=True)
        past_events.set_index("EventDate", inplace=True)
        next_event = df.head(1)
        upcoming_event = df.tail(df.shape[0] - 1)
        if type == "next":
            return next_event
        if type == "upcoming":
            return upcoming_event
        if type == "past":
            return past_events
        return next_event, upcoming_event, past_events

    @staticmethod
    def get_driver_season_standings(races, year, ergast):
        results = []
        for rnd, race in races["raceName"].items():
            try:
                temp = ergast.get_race_results(season=year, round=rnd + 1)
                temp = temp.content[0]
            except:
                break
            # If there is a sprint, get the results as well
            sprint = ergast.get_sprint_results(season=year, round=rnd + 1)
            if sprint.content and sprint.description["round"][0] == rnd + 1:
                temp = pd.merge(temp, sprint.content[0], on="driverCode", how="left")
                temp["points"] = temp["points_x"] + temp["points_y"]
                temp.drop(columns=["points_x", "points_y"], inplace=True)
            temp["round"] = rnd + 1
            temp["race"] = race.removesuffix(" Grand Prix")
            temp = temp[["round", "race", "driverCode", "points"]]
            results.append(temp)

        results = pd.concat(results)
        races = results["race"].drop_duplicates()
        results = results.pivot(index="driverCode", columns="round", values="points")
        # Rank the drivers by their total points
        results["total_points"] = results.sum(axis=1)
        results = results.sort_values(by="total_points", ascending=False)
        # results.drop(columns="total_points", inplace=True)
        results.columns = [*races, "Total"]
        return results

    @staticmethod
    def get_constructor_season_standings(races, year, ergast):
        results = []
        for rnd, race in races["raceName"].items():
            try:
                temp = ergast.get_constructor_standings(season=year, round=rnd + 1)
                temp = temp.content[0]
            except:
                break
            temp["round"] = rnd + 1
            results.append(temp)

        results = pd.concat(results)
        results = results.pivot(
            index="constructorName", columns="round", values="points"
        )
        results = results.sort_values(results.columns[-1], ascending=False)
        return results
