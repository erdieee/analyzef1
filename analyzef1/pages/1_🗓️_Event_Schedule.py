import logging
from datetime import datetime

import streamlit as st
from analyzef1.data_management import DataHandler
from utils import set_page_config


logger = logging.getLogger(__name__)


@st.cache_data
def get_schedule():
    next_event, upcoming_events, past_events = DataHandler.get_upcoming_events()
    return next_event, upcoming_events, past_events


def events(events, type=None):
    event_names = events["EventName"].tolist()
    logger.info(event_names)
    if type == "next":
        containers = [st.container() for name in (event_names)]
    else:
        containers = [st.expander(name) for name in (event_names)]
    for i, event in enumerate(containers):
        with event:
            data = events.iloc[i]
            if type:
                st.header(f"{data['EventName']}")
            st.markdown(f"**Location:** {data['Location']}, {data['Country']}")
            st.markdown(
                f"**Event Number:** {data['RoundNumber']}, **Format:** {data['EventFormat']}"
            )
            cols = st.columns(5)
            for i, col in enumerate(cols):
                with col:
                    st.markdown(f"**Session {i + 1}**")
                    try:
                        st.markdown(f"{data[f'Session{i+1}']}")
                        st.markdown(
                            f"{data[f'Session{i+1}Date'].strftime('%d/%m/%Y, %H:%M:%S')}"
                        )
                    except:
                        st.markdown("No session")


def app() -> None:
    set_page_config()
    st.title(f"Event Schedule Season {datetime.now().year}")
    logger.info(f"Currently in page {__file__}")

    next_event, upcoming_events, past_events = get_schedule()
    event_schedule = st.tabs(["Next Event", "Upcoming Events", "Previous Events"])

    with event_schedule[0]:
        events(next_event, type="next")

    with event_schedule[1]:
        events(upcoming_events)

    with event_schedule[2]:
        events(past_events)


app()
