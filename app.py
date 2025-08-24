import streamlit as st
import pandas as pd
from config import init_connection
from country_visitors import show_country_visitors_analysis
from gender_analysis import show_gender_analysis
from tourist_places import show_tourist_places_analysis
from top_places import show_top_places_analysis

# Set page configuration
st.set_page_config(page_title="Snowflake Tourism Data Explorer", layout="wide")

# Initialize Snowflake connection when app starts
init_connection()

# Add title
st.title("Snowflake Tourism Database Explorer")

# Create sidebar for navigation
st.sidebar.header("📊 Navigation Menu")
selected_table = st.sidebar.radio(
    "Choose what to explore:",
    options=["COUNTRYWISEYEARLYVISITORS", "COUNTRYWISEGENDER", "INDIA_FAMOUS_TOURIST_PLACES", "TOPPLACESTOVISIT"],
    format_func=lambda x: {
        "COUNTRYWISEYEARLYVISITORS": "🌍 International Visitors Trend",
        "COUNTRYWISEGENDER": "👥 Gender Distribution Analysis",
        "INDIA_FAMOUS_TOURIST_PLACES": "🗺️ Famous Tourist Destinations",
        "TOPPLACESTOVISIT": "⭐ Top-Rated Places"
    }[x]
)

# Display the selected data analysis
if selected_table == "COUNTRYWISEYEARLYVISITORS":
    show_country_visitors_analysis()
elif selected_table == "COUNTRYWISEGENDER":
    show_gender_analysis()
elif selected_table == "INDIA_FAMOUS_TOURIST_PLACES":
    show_tourist_places_analysis()
else:  # "TOPPLACESTOVISIT"
    show_top_places_analysis()