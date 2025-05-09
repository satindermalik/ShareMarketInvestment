import streamlit as st
import os
import zipfile
import urllib.parse
import glob
from sqlalchemy import create_engine
from Fileupload import save_uploaded_file
from Fileupload import extract_zip
from read_csv import read_multiple_csv
from SyncTables import SyncTables
from RunBySell import run_buy_sell
import pandas as pd
import time
import psycopg2
from style_config import apply_custom_styles
from PIL import Image

#logo_path="/Users/satindermalik/Downloads/DataScience/logo.jpg"

#logo = Image.open(logo_path)  # Make sure this file exists
#st.image(logo, width=200)  # You can change the width


@st.cache_resource 
def get_connection():
    conn = psycopg2.connect(
        user="postgres",
        password="xxxx",
        host="localhost",
        port="5432",
        dbname="postgres"
    )
    return conn

def run_query_df(sql, params=None):
    engine = create_engine("postgresql+psycopg2://postgres:malik@localhost:5432/postgres")
    return pd.read_sql_query(sql, con=engine, params=params)


#st.title("Daily Run For Long-Term Share Market Investment")
apply_custom_styles()

# Title with custom style
st.markdown('<div class="custom-title">Daily Run For Long-Term Share Market Investment</div>', unsafe_allow_html=True)

# Header with different style
st.markdown('<div class="custom-header">Welcome to the Investment Dashboard</div>', unsafe_allow_html=True)


df_date=run_query_df('SELECT max(date) as max_date from "StockDB".raw_dump_orignal')
till_date=df_date.loc[0,"max_date"]

st.subheader(f"App have data till: {till_date}")

##### Upload Zip file #######
uploaded_file = st.file_uploader("Choose a ZIP file", type=["zip"], key=st.session_state.get("file_uploader_key", "default"))

# Only process the uploaded file if it's not already handled
if uploaded_file is not None and "file_processed" not in st.session_state:
    file_path = save_uploaded_file(uploaded_file)
    extracted_folder = extract_zip(file_path)

    st.session_state["file_path"] = file_path
    st.session_state["extracted_folder"] = extracted_folder
    st.session_state["file_processed"] = True  # Mark as done

    st.success(f"File saved to: {file_path}")
    st.success(f"Files extracted to: {extracted_folder}")

# Ensure extracted folder is available
if "extracted_folder" in st.session_state:
    st.subheader("Click on Read CSV button to load all CSV files")
    if st.button("Read CSV"):
        # Read all CSV files using read_multiple_csv
        df = read_multiple_csv(st.session_state["extracted_folder"])
        
        # Store dataframe in session state
        st.session_state["df"] = df
        
        # Display first few rows
        st.write("### Processed Data:")
        st.dataframe(df.head())
    
# Ensure df is available for cleaning
if "df" in st.session_state:
    st.subheader("Click on Data Clean button to clean the Report")
    if st.button("Data Clean"):
        df = st.session_state["df"].copy()  # Copy dataframe from session state
        
        #### Drop the Columns which are not required
        df.drop(['BizDt', 'Sgmt', 'Src', 'FinInstrmTp', 'FinInstrmId', 'ISIN', 'XpryDt', 'FininstrmActlXpryDt', 'StrkPric', 'OptnTp', 'FinInstrmNm', 'LastPric', 'PrvsClsgPric', 'UndrlygPric', 'SttlmPric', 'OpnIntrst', 'ChngInOpnIntrst', 'TtlTradgVol', 'TtlTrfVal', 'TtlNbOfTxsExctd',
                 'SsnId', 'NewBrdLotQty', 'Rmks', 'Rsvd1', 'Rsvd2', 'Rsvd3', 'Rsvd4'], axis=1, inplace=True, errors="ignore")
        
        #### Filter the Data ####
        final_df = df[df['SctySrs'].isin(['BE', 'EQ'])]

        ### Drop the SctySrs column 
        final_df.drop(['SctySrs'], axis=1, inplace=True, errors="ignore")

        ### Rename columns Name
        final_df.rename(columns={
            "TradDt": "date", 
            "TckrSymb": "ticker", 
            "OpnPric": "open", 
            "HghPric": "high", 
            "LwPric": "low", 
            "ClsPric": "close"
        }, inplace=True)

        # Store cleaned dataframe in session state
        st.session_state["final_df"] = final_df

        # Display final Data few rows
        st.write("### Cleaned Data:")
        st.dataframe(final_df.head())

        st.write(f"### Total number of Cleaned Data: {final_df.shape[0]}")

