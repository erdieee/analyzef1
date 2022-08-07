import logging
from datetime import datetime
from pathlib import Path
from typing import Dict

import fastf1 as ff1
import pandas as pd
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
        self.session = self._get_session(data)

    def _get_session(self, data: dict):
        session = ff1.get_session(data['year'], data['location'], data['event'])
        session.load()
        return session

    @property
    def get_session(self):
        return self.session

    @property
    def get_laps(self):
        return self.session.laps

    @property
    def get_weather_data(self):
        return self.session.weather_data

    @property
    def get_max_lap_number(self):
        return int(max(self.session.laps['LapNumber']))

    @property
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
    def get_upcoming_events(type: str = None):
        df = ff1.get_event_schedule(datetime.now().year)
        filter_upcoming = df['EventDate'] > pd.to_datetime('today')
        past_events = df.loc[~filter_upcoming]
        df = df.loc[filter_upcoming]
        df.drop(columns='F1ApiSupport', inplace=True)
        df.set_index('EventDate', inplace=True)
        past_events.drop(columns='F1ApiSupport', inplace=True)
        past_events.set_index('EventDate', inplace=True)
        next_event = df.head(1)
        upcoming_event = df.tail(df.shape[0] - 1)
        if type == 'next':
            return next_event
        if type == 'upcoming':
            return upcoming_event
        if type == 'past':
            return past_events
        return next_event, upcoming_event, past_events