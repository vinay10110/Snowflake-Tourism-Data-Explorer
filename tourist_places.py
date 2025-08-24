import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import get_table_data

def show_tourist_places_analysis():
    """Display India's famous tourist places analysis"""
    # Fetch data
    df = get_table_data("INDIAFAMOUSTOURISTPLACES")
    if df is not None:
        # Create visualizations
        create_tourist_places_visualizations(df)

def create_tourist_places_visualizations(df):
    """Create visualizations for tourist places data"""
    st.title("🗺️ India's Famous Tourist Places Analysis")
    st.markdown("---")
    
    # Interactive Place Selector with Enhanced Layout
    st.subheader("🔍 Explore Tourist Destinations")
    
    # Add a search filter with better styling
    search_term = st.text_input("🔎 Search Places", "", help="Type to filter places by name")
    filtered_df = df[df['NAME'].str.contains(search_term, case=False)] if search_term else df
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_place = st.selectbox(
            "Select a Tourist Place",
            filtered_df['NAME'].tolist()
        )
        
        place_data = df[df['NAME'] == selected_place].iloc[0]
        
        # Enhanced place details display with cards
        st.markdown("""
        <style>
        .info-card {
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            background-color: #f0f2f6;
        }
        </style>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown("### 📌 Location Details")
            st.write(f"🌍 **Zone:** {place_data['ZONE']}")
            st.write(f"📍 **State:** {place_data['STATE']}")
            st.write(f"🏙️ **City:** {place_data['CITY']}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown("### ℹ️ Visit Information")
            st.write(f"⏱️ **Time needed:** {place_data['TIME_NEEDED_TO_VISIT_IN_HRS']} hours")
            st.write(f"💰 **Entrance Fee:** ₹{place_data['ENTRANCE_FEE_IN_INR']:,}")
            st.write(f"⭐ **Rating:** {place_data['GOOGLE_REVIEW_RATING']}/5")
            st.write(f"📸 **DSLR Allowed:** {place_data['DSLR_ALLOWED']}")
            st.write(f"🕒 **Best Time:** {place_data['BEST_TIME_TO_VISIT']}")
            st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        # Enhanced image display with better styling
        if not pd.isna(place_data['IMAGE_URL']):
            st.markdown("""
            <style>
            .img-container {
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            </style>
            """, unsafe_allow_html=True)
            st.markdown('<div class="img-container">', unsafe_allow_html=True)
            st.image(place_data['IMAGE_URL'], caption=selected_place, use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Create two columns for visualizations
    col3, col4 = st.columns(2)
    
    with col3:
        # Enhanced Rating vs Visit Time scatter plot
        df['NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS'] = pd.to_numeric(df['NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS'], errors='coerce')
        
        fig_scatter = px.scatter(
            df,
            x='GOOGLE_REVIEW_RATING',
            y='TIME_NEEDED_TO_VISIT_IN_HRS',
            color='ZONE',
            size='NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS',
            hover_data=['NAME', 'CITY', 'STATE'],
            title='Tourist Places: Rating vs Visit Duration',
            template='plotly_white',
            labels={
                'GOOGLE_REVIEW_RATING': 'Google Rating ⭐',
                'TIME_NEEDED_TO_VISIT_IN_HRS': 'Visit Duration (hours) ⏱️',
                'NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS': 'Reviews (lakhs) 👥',
                'ZONE': 'Zone 🗺️'
            }
        )
        fig_scatter.update_layout(
            height=500,
            title_x=0.5,
            title_font_size=20,
            showlegend=True,
            legend_title_text='Zone 🗺️',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig_scatter.update_traces(
            marker=dict(line=dict(width=1, color='white')),
            opacity=0.7
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with col4:
        # Enhanced Type distribution by Zone
        type_zone_count = df.groupby(['ZONE', 'TYPE']).size().reset_index(name='count')
        fig_bar = px.bar(
            type_zone_count,
            x='ZONE',
            y='count',
            color='TYPE',
            title='Types of Tourist Places by Zone 🏛️',
            template='plotly_white',
            labels={
                'count': 'Number of Places',
                'ZONE': 'Zone',
                'TYPE': 'Place Type'
            },
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_bar.update_layout(
            height=500,
            title_x=0.5,
            title_font_size=20,
            showlegend=True,
            legend_title_text='Place Type',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            bargap=0.2
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Create two more columns
    col5, col6 = st.columns(2)
    
    with col5:
        # Enhanced Entry Fee Analysis with ranges
        df['Fee_Range'] = pd.cut(
            df['ENTRANCE_FEE_IN_INR'],
            bins=[-1, 0, 100, 500, float('inf')],
            labels=['Free', '₹1-100', '₹101-500', '₹500+']
        )
        fee_dist = df['Fee_Range'].value_counts()
        
        fig_pie = px.pie(
            values=fee_dist.values,
            names=fee_dist.index,
            title='Entry Fee Distribution 💰',
            hole=0.6,
            template='plotly_white',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig_pie.update_layout(
            height=500,
            title_x=0.5,
            title_font_size=20,
            showlegend=True,
            legend_title_text='Fee Range'
        )
        fig_pie.update_traces(
            textposition='outside',
            textinfo='percent+label',
            pull=[0.05] * len(fee_dist)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col6:
        # Enhanced Best Time Analysis
        visit_time_dist = df['BEST_TIME_TO_VISIT'].value_counts()
        fig_donut = px.pie(
            values=visit_time_dist.values,
            names=visit_time_dist.index,
            title='Best Time to Visit Distribution 🕒',
            hole=0.6,
            template='plotly_white',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_donut.update_layout(
            height=500,
            title_x=0.5,
            title_font_size=20,
            showlegend=True,
            legend_title_text='Time of Day'
        )
        fig_donut.update_traces(
            textposition='outside',
            textinfo='percent+label',
            pull=[0.05] * len(visit_time_dist)
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    
    # Enhanced insights section with better styling
    st.markdown("## 📊 Key Insights")
    st.markdown("---")
    
    col7, col8, col9 = st.columns(3)
    
    with col7:
        avg_rating = df['GOOGLE_REVIEW_RATING'].mean()
        total_reviews = df['NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS'].sum()
        st.metric(
            "Average Rating ⭐",
            f"{avg_rating:.1f}/5",
            f"Based on {total_reviews:.1f} lakh reviews"
        )
        
    with col8:
        top_rated = df.loc[df['GOOGLE_REVIEW_RATING'].idxmax()]
        st.metric(
            "Highest Rated Place 🏆",
            top_rated['NAME'],
            f"{top_rated['GOOGLE_REVIEW_RATING']}⭐ - {top_rated['CITY']}"
        )
        
    with col9:
        most_reviewed = df.loc[df['NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS'].idxmax()]
        st.metric(
            "Most Popular Place 🌟",
            most_reviewed['NAME'],
            f"{most_reviewed['NUMBER_OF_GOOGLE_REVIEW_IN_LAKHS']:.1f} lakh reviews"
        )