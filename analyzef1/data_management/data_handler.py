import logging
import pandas as pd
from pathlib import Path
from typing import Dict

import fastf1 as ff1
from fastf1.core import Laps

logger = logging.getLogger(__name__)
cachefolder = f'{Path().resolve()}/cache'

Path(cachefolder).mkdir(parents=True, exist_ok=True) 
ff1.Cache.enable_cache(cachefolder)
logger.info(f'Using cache folder: {cachefolder}')

class DataHandler:
    """
    Class responsable for getting and manipulating data
    """
    def __init__(self, data: Dict) -> None:
        self.cache = ff1.Cache.enable_cache(cachefolder)
        self.data = data
        self.session = self._get_session(self.data)

    def _get_session(self, data: dict):
        session = ff1.get_session(data['year'], data['location'], data['event'])
        session.load()
        return session

    def get_laps(self):
        return self.session.laps

    def get_session(self):
        return self.session

    def get_fastest_lap(self):
        return self.session.laps.pick_fastest()

    def get_drivers_fastest_lap(self):
        drivers = pd.unique(self.session.laps['Driver'])
        list_fastest_laps = list()
        for drv in drivers:
            drvs_fastest_lap = self.session.laps.pick_driver(drv).pick_fastest()
            list_fastest_laps.append(drvs_fastest_lap)
        fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)
        pole_lap = fastest_laps.pick_fastest()
        fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']
        return fastest_laps

    def get_drivers_laps(self):
        drivers = pd.unique(self.session.laps['Driver'])
        list_laps = list()
        for drv in drivers:
            drvs_laps = self.session.laps.pick_driver(drv)
            list_laps.append(drvs_laps)
        return list_laps

    @staticmethod
    def get_upcoming_events():
        df = ff1.get_event_schedule(2022)
        filter_upcoming = df['EventDate'] > pd.to_datetime('today')
        past_events = df.loc[~filter_upcoming]
        df = df.loc[filter_upcoming]
        df.drop(columns='F1ApiSupport', inplace=True)
        df.set_index('EventDate', inplace=True)
        next_event = df.head(1)
        upcoming_event = df.tail(df.shape[0] -1)
        return next_event, upcoming_event, past_events