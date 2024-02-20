import streamlit as st
import base64
import requests
import os
from connection import contract


def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)


def view_certificate(certificate_id):
    # Print Certificate ID
    
    # st.error("hello")
    try:
        result = contract.functions.getCertificate(certificate_id).call()
        if result[0] == "":
            st.error("Invalid Certificate ID!")
            return
    except Exception as e:
        st.error(f"Failed to retrieve certificate details: {e}")
        return
    
      # Print certificate details
    # st.write("Certificate details:", result)
   
    ipfs_hash = result[7]  # Assuming index 7 contains the IPFS hash, adjust if necessary
    # st.write("IPFS Hash:", ipfs_hash)

    pinata_gateway_base_url = 'https://gateway.pinata.cloud/ipfs'
    content_url = f"{pinata_gateway_base_url}/{ipfs_hash}"
    

    # Fetch PDF content from Pinata
    response = requests.get(content_url)

    
    with open("temp.pdf", 'wb') as pdf_file:
        pdf_file.write(response.content)

    # Display PDF
    displayPDF("temp.pdf")

    # Remove temporary PDF file
    os.remove("temp.pdf")
   



def hide_icons():
    hide_st_style = """
				<style>
				#MainMenu {visibility: hidden;}
				footer {visibility: hidden;}
				</style>"""
    st.markdown(hide_st_style, unsafe_allow_html=True)


def hide_sidebar():
    no_sidebar_style = """
    			<style>
        		div[data-testid="stSidebarNav"] {visibility: hidden;}
    			</style>"""
    st.markdown(no_sidebar_style, unsafe_allow_html=True)


def remove_whitespaces():
    st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>""", unsafe_allow_html=True)
