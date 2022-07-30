from datetime import datetime

import streamlit as st

def app():
    st.title(f'Leaderboard for {datetime.now().year} Season')
    st.write("This is the current leaderboard")

app()