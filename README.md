# Snowflake Tourism Data Explorer

An interactive Streamlit dashboard to explore tourism data stored in Snowflake. It provides country-wise visitor trends, gender distribution insights, and analytics on India’s famous and top-rated tourist places.

- Built with: Streamlit, Snowflake Connector for Python, Pandas, Plotly, python-dotenv
- Entry point: `app.py`
- Demo: https://mega.nz/file/VrBkkTwS#GVEnjLXysY46movYlw_3GhRSRsoHRK6JZ28JOnU20dg

## Features
- Country-wise yearly visitors (2014–2020) with trends, YoY growth heatmap, and COVID-19 impact view
- Gender distribution by country with trend lines, stacked bars, heatmap, and per-country breakdown
- India’s famous tourist places explorer with filters, cards, price/rating analysis, types by zone, and insights
- Top places to visit with popularity scoring, rating distribution, price vs rating, and rankings

## Project Structure
- `app.py` — Main Streamlit app and navigation
- `config.py` — Snowflake connection and data access helpers
- `country_visitors.py` — Country-wise visitors visuals
- `gender_analysis.py` — Gender distribution visuals
- `tourist_places.py` — Famous tourist places visuals
- `top_places.py` — Top places to visit visuals
- `.env.local` — Example environment file (copy to `.env` and fill)
- `requirements.txt` — Python dependencies

## Tech Stack
- Language: Python 3.8+
- App framework: Streamlit
- Data access: snowflake-connector-python
- Data manipulation: pandas
- Visualization: Plotly
- Config/Secrets: python-dotenv

## Quick Start
1) Python 3.8+ recommended

2) Install dependencies
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3) Configure environment
- Copy `.env.local` to `.env`
- Fill in your Snowflake credentials and context

Required variables in `.env`:
```
SNOWFLAKE_ACCOUNT=xy12345.us-east-1
SNOWFLAKE_USER=...
SNOWFLAKE_PASSWORD=...
SNOWFLAKE_ROLE=...
SNOWFLAKE_WAREHOUSE=...
SNOWFLAKE_DATABASE=TOURISM
SNOWFLAKE_SCHEMA=PUBLIC
```
Notes:
- `config.py` validates these variables at startup and will raise an error if any is missing.
- Data queries currently reference `TOURISM.PUBLIC.<TABLE_NAME>` explicitly in `config.get_table_data()`. If your data lives in a different database/schema, update the query there.

4) Run the app
```
streamlit run app.py
```
Open the URL shown in your terminal (typically http://localhost:8501).

## Snowflake Data Requirements
The app expects the following tables (in `TOURISM.PUBLIC` by default):

- COUNTRYWISEYEARLYVISITORS
  - Columns: `COUNTRY`, yearly columns like `'_2014' ... '_2020'` (numeric)

- COUNTRYWISEGENDER
  - Columns: `COUNTRY_OF_NATIONALITY`, yearly gender columns such as `'_2014_MALE'`, `'_2014_FEMALE'`, …, `'_2020_MALE'`, `'_2020_FEMALE'` (numeric percentages)

- INDIAFAMOUSTOURISTPLACES
  - Columns (used by the app): `NAME`, `ZONE`, `STATE`, `CITY`, `TIME_NEEDED_TO_VISIT_IN_HRS`, `ENTRANCE_FEE_IN_INR`, `GOOGLE_REVIEW_RATING`, `DSLR_ALLOWED`, `BEST_TIME_TO_VISIT`, `IMAGE_URL`, `TYPE`, `NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS`

- TOPPLACESTOVISIT
  - Columns (used by the app): `NAME`, `CITY`, `TYPE`, `GOOGLE_REVIEW_RATING`, `NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS`, `ENTRANCE_FEE_IN_INR`, `TIME_NEEDED_TO_VISIT_IN_HRS`

If your table or column names differ, adapt the code where the fields are referenced.

## Acknowledgements
This project was developed during the Snowflake hackathon "Your Story".
