#!/usr/bin/env python3
"""
Main analyzef1 script
"""

import logging
from pathlib import Path
from typing import Any, List

import streamlit as st

logger = logging.getLogger('analyzef1')

LOGFORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOGFORMAT)
logger.info('Starting analyzef1 ...')

def main() -> None:
    st.set_page_config(
            page_title = "AnalyzeF1",
            page_icon = ":bar_chart:",
            layout = "wide"
        )
    hide_streamlit_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    st.image(f"{Path().resolve()}/images/background/backgroundcrop.jpeg")
    st.title("Analyze F1 🏎️")
    
if __name__ == "__main__": 
    main()