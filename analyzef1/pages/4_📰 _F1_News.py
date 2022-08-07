import streamlit as st

from utils import set_page_config

def app() -> None:
    set_page_config()
    st.title('Latest F1 news')

    st.write('Here you willl find the latest F1 news.')

app()