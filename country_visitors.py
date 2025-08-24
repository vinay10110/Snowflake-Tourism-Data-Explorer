import plotly.express as px
import plotly.graph_objects as go
from config import get_table_data
import streamlit as st
import pandas as pd
def show_country_visitors_analysis():
    """Display country-wise visitors analysis"""
    # Fetch data
    df = get_table_data("COUNTRYWISEYEARLYVISITORS")
    if df is not None:
        # Create visualizations
        create_country_wise_visualizations(df)

def create_country_wise_visualizations(df):
    """Create visualizations for country-wise visitors data"""
    st.title("🌎 Country-wise Visitors Analysis (2014-2020)")
    st.markdown("---")
    
    # Create two columns for layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Line chart showing trends for all countries with enhanced styling
        fig_line = px.line(
            df.melt(id_vars=['COUNTRY'], var_name='Year', value_name='Visitors'),
            x='Year',
            y='Visitors',
            color='COUNTRY',
            title='Tourist Visitor Trends by Country',
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
            yaxis_title_font_size=14,
            showlegend=True
        )
        fig_line.update_traces(line_width=3)
        st.plotly_chart(fig_line, use_container_width=True)

    with col2:
        # Enhanced bar chart comparing total visitors by country
        total_visitors = df.iloc[:, 1:].sum(axis=1)
        fig_bar = px.bar(
            x=df['COUNTRY'],
            y=total_visitors,
            title='Total Visitors by Country',
            labels={'x': 'Country', 'y': 'Total Visitors'},
            template='plotly_white',
            color=total_visitors,
            color_continuous_scale='Viridis'
        )
        fig_bar.update_layout(
            height=500,
            title_x=0.5,
            title_font_size=20,
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            bargap=0.2,
            showlegend=False
        )
        fig_bar.update_traces(
            marker_line_width=1.5,
            marker_line_color='white',
            opacity=0.8
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Create two more columns
    col3, col4 = st.columns(2)

    with col3:
        # Enhanced heatmap for year-over-year growth rate
        years = df.columns[1:].astype(str).tolist()
        growth_data = {}
        
        for country in df['COUNTRY']:
            country_data = df[df['COUNTRY'] == country].iloc[0, 1:].astype(float)
            growth = [(country_data[i] - country_data[i-1])/country_data[i-1] * 100 
                     for i in range(1, len(country_data))]
            growth_data[country] = growth

        growth_df = pd.DataFrame(growth_data, index=years[1:]).T
        fig_heatmap = px.imshow(
            growth_df,
            title='Year-over-Year Growth Rate (%)',
            color_continuous_scale='RdYlBu',
            aspect='auto',
            labels={'x': 'Year', 'y': 'Country'}
        )
        fig_heatmap.update_layout(
            height=500,
            title_x=0.5,
            title_font_size=20,
            coloraxis_colorbar_title='Growth %'
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

    with col4:
        # Enhanced impact analysis visualization
        impact_df = df[['COUNTRY', '_2019', '_2020']].copy()
        impact_df['Decline (%)'] = ((impact_df['_2020'] - impact_df['_2019']) / impact_df['_2019'] * 100).round(1)
        
        fig_impact = px.bar(
            impact_df,
            x='COUNTRY',
            y='Decline (%)',
            title='COVID-19 Impact: Visitor Decline in 2020',
            color='Decline (%)',
            color_continuous_scale='RdBu_r'
        )
        fig_impact.update_layout(
            height=500,
            title_x=0.5,
            title_font_size=20,
            xaxis_title_font_size=14,
            yaxis_title_font_size=14
        )
        fig_impact.update_traces(
            marker_line_width=1.5,
            marker_line_color='white'
        )
        st.plotly_chart(fig_impact, use_container_width=True)

    # Enhanced insights section
    st.markdown("## 📊 Key Insights")
    st.markdown("---")
    
    # Create three columns with equal spacing
    col5, col6, col7 = st.columns(3)
    
    with col5:
        total_2019 = df['_2019'].sum()
        total_2020 = df['_2020'].sum()
        decline = ((total_2020 - total_2019) / total_2019 * 100).round(1)
        st.metric("Overall Tourism Decline in 2020", f"{decline}%", 
                 delta=f"{abs(decline)}% decrease",
                 delta_color="inverse")
        
    with col6:
        max_country = df.loc[df['_2019'].idxmax(), 'COUNTRY']
        max_visitors = df['_2019'].max()
        st.metric("Top Source Market (2019)", 
                 max_country,
                 f"{max_visitors:,.0f} visitors")
        
    with col7:
        avg_growth = growth_df.mean(axis=1)
        fastest_growing = avg_growth.idxmax()
        growth_rate = avg_growth.max().round(1)
        st.metric("Fastest Growing Market",
                 fastest_growing,
                 f"{growth_rate}% avg. growth")