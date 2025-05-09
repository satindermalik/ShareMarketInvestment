# style_config.py

import streamlit as st

def apply_custom_styles():
    st.markdown(
        """
        <style>
        .stApp {
        background: url("https://t4.ftcdn.net/jpg/07/79/78/95/360_F_779789562_vm61H0o1a6Fjqk6jr0el6Kdgcx7rQgFY.jpg") no-repeat center center fixed;
        background-size: cover;
    }

    .block-container {
        background-color: rgba(255, 255, 255, 0.75);
        max-width: 100%;
        padding-left: 4rem;
        padding-right: 4rem;
    }

    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.87); /* Change alpha (0.2) as needed */
    }

    /* Optional: make widgets' container transparent */
    section[data-testid="stSidebar"] .css-ng1t4o {
        background-color: rgba(255, 255, 255, 0.0);
    }

    /* Optional: style text color to ensure readability */
    #section[data-testid="stSidebar"] * {
    #    color: black;
    #}
    section[data-testid="stSidebar"] button:nth-of-type(6) {
        background-color: #4CAF50 !important;  /* Green */
        color: white !important;
        
    }
        /* Title style */
        .custom-title {
            font-size: 30px;
            font-weight: 600;
            color: #1a1a1a;
            text-align: center;
            font-family: 'Arial', sans-serif;
            margin-top: 10px;
            margin-bottom: 20px;
        }

        /* Header style */
        .custom-header {
            font-size: 30px;
            font-weight: 600;
            color: #4CAF50;
            text-align: left;
            font-family: 'Verdana', sans-serif;
            margin-top: 10px;
            margin-bottom: 20px;
        }

        /* Add more styles as needed for other components */


        </style>
        """,
        unsafe_allow_html=True
    )
