import streamlit as st

from home import show_home
from upload import show_upload

st.set_page_config(page_title="Cyber Defense Dashboard", layout="wide")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Home", "Upload"]
)

if page == "Home":
    show_home()

elif page == "Upload":
    show_upload()
