from typing import Dict, List

import streamlit as st

from analyzef1.constants import DRIVER_TEAM_MAPPING, TEAMS


def get_driver_abbreviation(drivers_dict: Dict) -> List[str]:
    drivers = []
    for i in list(drivers_dict.keys()):
        drivers.append(drivers_dict[i]["Abbreviation"])
    return drivers


def team_leaderboard_from_drivers(drivers_standings: Dict[str, int]) -> Dict[str, int]:
    teams = {team: 0 for team in TEAMS}
    for i in list(DRIVER_TEAM_MAPPING.keys()):
        drv = DRIVER_TEAM_MAPPING[i]["Abbreviation"]
        team = DRIVER_TEAM_MAPPING[i]["TeamName"]
        teams[team] += drivers_standings[drv]
    return dict(sorted(teams.items(), key=lambda item: item[1], reverse=True))


def set_page_config() -> None:
    st.set_page_config(page_title="AnalyzeF1", page_icon="🏎️", layout="wide")
    hide_streamlit_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
