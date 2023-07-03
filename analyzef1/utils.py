from typing import Dict, List

import streamlit as st


def get_driver_abbreviation(drivers_dict: Dict) -> List[str]:
    drivers = []
    for i in list(drivers_dict.keys()):
        drivers.append(drivers_dict[i]["Abbreviation"])
    return drivers


def set_page_config() -> None:
    st.set_page_config(page_title="AnalyzeF1", page_icon="🏎️", layout="wide")
    hide_streamlit_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
