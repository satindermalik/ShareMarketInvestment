import streamlit as st
from sqlalchemy import create_engine
import psycopg2
import urllib.parse


def SyncTables():
    try:
        conn = psycopg2.connect(
        user="postgres",
        password="xxxx",
        host="localhost",
        port="5432",
        dbname="postgres"
    )
        cur = conn.cursor()

        cur.execute("SELECT SyncTables();")
        conn.commit() 
        result = cur.fetchone()
        print("Result:", result)

    except psycopg2.Error as e:
        print("Database error:", e)

    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
