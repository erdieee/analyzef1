import logging 
from typing import Dict

import streamlit as st

from analyzef1.constants import CHOOSE_SESSION ,DRIVER_TEAM_MAPPING, NAVBAR, YEAR, LOCATION, SESSION
from analyzef1.data_management import DataHandler, Plotter
from utils import get_driver_abbreviation, set_page_config


logger = logging.getLogger(__name__)

def choose_session() -> Dict:
    col1, col2, col3 = st.columns(3)
    year_input = col1.selectbox(label = 'Choose year', options = YEAR, index=4)
    location_input = col2.selectbox(label = 'Choose Location', options = LOCATION)
    session_input = col3.selectbox(label = 'Choose Session', options = SESSION, index=6)
    data = {
        'year': year_input,
        'location': location_input,
        'event': session_input
    }
    return data

def race_info(datahanlder) -> None:
    col1, col2, col3 = st.columns(3)
    weather_data = datahanlder.get_weather_data
    air_temp_mean = weather_data['AirTemp'].mean()
    track_temp_mean =  weather_data['TrackTemp'].mean()
    humidity_mean = weather_data['Humidity'].mean()
    col1.metric(label = 'Mean Air Temperature', value = f'{air_temp_mean:0.2f} °C')
    col2.metric(label = 'Mean Track Temperature', value = f'{track_temp_mean:0.2f} °C')
    col3.metric(label = 'Mean Humidity', value = f'{humidity_mean:0.2f} %')

def app() -> None:
    set_page_config()
    st.title(f'Analyze Previous Session')

    st.subheader('Choose Session')
    data = choose_session()
    datahanlder = DataHandler(data)
    session = datahanlder.get_session
    plotter = Plotter(datahanlder, session)
    race_info(datahanlder)

    st.subheader('Choose analytics')
    analyze_session = st.tabs(['Compare 2 Drivers', 'Color Map', 'All Laps'])
    placeholder = st.empty()

    with analyze_session[0]:
        col1, col2, col3 = st.columns([1,1,2])
        driver_1 = col1.selectbox('First Driver', get_driver_abbreviation(DRIVER_TEAM_MAPPING))
        driver_2 = col2.selectbox('Second Driver', get_driver_abbreviation(DRIVER_TEAM_MAPPING), index = 1)
        drivers_list = [driver_1, driver_2]
        max_lap_number = datahanlder.get_max_lap_number
        lapnumber = col3.slider(label = 'Select Lap', min_value = 1, max_value = max_lap_number, value = 1)
        try:
            st.pyplot(plotter.compare_2_drv_lap(drivers_list, lapnumber))
        except:
            st.write("Data not available for both drivers...")

    with analyze_session[1]:
        col1, col2 = st.columns([1,1])
        color_map_switch = col1.selectbox(label = 'Choose Color Map', options = ['Speed', 'Gear Shifts'])
        driver_select = col2.selectbox('Select Driver', get_driver_abbreviation(DRIVER_TEAM_MAPPING))
        if color_map_switch == 'Speed':
            try:
                st.write(plotter.colormap_map_speed(driver_select))
            except:
                st.write("No Data available...")

        if color_map_switch == 'Gear Shifts':
            try:
                st.write(plotter.colormap_map_gear_shifts(driver_select))
            except:
                st.write("No Data available...")

    with analyze_session[2]:
        st.write(plotter.boxplot_drivers_laps())
        st.write(plotter.plot_drivers_fastest_laps())
        st.write(plotter.racepace_laps())

app()