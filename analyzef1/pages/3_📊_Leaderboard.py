from datetime import datetime

import streamlit as st

from utils import set_page_config

def app() -> None:
    set_page_config()
    st.title(f'Leaderboard for {datetime.now().year} Season')

    st.write("This is the current leaderboard")

app()