import logging
from pathlib import Path
import streamlit as st
from streamlit_option_menu import option_menu
from typing import Any

import fastf1 as ff1

from analyzef1.constants import CHOOSE_SESSION ,DRIVER_TEAM_MAPPING, NAVBAR, YEAR, LOCATION, SESSION
from analyzef1.data_management import Plotter, DataHandler
from utils import get_driver_abbreviation

logger = logging.getLogger(__name__)

class AnalyzeF1UI:
    """
    Class for AnalyzeF1 user interface
    """

    def __init__(self) -> None:
        self.data: dict
        self.datahanlder: Any
        self.plotter: Any
        self._configure_ui()
        
    def _configure_ui(self) -> None:
        st.set_page_config(
            page_title = "AnalyzeF1",
            page_icon = ":bar_chart:",
            layout = "wide"
        )
        hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
        st.image(f"{Path().resolve()}/backgroundcrop.jpeg")
        st.title("AnalyzeF1 🏎️")
        self._configure_navigation_bar()
        
    def _configure_navigation_bar(self):
        navbar = option_menu(
            menu_title = None,
            options = NAVBAR,
            orientation = "horizontal"
        )
        if navbar == "Upcoming Events":
            self.upcoming_event()
        if navbar == "Leaderboard":
            self.leaderboard()
        if navbar == "Previous Events":
            self.previous_events()

    def upcoming_event(self):
        next_event, upcoming_events, past_events = DataHandler.get_upcoming_events()
        st.write("Next Event")
        st.dataframe(next_event)
        st.write("Upcoming")
        st.dataframe(upcoming_events)
        st.write("Past Events this season")
        st.dataframe(past_events)

    def leaderboard(self):
        st.write("This is the current leaderboard")

    def previous_events(self):
        self._choose_event()
        self._configure_side_bar()

    def _choose_event(self):
        col1, col2, col3 = st.columns(3)
        year_input = col1.selectbox(label = 'Choose year', options = YEAR, index=4)
        location_input = col2.selectbox(label = 'Choose Location',options = LOCATION)
        session_inpiut = col3.selectbox(label = 'Choose Session',options = SESSION, index=6)
        self.data = {
            'year': year_input,
            'location': location_input,
            'event': session_inpiut
        }
        self.datahanlder = DataHandler(self.data)
        self.session = self.datahanlder.get_session()
        self.plotter = Plotter(self.datahanlder, self.session)

    def _configure_side_bar(self):
        st.sidebar.header("Analyze Session")
        lap_switcher = st.sidebar.radio(label='Laps Switcher', options=['Single Lap', 'All Laps'], horizontal=True)
        if lap_switcher == 'Single Lap':
            display_switcher = st.sidebar.radio(label='Select ', options=['Driver Color Map', 'Driver Telemetry Comparison'], horizontal=True)
            if display_switcher == 'Driver Color Map':
                driver_select = st.sidebar.selectbox('Select Driver', get_driver_abbreviation(DRIVER_TEAM_MAPPING))
                try:
                    st.write(self.plotter.driver_colormap_map(driver_select))
                except:
                    st.write("No Data available...")
            if display_switcher == 'Driver Telemetry Comparison':
                col1, col2 = st.sidebar.columns(2)
                driver_1 = col1.selectbox('First Driver', get_driver_abbreviation(DRIVER_TEAM_MAPPING))
                driver_2 = col2.selectbox('Second Driver', get_driver_abbreviation(DRIVER_TEAM_MAPPING), index = 1)
                drivers_list = [driver_1, driver_2]
                max_lap_number = self.datahanlder.get_max_lap_number()
                lapnumber = st.sidebar.slider(label = 'Select Lap', min_value = 1, max_value = max_lap_number, value = 1)
                try:
                    st.write(self.plotter.compare_2_drv_lap(drivers_list, lapnumber))
                except:
                    st.write("Data not available for both drivers...")
            
        if lap_switcher == 'All Laps':
            st.write(self.plotter.boxplot_drivers_laps())
            st.write(self.plotter.plot_drivers_fastest_laps())
            st.write(self.plotter.racepace_laps())