# Ensure final_df is available for database insertion
if "final_df" in st.session_state:
    st.subheader("Click on DB Connection button to store data")
    if st.button("Insert Data into DB"):
        try:
            # Database credentials
            DB_USER = "postgres"
            DB_PASSWORD = 'xxxx'
            DB_PASSWORD_ENCODED = urllib.parse.quote(DB_PASSWORD)
            DB_HOST = "localhost"  # e.g., "localhost" or an IP address
            DB_PORT = "5432"       # Default PostgreSQL port
            DB_NAME = "postgres"

            # Create SQLAlchemy engine
            
            engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD_ENCODED}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

            # Define correct column mapping
            column_mapping = {'date': 'date', 'ticker': 'ticker', 'open': 'open', 'high': 'high', 'low': 'low', 'close': 'close'}

            # Rename DataFrame columns based on mapping
            df_renamed = st.session_state["final_df"].rename(columns=column_mapping)

            # Insert into PostgreSQL table
            df_renamed.to_sql(
                name="raw_dump_orignal",  # Table name
                con=engine,
                schema="StockDB",  # Schema name
                if_exists="append", 
                index=False
            )

            st.success("Data successfully inserted into the database!")

        except Exception as e:
            st.error(f"Error while inserting into DB: {e}")


##### code to delete multiple extensions type file from inbound folder ###

#if uploaded_file is not None:
st.subheader("Delete file from inbound folder")

if st.button("Delete files"):
    folder_path = "/Users/satindermalik/Downloads/MarketInbound"
    file_extensions = ["*.zip", "*.csv"]
    deleted = False

    for ext in file_extensions:
        for file in glob.glob(os.path.join(folder_path, ext)):
            try:
                os.remove(file)
                deleted = True
            except Exception as e:
                st.error(f"Error deleting {file}: {e}")

    # Clear session state to avoid re-processing
    for key in ["file_path", "extracted_folder", "file_processed", "df", "final_df"]:
        st.session_state.pop(key, None)

    # Force re-render of file_uploader to reset it visually
    st.session_state["file_uploader_key"] = str(time.time())

    if deleted:
        st.success("Files deleted and session state cleared.")
    else:
        st.info("No matching files found.")


# Run the SyncTable function


st.subheader("Click on SyncTable button to Update data")
if st.button("SyncTable"):
        try:
            status=SyncTables()
            st.write(status)

            st.success("SyncTable fuction run sucessfully")
        except Exception as e:
            st.error(f"Error while running the SyncTable function :{e}")

### Input for share ShareType
# --- Query helper using SQLAlchemy ---


# --- Get distinct share types for dropdown ---


df_types = run_query_df('SELECT DISTINCT "Type" AS type FROM smallcap ORDER BY 1 ASC')
share_types = df_types['type'].dropna().unique().tolist()

# --- Dropdown UI ---

st.sidebar.subheader("Select Share Type")
selected_type = st.sidebar.selectbox("Share Type", share_types)


# --- SQL Script Function ---
def run_sql_script(selected_type):
    try:
        conn = psycopg2.connect(
            user="postgres",
            password="malik",
            host="localhost",
            port="5432",
            dbname="postgres"
        )

        with conn:
            with conn.cursor() as cur:
                # 1. Delete from futures
                cur.execute("DELETE FROM futures;")

                # 2. Insert filtered tickers
                cur.execute(
                    'INSERT INTO futures SELECT ticker FROM smallcap WHERE "Type" = %s;',
                    (selected_type,)
                )

                # 3. Safely create or replace the view with valid date arithmetic
                cur.execute("""
                    CREATE OR REPLACE VIEW "StockDB".raw_dump AS
                    SELECT * FROM "StockDB".raw_dump_orignal
                    UNION
                    SELECT id, ticker, ("date" + INTERVAL '1 day')::DATE AS date, "open", low, high, "close", volume, isprocessed, "3DayMA"
                    FROM "StockDB".raw_dump_orignal
                    WHERE "date" = (SELECT MAX("date") FROM "StockDB".raw_dump_orignal);
                """)

        conn.close()
        return "SQL script executed successfully."

    except Exception as e:
        return f"Error: {e}"

