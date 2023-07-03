import logging
from datetime import datetime
from typing import Dict
import streamlit as st
import pandas as pd
import fastf1 as ff1

from analyzef1.data_management import DataHandler, Plotter
from utils import get_driver_abbreviation, set_page_config


logger = logging.getLogger(__name__)


def get_session_options():
    year_options = [year for year in range(2018, datetime.now().year + 1)]
    options = {"year": year_options, "events": {}, "event_types": {}}
    for year in year_options:
        season = ff1.get_event_schedule(year)
        events = season["EventName"].tolist()
        events = [event for event in events if "pre" not in event.lower()]
        options["events"].update({year: events})
        options["event_types"][year] = {}
        for event in events:
            column = season.loc[season["EventName"] == event]
            temp = {
                event: [
                    *column[
                        [
                            "Session1",
                            "Session2",
                            "Session3",
                            "Session4",
                            "Session5",
                        ]
                    ].values[0]
                ]
            }
            options["event_types"][year].update(temp)
    return options


def choose_session() -> Dict:
    col1, col2, col3 = st.columns(3)
    options = get_session_options()
    year_input = col1.selectbox(
        label="Choose year", options=(year := options["year"]), index=len(year) - 1
    )
    event_input = col2.selectbox(
        label="Choose Location", options=options["events"][year_input]
    )
    session_input = col3.selectbox(
        label="Choose Session",
        options=(event_type := options["event_types"][year_input][event_input]),
        index=len(event_type) - 1,
    )
    data = {"year": year_input, "event": event_input, "event_type": session_input}
    return data


@st.cache_data
def load_session(data: dict):
    session = ff1.get_session(data["year"], data["event"], data["event_type"])
    session.load()
    return session


def race_info(session) -> None:
    col1, col2, col3 = st.columns(3)
    weather_data = session.weather_data
    air_temp_mean = weather_data["AirTemp"].mean()
    track_temp_mean = weather_data["TrackTemp"].mean()
    humidity_mean = weather_data["Humidity"].mean()
    col1.metric(label="Mean Air Temperature", value=f"{air_temp_mean:0.2f} °C")
    col2.metric(label="Mean Track Temperature", value=f"{track_temp_mean:0.2f} °C")
    col3.metric(label="Mean Humidity", value=f"{humidity_mean:0.2f} %")


def app() -> None:
    set_page_config()
    st.title(f"Analyze Previous Session")
    st.subheader("Choose Session")
    data = choose_session()
    session = load_session(data)
    st.subheader("Choose analytics")
    analyze_session = st.tabs(
        ["Compare 2 Drivers", "All Laps", "Color Map", "Race infos"]
    )
    drivers = session.results["Abbreviation"].tolist()
    with analyze_session[0]:
        col1, col2, col3 = st.columns([1, 1, 2])
        driver_1 = col1.selectbox("First Driver", drivers)
        driver_2 = col2.selectbox("Second Driver", drivers, index=1)
        drivers_list = [driver_1, driver_2]
        max_lap_number = session.total_laps
        lapnumber = col3.slider(
            label="Select Lap", min_value=1, max_value=max_lap_number, value=1
        )
        try:
            st.pyplot(Plotter.compare_2_drv_lap(session, drivers_list, lapnumber))
        except Exception as e:
            logger.warning(e)
            st.write("Data not available for both drivers...")

    with analyze_session[1]:
        st.pyplot(Plotter.driver_position_during_race(session))
        st.write(Plotter.boxplot_drivers_laps(session))
        st.write(Plotter.plot_drivers_fastest_laps(session))
        # st.write(Plotter.racepace_laps(session))

    with analyze_session[2]:
        col1, col2 = st.columns(2)
        color_map_switch = col1.selectbox(
            label="Choose Color Map", options=["Speed", "Gear Shifts"]
        )
        driver_select = col2.selectbox("Select Driver", drivers)
        if color_map_switch == "Speed":
            try:
                st.write(Plotter.colormap_map_speed(session, driver_select))
            except:
                st.write("No Data available...")

        if color_map_switch == "Gear Shifts":
            try:
                st.write(Plotter.colormap_map_gear_shifts(session, driver_select))
            except:
                st.write("No Data available...")

    with analyze_session[3]:
        race_info(session)


app()
