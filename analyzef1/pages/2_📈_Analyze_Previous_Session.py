from typing import Dict
import streamlit as st

from analyzef1.constants import CHOOSE_SESSION ,DRIVER_TEAM_MAPPING, NAVBAR, YEAR, LOCATION, SESSION
from analyzef1.data_management import DataHandler, Plotter
from utils import get_driver_abbreviation

def choose_session() -> Dict:
    col1, col2, col3 = st.columns(3)
    year_input = col1.selectbox(label = 'Choose year', options = YEAR, index=4)
    location_input = col2.selectbox(label = 'Choose Location',options = LOCATION)
    session_inpiut = col3.selectbox(label = 'Choose Session',options = SESSION, index=6)
    data = {
        'year': year_input,
        'location': location_input,
        'event': session_inpiut
    }
    return data

def app():
    st.title(f'Analyze Previous Session')
    data = choose_session()
    datahanlder = DataHandler(data)
    session = datahanlder.get_session()
    plotter = Plotter(datahanlder, session)
    st.sidebar.header("Analyze Session")
    navigation = st.sidebar.selectbox(label='Navigation', options=['Compare 2 Drivers', 'Color Map', 'All Laps'])
    if navigation == 'Compare 2 Drivers':
        col1, col2 = st.sidebar.columns(2)
        driver_1 = col1.selectbox('First Driver', get_driver_abbreviation(DRIVER_TEAM_MAPPING))
        driver_2 = col2.selectbox('Second Driver', get_driver_abbreviation(DRIVER_TEAM_MAPPING), index = 1)
        drivers_list = [driver_1, driver_2]
        max_lap_number = datahanlder.get_max_lap_number()
        lapnumber = st.sidebar.slider(label = 'Select Lap', min_value = 1, max_value = max_lap_number, value = 1)
        try:
            st.pyplot(plotter.compare_2_drv_lap(drivers_list, lapnumber))
        except:
            st.write("Data not available for both drivers...")
    if navigation == 'Color Map':
        color_map_switch = st.sidebar.radio(label = 'Choose Color Map', options = ['Speed', 'Gear Shifts'], horizontal = True)
        driver_select = st.sidebar.selectbox('Select Driver', get_driver_abbreviation(DRIVER_TEAM_MAPPING))
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
        
    if navigation == 'All Laps':
        st.write(plotter.boxplot_drivers_laps())
        st.write(plotter.plot_drivers_fastest_laps())
        st.write(plotter.racepace_laps())

app()