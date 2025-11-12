# app/utils.py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict
import os
import streamlit as st

def check_data_files():
    """Check which data files actually exist"""
    st.sidebar.header("🔍 Data File Check")
    
    expected_files = {
        'Benin': 'data/benin_clean.csv',
        'Togo': 'data/togo_clean.csv', 
        'Sierra Leone': 'data/sierraleone_clean.csv'
    }
    
    for country, file_path in expected_files.items():
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path) / (1024*1024)  # Size in MB
            st.sidebar.success(f"✅ {country}: {file_path} ({file_size:.1f} MB)")
        else:
            st.sidebar.error(f"❌ {country}: {file_path} - NOT FOUND")
    
    # List all files in data folder
    if os.path.exists('data'):
        st.sidebar.info("📁 All files in data folder:")
        for file in sorted(os.listdir('data')):
            if file.endswith('.csv'):
                file_path = os.path.join('data', file)
                file_size = os.path.getsize(file_path) / (1024*1024)
                st.sidebar.write(f"   📄 {file} ({file_size:.1f} MB)")

def find_data_file(country: str):
    """Find the correct data file for a country (case-insensitive on Windows)"""
    data_dir = 'data'
    if not os.path.exists(data_dir):
        return None
    
    # Map country names to possible file patterns
    file_patterns = {
        'Benin': ['benin_clean.csv', 'benin_clean.CSV', 'benin-malanville.csv'],
        'Togo': ['togo_clean.csv', 'togo_clean.CSV', 'togo-dapaong_qc.csv'],
        'Sierra Leone': ['sierraleone_clean.csv', 'sierraleone_clean.CSV', 'sierraleone-bumbuna.csv']
    }
    
    if country not in file_patterns:
        return None
    
    # Check each possible file pattern
    for pattern in file_patterns[country]:
        file_path = os.path.join(data_dir, pattern)
        if os.path.exists(file_path):
            return file_path
    
    # If exact match not found, try case-insensitive search (for Windows)
    for file in os.listdir(data_dir):
        if file.lower() in [p.lower() for p in file_patterns[country]]:
            return os.path.join(data_dir, file)
    
    return None

def load_solar_data(selected_countries: List[str]) -> pd.DataFrame:
    """
    Load solar data for selected countries from local CSV files
    """
    data_frames = []
    
    for country in selected_countries:
        file_path = find_data_file(country)
        
        if file_path and os.path.exists(file_path):
            try:
                # Show loading progress
                with st.sidebar.expander(f"Loading {country}..."):
                    st.sidebar.write(f"File: {os.path.basename(file_path)}")
                    
                    # Read the CSV file
                    df = pd.read_csv(file_path)
                    
                    # Add country identifier
                    df['Country'] = country
                    data_frames.append(df)
                    
                    st.sidebar.success(f"✅ {country}: {len(df):,} records")
                    
            except Exception as e:
                st.sidebar.error(f"❌ Error loading {country}: {str(e)}")
        else:
            st.sidebar.error(f"❌ Could not find data file for {country}")
    
    if data_frames:
        combined_df = pd.concat(data_frames, ignore_index=True)
        st.sidebar.success(f"📊 Combined data: {len(combined_df):,} records from {len(data_frames)} countries")
        return combined_df
    else:
        st.sidebar.error("❌ No data files could be loaded")
        return pd.DataFrame()

def create_solar_boxplot(df: pd.DataFrame, metric: str) -> go.Figure:
    """
    Create an interactive boxplot for solar metrics
    """
    if df.empty or metric not in df.columns:
        return None
    
    fig = px.box(
        df, 
        x='Country', 
        y=metric,
        title=f'{metric} Distribution by Country',
        color='Country',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(
        xaxis_title="Country",
        yaxis_title=f"{metric} (W/m²)",
        showlegend=False,
        height=500
    )
    
    return fig

def get_top_regions_table(df: pd.DataFrame, metric: str = 'GHI') -> pd.DataFrame:
    """
    Generate a table ranking countries by solar metric performance
    """
    if df.empty or metric not in df.columns:
        return pd.DataFrame()
    
    summary = df.groupby('Country')[metric].agg([
        ('Average', 'mean'),
        ('Median', 'median'),
        ('Std_Dev', 'std'),
        ('Min', 'min'),
        ('Max', 'max'),
        ('Count', 'count')
    ]).round(2)
    
    summary = summary.sort_values('Average', ascending=False)
    return summary.reset_index()

def get_available_metrics(df: pd.DataFrame) -> List[str]:
    """
    Get list of available solar metrics in the data
    """
    solar_metrics = ['GHI', 'DNI', 'DHI', 'Tamb', 'WS', 'WSgust', 'WD', 'RH', 'BP']
    return [metric for metric in solar_metrics if metric in df.columns]