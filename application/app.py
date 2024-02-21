import streamlit as st
from PIL import Image
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()


st.title("Certificate Validation System")
st.write("")
st.subheader("Select Your Role")

col1, col2, col3 = st.columns(3)
institite_logo = Image.open("../assets/logo.jpg")
producer_logo = Image.open("../assets/spark.png")
with col1:
    st.image(producer_logo, output_format="jpg", width=230)
    clicked_producer = st.button("Producer")
with col2:
    st.image(institite_logo, output_format="jpg", width=230)
    clicked_institute = st.button("Central Authority")

company_logo = Image.open("../assets/company_logo.jpg")
with col3:
    st.image(company_logo, output_format="jpg", width=230)
    clicked_verifier = st.button("Verifier")

if clicked_institute:
    st.session_state.profile = "Central Authority"
    switch_page('login')
elif clicked_verifier:
    st.session_state.profile = "Verifier"
    switch_page('login')
elif clicked_producer:
    st.session_state.profile = "Producer"
    switch_page('login')