# --- Trigger SQL script on button click with spinner ---
if st.sidebar.button("Submit"):
    with st.spinner("Running SQL script..."):
        result = run_sql_script(selected_type)

    if result.startswith("Error"):
        st.error(result)
    else:
        st.success(result)


#  Inputs for RunBuySell

from datetime import datetime, date,timedelta

default_date = date(2025, 4, 7)

st.subheader("RunBuySell Parameters")

number_of_share = st.number_input("Number of Shares", value=10, min_value=1, step=1)
values=st.number_input("values",value=20)
start_date = st.date_input("Start Date", value=default_date)
run_date = st.date_input("Run Date", value=start_date+ timedelta(days=1))
current_date = st.date_input("Current Date", value=datetime.now().date())

#  RunBuySell Button
if st.button("Run RunBuySell"):
    st.subheader("Running RunBuySell... ⏳")
    
    timer_placeholder = st.empty()
    spinner_placeholder = st.empty()

    start_time = time.time()

    # Start spinner + live timer
    with spinner_placeholder.container():
        with st.spinner("Processing..."):
            while True:
                elapsed = time.time() - start_time
                timer_placeholder.markdown(f"⏱️ Elapsed Time: **{elapsed:.1f} seconds**")
                time.sleep(0.1)  # refresh rate

                # Stop condition: after function completes
                if elapsed > 5:  # simulate stop after ~5s
                    break

    # Call the function (simulate real call)
    result = run_buy_sell(number_of_share, values, start_date, run_date, current_date)

    # Final time
    final_time = time.time() - start_time

    # Cleanup spinners and show results
    spinner_placeholder.empty()
    timer_placeholder.markdown(f"✅ Completed in **{final_time:.2f} seconds**")

    if not result.empty:
        st.success(f"{len(result)} row(s) returned.")
        st.dataframe(result)
    else:
        st.warning("No data returned.")


## get the list of share
st.markdown("""
    <style>
        /* Style the first stButton (which should be your 'Get Share List' button) */
        div.stButton > button:first-child {
            background-color: #28a745; /* green */
            color: white;
            border-radius: 8px;
            
        }
    </style>
""", unsafe_allow_html=True)

if st.button("Get Share List"):
    try:
        share_list = run_query_df("""
            SELECT 
                h.ticker,
                h.reffdate,
                h.close AS holding_close,
                h.cagr,
                h.pergain,
                h.actiontype,
                h.actiondate,
                h.actionprice,
                d."close" AS latest_close
            FROM holdings h
            JOIN "StockDB".raw_dump d  
              ON d.ticker = h.ticker 
             AND d."date" = (SELECT MAX("date") FROM "StockDB".raw_dump_orignal)
            ORDER BY h.reffdate DESC;
        """)
        holding = run_query_df("select * from holdings_log order by actiondate desc ;")
        LogTran = run_query_df("select shares,b_amount,b_ticker,b_actiontype,b_actiondate,b_actionprice,s_ticker,s_actiontype,s_actiondate,s_actionprice,total_gain,total_gain_per from log_transection order by s_actiondate desc;")
        holdinggain = run_query_df("""select * from drawdown where "Type"='Holding' order by  reviewdate desc;""")        
        if not share_list.empty:
            st.dataframe(share_list)
            st.dataframe(holding)
            st.dataframe(LogTran)
            st.dataframe(holdinggain)
        else:
            st.warning("No data returned.")

    except Exception as e:
        st.error(f"Error fetching share list: {e}")


