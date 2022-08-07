import logging
from datetime import datetime

import streamlit as st

from analyzef1.data_management import DataHandler
from utils import set_page_config

logger = logging.getLogger(__name__)

def app() -> None:
    set_page_config()
    st.title(f'Event Schedule Season {datetime.now().year}')
    logger.info(f'Currently in page {__file__}')

    next_event, upcoming_events, past_events = DataHandler.get_upcoming_events()
    event_schedule = st.tabs(['Next Event', 'Upcoming Event', 'Previous Events'])

    with event_schedule[0]:
        st.write("Next Event")
        st.dataframe(next_event)

    with event_schedule[1]:
        st.write("Upcoming")
        st.dataframe(upcoming_events)

    with event_schedule[2]:
        st.write("Past Events this season")
        st.dataframe(past_events)

app()