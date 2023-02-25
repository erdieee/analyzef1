import logging
from datetime import datetime

import streamlit as st

from analyzef1.data_management import DataHandler
from utils import set_page_config


logger = logging.getLogger(__name__)


def app() -> None:
    set_page_config()
    st.title(f"Event Schedule Season {datetime.now().year}")
    logger.info(f"Currently in page {__file__}")

    next_event, upcoming_events, past_events = DataHandler.get_upcoming_events()
    event_schedule = st.tabs(["Next Event", "Upcoming Events", "Previous Events"])

    with event_schedule[0]:
        st.write("Next Event")
        st.dataframe(next_event)
        body = "<style>    .race-container{        display: block;        max-width: 500px;        height: 75px;        background-color: #efefef;        border-radius: 5px;        padding: 10px;        font-family:sans-serif;    }    .race-container .expand{        width: 75px;        height: 100%;        text-align: center;        display: table;        border-right: 2px solid rgb(185, 185, 185);        font-weight: bold;        cursor: pointer;        float:left;    }    .race-container .status{        display: table;        float: right;        border-left: 2px solid rgb(185, 185, 185);        font-weight: bold;        width: 75px;        height: 100%;        text-align: center;    }    .race-container .vertical-align{        display: table-cell;        vertical-align: middle;    }    .race-container .info{        position: relative;        width: 326px;        height: 75px;        margin: auto;        padding-left: 10px;        padding-right: 10px;    }    .race-container .info .date{        position: absolute;        width: 90px;        text-align: center;        bottom:0px;        left: 10px;        padding-right: 10px;        font-weight: bold;    }    .race-container .info .name{        position: relative;        text-align: center;        top: 15px;        left: 10px;        height: 20px;        font-size: 20px;            }    .race-container .info .flag{        position: relative;        float: left;        width: 90px;        height: 50px;        border-radius: 5px;    }    .misc{        position: absolute;        text-align: center;        left: 100px;        width: 236px;        color:#999;        bottom: 0px;    }    .misc ul{        list-style: none;        padding:0px;        margin: 0px;    }    .misc li{        display: inline-block;        padding-right: 5px;    }    </style>"
        st.markdown(body, unsafe_allow_html=True)

    with event_schedule[1]:
        st.write("Upcoming")
        st.dataframe(upcoming_events)

    with event_schedule[2]:
        st.write("Past Events this season")
        st.dataframe(past_events)


app()
