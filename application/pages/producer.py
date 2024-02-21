import streamlit as st
import os
import hashlib
from utils.cert_utils import extract_certificate
from utils.streamlit_utils import view_certificate
from connection import contract
from utils.streamlit_utils import displayPDF, hide_icons, hide_sidebar, remove_whitespaces
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyAIeaWiceVeYOWQSjTu1nSNNq_xDbcivpE",
  "authDomain": "recmpr-c4916.firebaseapp.com",
  "projectId": "recmpr-c4916",
  "storageBucket": "recmpr-c4916.appspot.com",
  "messagingSenderId": "289811255339",
  "appId": "1:289811255339:web:9dedb735efaf22dc815a6e",
  "measurementId": "G-N709H0H235",
  "databaseURL":"https://recmpr-c4916-default-rtdb.firebaseio.com/"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)

# Get a reference to the database service
db = firebase.database()

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()


options = ("Request Form for Renewable Energy Certificate (REC)", "View/Verify Certificate using Certificate ID")
selected = st.selectbox("", options, label_visibility="hidden")

if selected == options[0]:
    form = st.form("Generate-Certificate")
    customer_id = form.text_input(label="Customer ID")
    customer_name = form.text_input(label="Name")
    energy_source = form.text_input(label="Energy Source")
    capacity_generated = form.text_input(label="Capacity Generated(in mWh)")
    powerhouse_id = form.text_input(label="Powerhouse ID")
    powerhouse_name = form.text_input(label="Powerhouse Name")
    date_of_claim = form.text_input(label="Date of Claim")
    
    submit = form.form_submit_button("Submit")

    if submit:
        data = {
            'customer_id': customer_id,
            'customer_name': customer_name,
            'energy_source': energy_source,
            'capacity_generated': capacity_generated,
            'powerhouse_id': powerhouse_id,
            'powerhouse_name': powerhouse_name,
            'date_of_claim': date_of_claim,
            'status':'Pending'
        }
        db.child("users").push(data)
        st.success('Data submitted successfully!')

elif selected == options[1]:
    form = st.form("View-Certificate")
    certificate_id = form.text_input("Enter the Certificate ID")
    submit = form.form_submit_button("Submit")
    if submit:
        try:
            view_certificate(certificate_id)
        except Exception as e:
            st.error("Invalid Certificate ID!")