# 📈 Long-Term Stock Market Investment Dashboard

This Streamlit-based dashboard provides a comprehensive tool for managing long-term stock market investments. It allows users to upload stock data, clean and process it, store it in a PostgreSQL database, and analyze/share recommendations based on a custom buy/sell strategy.

---

## 🚀 Features

* **ZIP File Upload & Extraction**: Upload compressed stock data files (.zip) and automatically extract them.
* **CSV Reading & Cleaning**: Load and clean multiple CSVs to remove unneeded columns and filter by relevant share types.
* **Database Insertion**: Cleaned data can be pushed into a PostgreSQL database under a specific schema.
* **SyncTables Functionality**: Keeps internal tables synchronized after uploads.
* **Share Type Filtering**: Filter data and perform SQL operations based on the selected share type.
* **Buy/Sell Strategy Runner**: Run custom investment strategies with configurable parameters.
* **View Reports**: Retrieve latest holdings, transaction logs, and gain/loss reports.
* **Session-State Management**: Streamlit's session management prevents reprocessing already-handled files.

---

## 🧰 Requirements

* Python 3.8+
* PostgreSQL (configured locally)
* Python packages:

  * `streamlit`
  * `pandas`
  * `sqlalchemy`
  * `psycopg2`
  * `Pillow`
  * custom modules: `Fileupload`, `read_csv`, `SyncTables`, `RunBySell`, `style_config`

---

## 🏗️ Project Structure

```
.
├── main_app.py
├── Fileupload.py
├── read_csv.py
├── SyncTables.py
├── RunBySell.py
├── style_config.py
├── requirements.txt
└── README.md
```

---

## 🛠️ Setup Instructions

1. **Clone the Repository**

```bash
git clone https://your-repo-url.git
cd your-repo
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Start PostgreSQL Locally**
   Make sure PostgreSQL is running and accessible at:

```
user: postgres
password:
host: localhost
port: 5432
database: postgres
```

Ensure schema `StockDB` and tables are pre-configured accordingly.

4. **Run the App**

```bash
streamlit run main_app.py
```

---

## 💡 How to Use

1. Upload your stock ZIP file.
2. Read and clean the CSV files.
3. Insert cleaned data into the database.
4. Sync tables.
5. Choose a share type.
6. Execute SQL script to refresh views.
7. Run the buy/sell strategy.
8. View results and holding reports.

---

## 📊 Sample Outputs

* DataFrames showing processed stock data
* Holdings reports with CAGR and percentage gain
* Transaction logs and drawdown reports

---

## 🧪 Notes

* Ensure local PostgreSQL database is configured correctly.
* Cleaned data is inserted into the `StockDB.raw_dump_orignal` table.
* The app includes dynamic SQL view updates and session-based logic for smooth interaction.

---

## 📬 Contact

For queries or feedback, contact the developer at: \[[your-email@example.com](mailto:your-email@example.com)]

---

## 📝 License

MIT License
