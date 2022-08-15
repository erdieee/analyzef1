import logging
from datetime import datetime
from pathlib import Path

import streamlit as st

from analyzef1.persistance import init_db, Season, SessionResult
from utils import set_page_config, team_leaderboard_from_drivers


logger = logging.getLogger(__name__)

DB_FOLDER = f"{Path().resolve()}/database"
DB_URL = f"{DB_FOLDER}/Season_{datetime.now().year}.sqlite"

def database_connection():
    Path(DB_FOLDER).mkdir(parents=True, exist_ok=True) 
    init_db()
    Season.check_new_session()

def app() -> None:
    set_page_config()
    database_connection()
    st.title(f'Leaderboard for {datetime.now().year} Season')

    standings = st.tabs(['Drivers', 'Teams'])
    driver_leaderboard = Season.leaderboard()
    team_leaderboard = team_leaderboard_from_drivers(driver_leaderboard)

    with standings[0]:
        st.write('Driver standings')
        st.write(driver_leaderboard)
        
    with standings[1]: 
        st.write('Team standings')
        st.write(team_leaderboard)

app()