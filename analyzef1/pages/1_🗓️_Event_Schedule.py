import logging
from datetime import datetime

import streamlit as st

from analyzef1.data_management import DataHandler

logger = logging.getLogger(__name__)

def app():
    logger.info(f'Currently in page {__file__}')
    st.title(f'Event Schedule Season {datetime.now().year}')
    next_event, upcoming_events, past_events = DataHandler.get_upcoming_events()
    st.write("Next Event")
    st.dataframe(next_event)
    st.write("Upcoming")
    st.dataframe(upcoming_events)
    st.write("Past Events this season")
    st.dataframe(past_events)

app()