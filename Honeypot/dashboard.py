import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Set page config
st.set_page_config(
    page_title="Honeypot Dashboard",
    page_icon="🕷️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    .stMetric {
        background-color: #262730;
        padding: 15px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

def get_attack_data():
    conn = sqlite3.connect('honeypot.db')
    query = '''
        SELECT 
            timestamp,
            source_ip,
            port,
            payload,
            anomaly_score,
            threat_level
        FROM attacks
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def main():
    st.title("🕷️ Honeypot Attack Dashboard")
    
    # Get data
    df = get_attack_data()
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Attacks", len(df))
    
    with col2:
        high_threat = len(df[df['threat_level'] == 'HIGH'])
        st.metric("High Threat Attacks", high_threat)
    
    with col3:
        unique_ips = df['source_ip'].nunique()
        st.metric("Unique Attackers", unique_ips)
    
    with col4:
        avg_anomaly = df['anomaly_score'].mean()
        st.metric("Avg Anomaly Score", f"{avg_anomaly:.2f}")
    
    # Time range selector
    st.subheader("Time Range")
    time_range = st.selectbox(
        "Select time range",
        ["Last 24 hours", "Last 7 days", "Last 30 days", "All time"]
    )
    
    if time_range == "Last 24 hours":
        df = df[df['timestamp'] > datetime.now() - timedelta(days=1)]
    elif time_range == "Last 7 days":
        df = df[df['timestamp'] > datetime.now() - timedelta(days=7)]
    elif time_range == "Last 30 days":
        df = df[df['timestamp'] > datetime.now() - timedelta(days=30)]
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Attack timeline
        st.subheader("Attack Timeline")
        timeline_data = df.set_index('timestamp').resample('H').size().reset_index()
        timeline_data.columns = ['timestamp', 'count']
        
        fig = px.line(timeline_data, x='timestamp', y='count',
                     title='Attack Frequency Over Time')
        fig.update_layout(
            template='plotly_dark',
            xaxis_title="Time",
            yaxis_title="Number of Attacks"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Port distribution
        st.subheader("Attack Distribution by Port")
        port_data = df['port'].value_counts().reset_index()
        port_data.columns = ['port', 'count']
        
        fig = px.pie(port_data, values='count', names='port',
                    title='Attacks by Port')
        fig.update_layout(template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Threat level distribution
        st.subheader("Threat Level Distribution")
        threat_data = df['threat_level'].value_counts().reset_index()
        threat_data.columns = ['threat_level', 'count']
        
        fig = px.bar(threat_data, x='threat_level', y='count',
                    title='Distribution of Threat Levels')
        fig.update_layout(
            template='plotly_dark',
            xaxis_title="Threat Level",
            yaxis_title="Count"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Anomaly score distribution
        st.subheader("Anomaly Score Distribution")
        fig = px.histogram(df, x='anomaly_score',
                          title='Distribution of Anomaly Scores')
        fig.update_layout(
            template='plotly_dark',
            xaxis_title="Anomaly Score",
            yaxis_title="Count"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent attacks table
    st.subheader("Recent Attacks")
    recent_attacks = df.sort_values('timestamp', ascending=False).head(10)
    recent_attacks['timestamp'] = recent_attacks['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    st.dataframe(recent_attacks[['timestamp', 'source_ip', 'port', 'threat_level', 'anomaly_score']])
    
    # Top attackers
    st.subheader("Top Attackers")
    top_attackers = df.groupby('source_ip').agg({
        'timestamp': 'count',
        'anomaly_score': 'mean'
    }).reset_index()
    top_attackers.columns = ['IP Address', 'Attack Count', 'Avg Anomaly Score']
    top_attackers = top_attackers.sort_values('Attack Count', ascending=False).head(10)
    st.dataframe(top_attackers)

if __name__ == "__main__":
    main() 