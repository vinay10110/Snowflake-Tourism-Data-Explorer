import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import get_table_data

def show_top_places_analysis():
    """Display top places to visit analysis"""
    # Fetch data
    df = get_table_data("TOPPLACESTOVISIT")
    if df is not None:
        # Create visualizations
        create_top_places_visualizations(df)

def create_top_places_visualizations(df):
    """Create visualizations for top places data"""
    st.title("🏆 India's Top-Rated Tourist Attractions")
    st.markdown("---")
    
    # Convert numeric columns to proper data types
    df['GOOGLE_REVIEW_RATING'] = pd.to_numeric(df['GOOGLE_REVIEW_RATING'], errors='coerce')
    df['NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS'] = pd.to_numeric(df['NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS'], errors='coerce')
    df['ENTRANCE_FEE_IN_INR'] = pd.to_numeric(df['ENTRANCE_FEE_IN_INR'], errors='coerce')
    df['TIME_NEEDED_TO_VISIT_IN_HRS'] = pd.to_numeric(df['TIME_NEEDED_TO_VISIT_IN_HRS'], errors='coerce')
    
    # Create a ranking summary at the top
    st.subheader("🎖️ Top 5 Most Popular Places")
    
    # Calculate rankings based on different metrics with proper numeric types
    df['popularity_score'] = df['GOOGLE_REVIEW_RATING'] * df['NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS']
    top_places = df.nlargest(5, 'popularity_score')
    
    # Display top 5 places in an enhanced format
    for idx, place in top_places.iterrows():
        col1, col2, col3 = st.columns([0.4, 0.3, 0.3])
        with col1:
            st.markdown(f"**{place['NAME']}**")
        with col2:
            st.markdown(f"⭐ {place['GOOGLE_REVIEW_RATING']:.1f}/5")
        with col3:
            st.markdown(f"👥 {place['NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS']:.1f}L reviews")
    
    st.markdown("---")
    
    # Create four columns for different rankings
    col1, col2 = st.columns(2)
    
    with col1:
        # Enhanced Rating Distribution
        fig_rating = px.histogram(
            df[df['GOOGLE_REVIEW_RATING'].notna()],
            x='GOOGLE_REVIEW_RATING',
            title='Rating Distribution of Tourist Places',
            template='plotly_white',
            nbins=20,
            color_discrete_sequence=['#3498db']
        )
        fig_rating.update_layout(
            height=400,
            title_x=0.5,
            title_font_size=20,
            showlegend=False,
            xaxis_title='Rating ⭐',
            yaxis_title='Number of Places',
            bargap=0.1
        )
        st.plotly_chart(fig_rating, use_container_width=True)

    with col2:
        # Price vs Rating Analysis
        fig_scatter = px.scatter(
            df[df['ENTRANCE_FEE_IN_INR'].notna() & df['GOOGLE_REVIEW_RATING'].notna()],
            x='ENTRANCE_FEE_IN_INR',
            y='GOOGLE_REVIEW_RATING',
            color='TYPE',
            size='NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS',
            hover_data=['NAME', 'CITY'],
            title='Price vs Rating Analysis',
            template='plotly_white',
            labels={
                'ENTRANCE_FEE_IN_INR': 'Entrance Fee (₹)',
                'GOOGLE_REVIEW_RATING': 'Rating',
                'TYPE': 'Place Type'
            }
        )
        fig_scatter.update_layout(
            height=400,
            title_x=0.5,
            title_font_size=20,
            showlegend=True
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Create two more columns
    col3, col4 = st.columns(2)
    
    with col3:
        # Top Places by Type
        type_avg_rating = df.groupby('TYPE').agg({
            'GOOGLE_REVIEW_RATING': 'mean',
            'NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS': 'sum'
        }).reset_index()
        
        fig_bubble = px.scatter(
            type_avg_rating,
            x='GOOGLE_REVIEW_RATING',
            y='NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS',
            size='NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS',
            color='TYPE',
            title='Place Types: Rating vs Popularity',
            template='plotly_white',
            labels={
                'GOOGLE_REVIEW_RATING': 'Average Rating',
                'NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS': 'Total Reviews (Lakhs)',
                'TYPE': 'Place Type'
            }
        )
        fig_bubble.update_layout(
            height=400,
            title_x=0.5,
            title_font_size=20
        )
        st.plotly_chart(fig_bubble, use_container_width=True)
        
    with col4:
        # Visit Duration vs Popularity
        fig_duration = px.scatter(
            df[df['TIME_NEEDED_TO_VISIT_IN_HRS'].notna()],
            x='TIME_NEEDED_TO_VISIT_IN_HRS',
            y='NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS',
            color='GOOGLE_REVIEW_RATING',
            size='NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS',
            hover_data=['NAME', 'TYPE'],
            title='Visit Duration vs Popularity',
            template='plotly_white',
            labels={
                'TIME_NEEDED_TO_VISIT_IN_HRS': 'Time Needed (Hours)',
                'NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS': 'Number of Reviews (Lakhs)',
                'GOOGLE_REVIEW_RATING': 'Rating'
            }
        )
        fig_duration.update_layout(
            height=400,
            title_x=0.5,
            title_font_size=20,
            coloraxis_colorbar_title='Rating'
        )
        st.plotly_chart(fig_duration, use_container_width=True)

    # Rankings Section
    st.markdown("## 🏅 Rankings & Analytics")
    st.markdown("---")
    
    col5, col6, col7 = st.columns(3)
    
    with col5:
        # Ensure we don't divide by zero
        df['value_score'] = df['ENTRANCE_FEE_IN_INR'].div(df['GOOGLE_REVIEW_RATING'].replace(0, float('nan')))
        best_value = df.loc[df['value_score'].idxmin()]
        st.metric(
            "Best Value for Money 💰",
            best_value['NAME'],
            f"₹{best_value['ENTRANCE_FEE_IN_INR']:.0f} | ⭐{best_value['GOOGLE_REVIEW_RATING']:.1f}"
        )
        
    with col6:
        highest_rated_type = type_avg_rating.loc[type_avg_rating['GOOGLE_REVIEW_RATING'].idxmax()]
        st.metric(
            "Most Popular Category 🌟",
            highest_rated_type['TYPE'],
            f"⭐ {highest_rated_type['GOOGLE_REVIEW_RATING']:.2f} avg rating"
        )
        
    with col7:
        df['time_efficiency'] = df['NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS'].div(df['TIME_NEEDED_TO_VISIT_IN_HRS'].replace(0, float('nan')))
        most_time_efficient = df.loc[df['time_efficiency'].idxmax()]
        st.metric(
            "Most Time-Efficient Visit ⏱️",
            most_time_efficient['NAME'],
            f"{most_time_efficient['TIME_NEEDED_TO_VISIT_IN_HRS']:.1f} hrs | {most_time_efficient['NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS']:.1f}L reviews"
        )