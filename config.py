import streamlit as st
import snowflake.connector
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Required Snowflake configuration parameters
REQUIRED_ENV_VARS = [
    "SNOWFLAKE_ACCOUNT",
    "SNOWFLAKE_USER",
    "SNOWFLAKE_PASSWORD",
    "SNOWFLAKE_ROLE",
    "SNOWFLAKE_WAREHOUSE",
    "SNOWFLAKE_DATABASE",
    "SNOWFLAKE_SCHEMA"
]

# Validate environment variables
missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}. "
                    f"Please check your .env file and ensure all required variables are set.")

# Snowflake connection parameters from environment variables
SNOWFLAKE_CONFIG = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "role": os.getenv("SNOWFLAKE_ROLE"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA")
}

def init_connection():
    """Initialize Snowflake connection and store in session state"""
    if 'snowflake_cursor' not in st.session_state:
        try:
            conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
            st.session_state.snowflake_cursor = conn.cursor()
            return conn
        except Exception as e:
            st.error(f"Error connecting to Snowflake: {str(e)}")
            st.info("Please check your .env file and ensure all credentials are correct.")
            return None
    return None

def get_table_data(table_name):
    """Get data from a specific table in Snowflake"""
    try:
        conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
        cur = conn.cursor()
        
        cur.execute(f'SELECT * FROM TOURISM.PUBLIC.{table_name}')
        columns = [desc[0] for desc in cur.description]
        results = cur.fetchall()
        df = pd.DataFrame(results, columns=columns)
        
        cur.close()
        conn.close()
        
        return df
    except Exception as e:
        st.error(f"Error fetching data from {table_name}: {str(e)}")
        return None