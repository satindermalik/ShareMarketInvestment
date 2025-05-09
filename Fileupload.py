import streamlit as st
import os
import zipfile

#def save_uploaded_file(uploaded_file, folder="D:/MarketReport/inbound"):
def save_uploaded_file(uploaded_file, folder="/Users/satindermalik/Downloads/MarketInbound"):    
    # Create folder if it does not exist
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    file_path = os.path.join(folder, uploaded_file.name)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path

def extract_zip(file_path, extract_to="/Users/satindermalik/Downloads/MarketInbound"):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    return extract_to
