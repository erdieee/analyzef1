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
    col1, col2 = st.columns([2, 2])
    col1.image(f"{Path().resolve()}/images/background/backgroundcrop.jpeg")
    col2.title("Analyze F1 🏎️")
    col2.write("For all the F1 nerds.")
    st.markdown("---")
    st.write("Just a math student enjoying data")


if __name__ == "__main__":
    main()
