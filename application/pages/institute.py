import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import hashlib
from utils.cert_utils import generate_certificate
from utils.streamlit_utils import view_certificate
from connection import contract, w3
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

load_dotenv()

api_key = os.getenv("PINATA_API_KEY")
api_secret = os.getenv("PINATA_API_SECRET")


def upload_to_pinata(file_path, api_key, api_secret):
    # Set up the Pinata API endpoint and headers
    pinata_api_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": api_key,
        "pinata_secret_api_key": api_secret,
    }

    # Prepare the file for upload
    with open(file_path, "rb") as file:
        files = {"file": (file.name, file)}

        # Make the request to Pinata
        response = requests.post(pinata_api_url, headers=headers, files=files)

        # Parse the response
        result = json.loads(response.text)

        if "IpfsHash" in result:
            ipfs_hash = result["IpfsHash"]
            print(f"File uploaded to Pinata. IPFS Hash: {ipfs_hash}")
            return ipfs_hash
        else:
            print(f"Error uploading to Pinata: {result.get('error', 'Unknown error')}")
            return None


options = ("Generate Certificate", "View Certificates")
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
        pdf_file_path = "certificate.pdf"
        institute_logo_path = "../assets/logo.jpg"
        generate_certificate(pdf_file_path, customer_id, customer_name, energy_source, capacity_generated, powerhouse_id, powerhouse_name, date_of_claim, institute_logo_path)
    
        # Upload the PDF to Pinata
        ipfs_hash = upload_to_pinata(pdf_file_path, api_key, api_secret)
        os.remove(pdf_file_path)
        #changes
        data_to_hash = f"{customer_id}{customer_name}{energy_source}{capacity_generated}{powerhouse_id}{powerhouse_name}{date_of_claim}".encode('utf-8')
        certificate_id = hashlib.sha256(data_to_hash).hexdigest()
        
        # Smart Contract Call
        try:
            tx_hash = contract.functions.generateCertificate(
                certificate_id,
                customer_id,
                customer_name,
                energy_source,
                capacity_generated,
                powerhouse_id,
                powerhouse_name,
                date_of_claim,
                ipfs_hash
            ).transact({'from': w3.eth.accounts[0]})
            st.success(f"Certificate successfully generated with Certificate ID: {certificate_id}")
            print("Transaction Hash:", tx_hash.hex())
        except Exception as e:
            st.error(f"Failed to generate certificate: {e}")
            print("Error:", e)

else:
    form = st.form("View-Certificate")
    certificate_id = form.text_input("Enter the Certificate ID")
    submit = form.form_submit_button("Submit")
    if submit:
        try:
            
            view_certificate(certificate_id)
        except Exception as e:
            st.error("Invalid Certificate ID!")