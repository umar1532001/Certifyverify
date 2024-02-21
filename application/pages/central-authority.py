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
import pyrebase
import time
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

firebase = pyrebase.initialize_app(firebaseConfig)

# Get a reference to the database service
db = firebase.database()

# Streamlit app
st.title('Certificate Requests')

# Retrieve all data from Firebase
all_data = db.child("users").get()


options = ("Validate Certificate", "View Certificates")
selected = st.selectbox("", options, label_visibility="hidden")

if selected == options[0]:
    if all_data:
        for user in all_data.each():
            if user.val()['status']!='Accepted' and user.val()['status']!='Rejected':
                
                customer_id = user.val()['customer_id']
                customer_name = user.val()['customer_name']
                energy_source = user.val()['energy_source']
                capacity_generated = user.val()['capacity_generated']
                powerhouse_id = user.val()['powerhouse_id']
                powerhouse_name = user.val()['powerhouse_name']
                date_of_claim = user.val()['date_of_claim']
                
                st.write("ID:", customer_id)
                st.write("Customer Name:", customer_name)
                st.write("Energy Source:", energy_source)
                st.write("Capacity Generated:", capacity_generated)
                st.write("Powerhouse ID:", powerhouse_id)
                st.write("Powerhouse Name:", powerhouse_name)
                st.write("Date of Claim:", date_of_claim)

                accept_key = f"accept_{user.key()}"
                reject_key = f"reject_{user.key()}"
                
                accept = st.button("Accept", key=accept_key)
                reject = st.button("Reject", key=reject_key)

                if accept:

                    db.child("users").child(user.key()).update({"status": "Accepted"})
                    pdf_file_path = "certificate.pdf"
                    institute_logo_path = "../assets/logo.jpg"
                    data_to_hash=generate_certificate(pdf_file_path, customer_id, customer_name, energy_source, capacity_generated, powerhouse_id, powerhouse_name, date_of_claim, institute_logo_path)
                    # print(data_to_hash)
                    # Upload the PDF to Pinata
                    ipfs_hash = upload_to_pinata(pdf_file_path, api_key, api_secret)
                    os.remove(pdf_file_path)
                    #changes
                    # data_to_hash = f"{customer_id}{customer_name}{energy_source}{capacity_generated}{powerhouse_id}{powerhouse_name}{date_of_claim}".encode('utf-8')
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
                        
                        time.sleep(10)
                        st.experimental_rerun()

                    except Exception as e:
                        st.error(f"Failed to generate certificate: {e}")
                        print("Error:", e)
                elif reject:
                    db.child("users").child(user.key()).update({"status": "Rejected"})
                    st.warning(f"{customer_name} has been rejected!")
                    st.experimental_rerun()
                st.write("-" * 30)

else:
    form = st.form("View-Certificate")
    certificate_id = form.text_input("Enter the Certificate ID")
    submit = form.form_submit_button("Submit")
    if submit:
        try:
            
            view_certificate(certificate_id)
        except Exception as e:
            st.error("Invalid Certificate ID!")
