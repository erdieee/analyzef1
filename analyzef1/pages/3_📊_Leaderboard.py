import logging
from datetime import datetime, timedelta

import streamlit as st
from fastf1.ergast import Ergast

from analyzef1.data_management import DataHandler, Plotter
from analyzef1.utils import set_page_config


logger = logging.getLogger(__name__)


@st.cache_data
def get_race_schedule(year, _ergast):
    races = _ergast.get_race_schedule(year)
    return races


@st.cache_data
def get_driver_season_standings(_races, year, _ergast, reload_check):
    results = DataHandler.get_driver_season_standings(_races, year, _ergast)
    return results


@st.cache_data
def get_constructor_season_standings(_races, year, _ergast, reload_check):
    results = DataHandler.get_constructor_season_standings(_races, year, _ergast)
    return results


def should_reload():
    """
    Gets date of next monday. Used to check if standings should be reloaded
    """
    todayDate = datetime.today()
    # Increment today's date with 1 week to get the next Monday
    nextMonday = todayDate + timedelta(days=-todayDate.weekday(), weeks=1)
    return nextMonday


def app() -> None:
    set_page_config()
    st.title("Leaderboard")
    options = [*range(2005, datetime.today().year + 1)]
    year = st.selectbox("Select year", reversed(options), index=0)
    standings = st.tabs(["Driver", "Team"])
    reload_check = should_reload()
    ergast = Ergast()
    races = get_race_schedule(year, ergast)  # Races in year 2022
    with standings[0]:
        try:
            results = get_driver_season_standings(races, year, ergast, reload_check)
            st.plotly_chart(Plotter.leadboard_driver_heatmap_plot(results))
            st.pyplot(Plotter.leadboard_driver_line_plot(results, year))
        except Exception as e:
            logger.warning(e)
            st.info(f"Could not load data for year: {year}")
    with standings[1]:
        try:
            results = get_constructor_season_standings(
                races, year, ergast, reload_check
            )
            st.pyplot(Plotter.leadboard_constructor_line_plot(results, year))
        except Exception as e:
            logger.warning(e)
            st.info(f"Could not load data for year: {year}")


app()
