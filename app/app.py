import streamlit as st

from home import show_home
from upload import show_upload
from compute import show_compute_kpi

st.set_page_config(page_title="Cyber Defense Dashboard", layout="wide")

st.sidebar.title("Navigation")


page = st.sidebar.radio(
    "Go to",
    ["Home", "Upload", "Compute KPI"]
)

if page == "Home":
    show_home()

elif page == "Upload":
    show_upload()

elif page == "Compute KPI":
    show_compute_kpi()

