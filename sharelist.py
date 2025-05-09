import psycopg2
import pandas as pd

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
                cur.execute('INSERT INTO futures SELECT ticker FROM smallcap WHERE "Type" = %s;', (selected_type,))

                # 3. Create or replace view
                cur.execute("""
                    CREATE OR REPLACE VIEW "StockDB".raw_dump AS
                    SELECT * FROM "StockDB".raw_dump_orignal
                    UNION
                    SELECT id, ticker, "date" + 1, "open", low, high, "close", volume, isprocessed, "3DayMA"
                    FROM "StockDB".raw_dump_orignal
                    WHERE "date" = (SELECT MAX("date") FROM "StockDB".raw_dump_orignal);
                """)

        conn.close()
        return "SQL Script executed successfully."

    except Exception as e:
        return f"Error: {e}"