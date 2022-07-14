import logging
from pathlib import Path
import streamlit as st
from streamlit_option_menu import option_menu
from typing import Any

import fastf1 as ff1

from analyzef1.commands import CHOOSE_SESSION ,DRIVER_TEAM_MAPPING, UINAVBAR, YEAR, LOCATION, SESSION
from analyzef1.data_management import Analysis, DataHandler
from utils import get_driver_abbreviation

logger = logging.getLogger(__name__)

class AnalyzeF1UI:
    """
    Class for AnalyzeF1 user interface
    """

    def __init__(self) -> None:
        self.data: dict
        self.datahanlder: Any
        self.analysis: Any
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
            options = UINAVBAR,
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
        #st.write(self.datahanlder.get_drivers_fastest_lap()[['Driver', 'LapTime', 'LapTimeDelta']])
        #st.write(self.datahanlder.get_drivers_laps()[0].loc[1,'LapTime'])
        #st.write(self.datahanlder.get_fastest_lap())
        
        #st.dataframe(self.analysis.smoothed_laps())

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
        self.analysis = Analysis(self.datahanlder)

    def _configure_side_bar(self):
        st.sidebar.header("Analyze Session")
        lap_switcher = st.sidebar.radio(label='Laps Switcher', options=['Single Lap', 'All Laps'], horizontal=True)
        if lap_switcher == 'Single Lap':
            driver_select = st.sidebar.multiselect('Drivers', get_driver_abbreviation(DRIVER_TEAM_MAPPING))
            st.write(self.analysis.driver_colormap_map('LEC'))
            st.write(self.analysis.compare_2_drv_lap(['LEC', 'VER'], 5))
            
        if lap_switcher == 'All Laps':
            st.write(self.analysis.boxplot_drivers_laps())
            st.write(self.analysis.plot_drivers_fastest_laps())
            st.write(self.analysis.racepace_laps())