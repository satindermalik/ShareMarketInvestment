import streamlit as st
from sqlalchemy import create_engine
import psycopg2
import urllib.parse
import pandas as pd

def run_buy_sell(number_of_share,values,start_date, run_date, current_date):
    try:
        conn = psycopg2.connect(
            user="postgres",
            password="xxxx",
            host="localhost",
            port="5432",
            dbname="postgres"
        )
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM public.RunBuySell(%s,%s, %s, %s, %s);",
            (number_of_share,values ,start_date, run_date, current_date)
        )
        conn.commit()   
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows, columns=colnames)
        cur.close()
        conn.close()
        return df
    except Exception as e:
        return f"Error: {e}"
    
