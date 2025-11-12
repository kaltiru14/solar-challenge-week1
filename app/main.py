# app/main.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Add the current directory to Python path so we can import utils
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Now import from utils directly
from utils import (
    load_solar_data, create_solar_boxplot, get_top_regions_table, 
    check_data_files, get_available_metrics
)

# Page configuration
st.set_page_config(
    page_title="Solar Potential Dashboard",
    page_icon="☀️",
    layout="wide"
)

def main():
    st.title("🌍 West Africa Solar Potential Dashboard")
    
    st.markdown("Compare solar energy potential across different countries.")
    
    # Run data file check
    check_data_files()
    
    # Sidebar with widgets
    st.sidebar.header("Dashboard Controls")
    
    # Country selection widget
    available_countries = ['Benin', 'Togo', 'Sierra Leone']
    selected_countries = st.sidebar.multiselect(
        "Select Countries:",
        available_countries,
        default=available_countries
    )
    
    # Load data first to see available metrics
    df = pd.DataFrame()
    if selected_countries:
        df = load_solar_data(selected_countries)
    
    # Metric selection widget (dynamic based on loaded data)
    if not df.empty:
        available_metrics = get_available_metrics(df)
        if available_metrics:
            selected_metric = st.sidebar.selectbox(
                "Select Solar Metric:",
                available_metrics
            )
        else:
            st.sidebar.warning("No solar metrics found in data")
            selected_metric = None
    else:
        selected_metric = None
        st.sidebar.info("Select countries to see available metrics")
    
    # Display data info
    if not df.empty:
        st.success(f"✅ Loaded {len(df):,} records from {df['Country'].nunique()} countries")
        
        # Show available columns for debugging
        with st.expander("🔍 Data Columns Info"):
            st.write("Available columns:", list(df.columns))
            st.write("Data types:", df.dtypes.to_dict())
        
        # Boxplot section
        if selected_metric:
            st.header("📊 Solar Metric Distribution")
            boxplot_fig = create_solar_boxplot(df, selected_metric)
            if boxplot_fig:
                st.plotly_chart(boxplot_fig, use_container_width=True)
            else:
                st.warning(f"Could not create boxplot for {selected_metric}")
            
            # Top regions table section
            st.header("🏆 Country Performance Ranking")
            rankings_df = get_top_regions_table(df, selected_metric)
            if not rankings_df.empty:
                # Style the table
                styled_df = rankings_df.style.background_gradient(
                    subset=['Average'], 
                    cmap='Blues'
                ).format({
                    'Average': '{:.1f}',
                    'Median': '{:.1f}',
                    'Std_Dev': '{:.1f}',
                    'Min': '{:.1f}',
                    'Max': '{:.1f}'
                })
                st.dataframe(styled_df, use_container_width=True)
                
                # Display top country
                top_country = rankings_df.iloc[0]['Country']
                top_value = rankings_df.iloc[0]['Average']
                st.info(f"**🏆 Top Performer**: {top_country} with average {selected_metric} of {top_value} W/m²")
            else:
                st.warning("No ranking data available.")
            
            # Data summary
            st.header("📈 Data Summary")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Records", f"{len(df):,}")
            with col2:
                st.metric("Countries", df['Country'].nunique())
            with col3:
                st.metric(f"Avg {selected_metric}", f"{df[selected_metric].mean():.1f}")
            with col4:
                st.metric(f"Max {selected_metric}", f"{df[selected_metric].max():.1f}")
        
        # Raw data preview
        with st.expander("📋 Raw Data Preview"):
            st.dataframe(df.head(100))
            
            # Show country distribution
            st.write("**Records per country:**")
            country_counts = df['Country'].value_counts()
            st.write(country_counts)
    
    elif selected_countries:
        st.error("""
        ❌ No data loaded even though countries were selected. 
        
        Possible issues:
        - Data files exist but can't be read
        - CSV files have formatting issues
        - Memory limitations
        """)

if __name__ == "__main__":
    main()