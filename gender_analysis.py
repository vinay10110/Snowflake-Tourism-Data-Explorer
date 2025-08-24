import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import get_table_data

def show_gender_analysis():
    """Display country-wise gender distribution analysis"""
    # Fetch data
    df = get_table_data("COUNTRYWISEGENDER")
    if df is not None:
        # Create visualizations
        create_gender_visualizations(df)

def create_gender_visualizations(df):
    """Create visualizations for gender distribution data"""
    st.title("👥 Country-wise Gender Distribution Analysis (2014-2020)")
    st.markdown("---")
    
    # Create two columns for layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Line chart showing male percentage trends with enhanced styling
        male_cols = [col for col in df.columns if 'MALE' in col]
        female_cols = [col for col in df.columns if 'FEMALE' in col]
        
        # Prepare data for plotting with better formatting
        male_data = pd.melt(df, id_vars=['COUNTRY_OF_NATIONALITY'], value_vars=male_cols, 
                          var_name='Year', value_name='Male Percentage')
        male_data['Year'] = male_data['Year'].apply(lambda x: x.split('_')[1][:4])
        
        fig_line = px.line(
            male_data,
            x='Year',
            y='Male Percentage',
            color='COUNTRY_OF_NATIONALITY',
            title='Male Tourist Percentage Trends by Country',
            template='plotly_white',
            line_shape='spline',
            markers=True
        )
        fig_line.update_layout(
            height=500,
            hovermode='x unified',
            title_x=0.5,
            title_font_size=20,
            legend_title_text='Countries',
            xaxis_title_font_size=14,
            yaxis_title_font_size=14
        )
        fig_line.update_traces(line_width=3)
        st.plotly_chart(fig_line, use_container_width=True)

    with col2:
        # Enhanced stacked bar chart for gender distribution
        latest_year_male = df[['COUNTRY_OF_NATIONALITY', '_2020_MALE']].copy()
        latest_year_female = df[['COUNTRY_OF_NATIONALITY', '_2020_FEMALE']].copy()
        
        fig_stacked = go.Figure()
        fig_stacked.add_trace(go.Bar(
            name='Male',
            x=df['COUNTRY_OF_NATIONALITY'],
            y=df['_2020_MALE'],
            marker_color='#2E86C1'
        ))
        fig_stacked.add_trace(go.Bar(
            name='Female',
            x=df['COUNTRY_OF_NATIONALITY'],
            y=df['_2020_FEMALE'],
            marker_color='#D35400'
        ))
        
        fig_stacked.update_layout(
            barmode='stack',
            title={
                'text': 'Gender Distribution by Country (2020)',
                'x': 0.5,
                'font_size': 20
            },
            height=500,
            template='plotly_white',
            xaxis_title='Country',
            yaxis_title='Percentage',
            legend_title_text='Gender',
            bargap=0.3
        )
        st.plotly_chart(fig_stacked, use_container_width=True)

    # Create two more columns
    col3, col4 = st.columns(2)

    with col3:
        # Enhanced gender gap evolution heatmap
        gender_gap = pd.DataFrame()
        for year in range(2014, 2021):
            male_col = f'_{year}_MALE'
            female_col = f'_{year}_FEMALE'
            gender_gap[str(year)] = df[male_col] - df[female_col]
        gender_gap.index = df['COUNTRY_OF_NATIONALITY']
        
        fig_heatmap = px.imshow(
            gender_gap.T,
            title='Gender Gap Evolution (Male% - Female%)',
            color_continuous_scale='RdBu',
            aspect='auto',
            labels={'x': 'Country', 'y': 'Year'}
        )
        fig_heatmap.update_layout(
            height=500,
            title_x=0.5,
            title_font_size=20,
            coloraxis_colorbar_title='Gap %'
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

    with col4:
        # Enhanced pie chart with country selector
        selected_country = st.selectbox(
            "📍 Select Country for Gender Distribution",
            df['COUNTRY_OF_NATIONALITY'].tolist()
        )
        
        country_data = df[df['COUNTRY_OF_NATIONALITY'] == selected_country]
        gender_values = [
            country_data['_2020_MALE'].iloc[0],
            country_data['_2020_FEMALE'].iloc[0]
        ]
        
        fig_pie = px.pie(
            values=gender_values,
            names=['Male', 'Female'],
            title=f'Gender Distribution in {selected_country} (2020)',
            color_discrete_sequence=['#2E86C1', '#D35400'],
            hole=0.4
        )
        fig_pie.update_layout(
            height=500,
            title_x=0.5,
            title_font_size=20,
            showlegend=True
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Enhanced insights section
    st.markdown("## 📊 Key Insights")
    st.markdown("---")
    col5, col6, col7 = st.columns(3)
    
    with col5:
        avg_male_2020 = df['_2020_MALE'].mean()
        avg_female_2020 = df['_2020_FEMALE'].mean()
        st.metric(
            "Gender Distribution (2020)", 
            f"M: {avg_male_2020:.1f}% | F: {avg_female_2020:.1f}%",
            f"Gap: {(avg_male_2020 - avg_female_2020):.1f}%"
        )
        
    with col6:
        most_balanced = df.loc[abs(df['_2020_MALE'] - 50).idxmin(), 'COUNTRY_OF_NATIONALITY']
        balance_value = df.loc[abs(df['_2020_MALE'] - 50).idxmin(), '_2020_MALE']
        st.metric(
            "Most Gender Balanced Country", 
            most_balanced,
            f"M: {balance_value:.1f}% | F: {(100-balance_value):.1f}%"
        )
        
    with col7:
        largest_gap_idx = abs(df['_2020_MALE'] - df['_2020_FEMALE']).idxmax()
        largest_gap_country = df.loc[largest_gap_idx, 'COUNTRY_OF_NATIONALITY']
        gap_size = abs(df.loc[largest_gap_idx, '_2020_MALE'] - df.loc[largest_gap_idx, '_2020_FEMALE'])
        st.metric(
            "Largest Gender Gap", 
            largest_gap_country,
            f"{gap_size:.1f}% difference"
        )