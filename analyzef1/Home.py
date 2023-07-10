#!/usr/bin/env python3
"""
Main analyzef1 script
"""

import logging
from pathlib import Path
from typing import Any, List

import streamlit as st

from utils import set_page_config

logger = logging.getLogger(__name__)

LOGFORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOGFORMAT)


def main() -> None:
    set_page_config()
    logger.info("Showing Home Page")
    st.title("Analyze Formula 1 🏎️")

    col1, col2 = st.columns([2, 2])
    col1.image(f"{Path().resolve()}/images/background/backgroundcrop.jpeg")
    col2.markdown("For all the **F1** nerds.")
    col2.markdown("Just a math student enjoying data")
    st.divider()
    st.subheader("Event Schedule")
    st.markdown(
        f"Display current race season. Next, upcoming and past events with session times."
    )
    st.subheader("Analyze Session")
    st.markdown(
        f"Analyze all previous sessions up to **2018**. If the session has just ended, the data should be available a few minutes later."
    )
    st.subheader("Leaderboard")
    st.markdown(f"Driver and constructor standings up to **2005**.")
    st.divider()
    st.markdown(
        f"In case you find any bugs or want to improve the page, make sure to open an issue or pull request on [Github](https://github.com/erdieee/analyzef1)."
    )


if __name__ == "__main__":
    main()
