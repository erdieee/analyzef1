import logging
from datetime import datetime

import streamlit as st
from fastf1.ergast import Ergast
import plotly.express as px
from plotly.io import show

from analyzef1.data_management import DataHandler
from analyzef1.utils import set_page_config


logger = logging.getLogger(__name__)


@st.cache_data
def get_race_schedule(year, _ergast):
    races = _ergast.get_race_schedule(year)  # Races in year 2022
    return races


@st.cache_data
def get_driver_season_standings(_races, year, _ergast):
    results = DataHandler.get_driver_season_standings(_races, year, _ergast)
    return results


@st.cache_data
def get_constructor_season_standings(_races, year, _ergast):
    results = DataHandler.get_constructor_season_standings(_races, year, _ergast)
    return results


def app() -> None:
    set_page_config()
    st.title("Leaderboard")
    options = [*range(2005, datetime.today().year + 1)]
    year = st.selectbox("Select year", reversed(options), index=0)
    standings = st.tabs(["Driver", "Team"])

    ergast = Ergast()
    races = get_race_schedule(year, ergast)  # Races in year 2022
    with standings[0]:
        try:
            results = get_driver_season_standings(races, year, ergast)
            fig = px.imshow(
                results,
                text_auto=True,
                aspect="auto",  # Automatically adjust the aspect ratio
                color_continuous_scale=[
                    [0, "rgb(198, 219, 239)"],  # Blue scale
                    [0.25, "rgb(107, 174, 214)"],
                    [0.5, "rgb(33,  113, 181)"],
                    [0.75, "rgb(8,   81,  156)"],
                    [1, "rgb(8,   48,  107)"],
                ],
                labels={
                    "x": "Race",
                    "y": "Driver",
                    "color": "Points",
                },  # Change hover texts
            )
            fig.update_xaxes(title_text="")  # Remove axis titles
            fig.update_yaxes(title_text="")
            fig.update_yaxes(tickmode="linear")  # Show all ticks, i.e. driver names
            fig.update_yaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor="LightGrey",
                showline=False,
                tickson="boundaries",
            )  # Show horizontal grid only
            fig.update_xaxes(showgrid=False, showline=False)  # And remove vertical grid
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")  # White background
            fig.update_layout(coloraxis_showscale=False)  # Remove legend
            fig.update_layout(xaxis=dict(side="top"))  # x-axis on top
            fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))  # Remove border margins
            st.plotly_chart(fig)
        except Exception as e:
            logger.warning(e)
            st.info(f"Could not load data for year: {year}")
    with standings[1]:
        # try:
        #     # results = get_constructor_season_standings(races, year, ergast)
        #     st.dataframe(results)
        # except Exception as e:
        #     logger.warning(e)
        st.info("Not implemented yet .. ")


app()
