import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from cassandra.cluster import Cluster
from PIL import Image
import time
import subprocess
import os
import datetime

# Page Configuration
st.set_page_config(
    page_title="Real-Time User Data Pipeline",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS from the reference app
st.markdown("""
<style>
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: white;
    }
    
    /* Headers with glow effect */
    h1, h2, h3, h4 { 
        color: #00d4ff !important;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        color: #00ff88 !important;
        font-weight: 700 !important;
        text-shadow: 0 0 15px rgba(0, 255, 136, 0.4);
    }
    
    [data-testid="stMetricLabel"] { 
        color: #e0e0e0 !important;
        font-size: 1rem !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
        border-right: 1px solid rgba(0, 212, 255, 0.2);
    }
    
    /* Card styling */
    .info-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .metric-card {
        background: linear-gradient(145deg, rgba(0, 212, 255, 0.1), rgba(0, 255, 136, 0.05));
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(0, 212, 255, 0.3);
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Flow Diagram Box */
    .flow-box {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 20px 30px; 
        border-radius: 15px; 
        min-width: 150px;
        text-align: center;
        color: white;
    }
    
    /* Live Dot Animation */
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.1); }
        100% { opacity: 1; transform: scale(1); }
    }
    .live-dot {
        display: inline-block;
        width: 12px;
        height: 12px;
        background: #00ff88;
        border-radius: 50%;
        margin-right: 10px;
        animation: pulse 1.5s infinite;
        box-shadow: 0 0 10px #00ff88;
    }

    /* DataFrame styling */
    div[data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ FUNCTIONS ------------------

def get_cassandra_session():
    try:
        cluster = Cluster(['localhost'], port=9042)
        session = cluster.connect()
        return session
    except Exception as e:
        return None

def get_data(session):
    try:
        # Fetch total count
        count_row = session.execute("SELECT count(*) FROM spark_streams.created_users").one()
        count = count_row[0]
        
        # Fetch recent data for table
        rows = session.execute("SELECT * FROM spark_streams.created_users LIMIT 100")
        df = pd.DataFrame(list(rows))
        return count, df
    except Exception as e:
        return 0, pd.DataFrame()

def get_docker_logs(container_name, lines=50):
    try:
        result = subprocess.run(
            ["docker", "logs", "--tail", str(lines), container_name],
            capture_output=True, text=True, encoding='utf-8', errors='ignore'
        )
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error fetching logs: {e}"

# ------------------ SIDEBAR ------------------

with st.sidebar:
    st.image("https://airflow.apache.org/images/feature-image.png", use_container_width=True)
    st.markdown("## 🎛️ Pipeline Control")
    st.markdown("---")
    
    # Connection Status
    session = get_cassandra_session()
    if session:
        st.markdown('<div class="metric-card"><span class="live-dot"></span><strong>SYSTEM ONLINE</strong><br><small>Connected to Cassandra</small></div>', unsafe_allow_html=True)
    else:
        st.error("🔴 System Offline: Check Containers")
    
    st.markdown("### 🔄 Auto-Refresh")
    auto_refresh = st.toggle("Enable Live Updates", value=False)
    if auto_refresh:
        refresh_rate = st.slider("Interval (seconds)", 1, 10, 2)
    
    st.markdown("---")
    st.markdown("### 🛠️ Tech Stack Analysis")
    st.info("""
    **Airflow**: Orchestration
    **Kafka**: Streaming
    **Spark**: Processing
    **Cassandra**: NoSQL DB
    **Docker**: Containerization
    """)

# ------------------ MAIN LAYOUT ------------------

st.markdown("""
<div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
    <div style="background: linear-gradient(45deg, #FF512F, #DD2476); padding: 10px 20px; border-radius: 25px; color: white; font-weight: bold; box-shadow: 0 4px 15px rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.2);">
        Ratnesh Singh | Data Scientist (4+ Year Exp)
    </div>
</div>
<div style="text-align: center; margin-bottom: 30px;">
    <h1>⚡ Real-Time User Data Pipeline</h1>
    <p style="font-size: 1.2rem; color: #aaa;">End-to-End Data Engineering</p>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Project Demo (Live)", 
    "ℹ️ About the Project ", 
    "🏗️ Architecture & Tech Stack", 
    "📜 System Logs"
])

# ==================== TAB 1: PROJECT DEMO ====================
with tab1:
    if session:
        # Fetch more data for better analysis
        # OPTIMIZED: Select ONLY necessary columns to avoid MessageSizeError (skipping 'picture' which is heavy)
        try:
            query = "SELECT username, first_name, gender, email, registered_date FROM spark_streams.created_users LIMIT 2000"
            rows = session.execute(query)
            df = pd.DataFrame(list(rows))
            count = len(df) 
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            count = 0
            df = pd.DataFrame()

        # Get total count separately for accuracy
        try:
            count_row = session.execute("SELECT count(*) FROM spark_streams.created_users").one()
            total_count = count_row[0]
        except:
            total_count = count

        # --- Top Metrics ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records Processed", f"{total_count:,}", delta="Live")
        with col2:
            last_user = df.iloc[0]['username'] if not df.empty else "N/A"
            st.metric("Latest User", last_user)
        with col3:
            # Simple throughput estimate (records in last minute if we had timestamps, otherwise placeholder)
            st.metric("System Status", "🟢 Active", delta="Streaming")

        st.markdown("---")

        # --- Visualizations ---
        if not df.empty:
            # Data Preprocessing
            if 'registered_date' in df.columns:
                df['registered_date'] = pd.to_datetime(df['registered_date'])
            
            if 'email' in df.columns:
                df['email_domain'] = df['email'].apply(lambda x: x.split('@')[-1] if isinstance(x, str) else "Unknown")

            # Row 1: Charts
            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown("### 🌍 Gender Distribution")
                if 'gender' in df.columns:
                    gender_counts = df['gender'].value_counts().reset_index()
                    gender_counts.columns = ['gender', 'count']
                    fig = px.pie(gender_counts, values='count', names='gender', 
                                 color_discrete_sequence=['#00d4ff', '#00ff88', '#ff6b6b'],
                                 hole=0.4)
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                                      font_color='white', margin=dict(t=0, b=0, l=0, r=0))
                    st.plotly_chart(fig, use_container_width=True)
            
            with c2:
                st.markdown("### 📧 Top Email Providers")
                if 'email_domain' in df.columns:
                    email_counts = df['email_domain'].value_counts().head(5).reset_index()
                    email_counts.columns = ['domain', 'count']
                    fig = px.bar(email_counts, x='domain', y='count', color='count',
                                 color_continuous_scale=['#00d4ff', '#00ff88'])
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                                      font_color='white', margin=dict(t=0, b=0, l=0, r=0),
                                      xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'))
                    st.plotly_chart(fig, use_container_width=True)

            # Row 2: Timeline & Table
            st.markdown("---")
            
            if 'registered_date' in df.columns:
                st.markdown("### 📈 User Registration Timeline (By Year)")
                
                # OPTIMIZED: Group by Year to avoid creating millions of points for 20-year spans
                df['year'] = df['registered_date'].dt.year
                df_trend = df.groupby('year').size().reset_index(name='count')
                
                fig = px.area(df_trend, x='year', y='count', 
                              markers=True, line_shape='spline')
                fig.update_traces(line_color='#00d4ff', fillcolor='rgba(0, 212, 255, 0.2)')
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                                  font_color='white', hovermode="x unified",
                                  xaxis=dict(showgrid=False, title='Year'), 
                                  yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title='Registrations'))
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("### 📋 Latest Registrations Table")
            cols_to_show = ['username', 'first_name', 'gender', 'email', 'registered_date']
            valid_cols = [c for c in cols_to_show if c in df.columns]
            st.dataframe(df[valid_cols].head(20), hide_index=True, use_container_width=True)

        else:
            st.warning("Waiting for data stream... Please start the Airflow DAG.")

# ==================== TAB 2: ABOUT THE PROJECT ====================
with tab2:
    st.markdown("## 📚 Comprehensive Project Documentation")
    st.markdown("*A complete guide to understanding this project - written for everyone!*")
    st.markdown("---")
    
    # Simple Introduction
    st.markdown("### 📚 What is This Project?")
    st.markdown("""
    <div class="info-card">
        <p style="font-size: 1.1rem; line-height: 1.8;">
            In the modern data landscape, handling real-time data efficiently is crucial. Traditional batch processing 
            methods often fail to provide insights instantly. This project addresses the challenge of building a 
            <strong>scalable, fault-tolerant, and real-time data engineering pipeline</strong> that can ingest, process, and store 
            user data instantaneously.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    # Real World Analogy
    st.markdown("### 🍕 Understanding With a Pizza Shop Analogy")
    
    col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1, 2, 1, 2, 1, 2])
    with col1:
        st.info("**👨‍🍳 Pizza Orders**\n\n(API Source)\nCustomers placing orders.")
    with col2:
        st.markdown("<h2 style='text-align: center'>➜</h2>", unsafe_allow_html=True)
    with col3:
        st.warning("**📨 Waiter/Ticket**\n\n(Kafka)\nTakes order, holds in queue.")
    with col4:
        st.markdown("<h2 style='text-align: center'>➜</h2>", unsafe_allow_html=True)
    with col5:
        st.error("**🔥 Kitchen**\n\n(Spark)\nCooks/Processes the pizza.")
    with col6:
        st.markdown("<h2 style='text-align: center'>➜</h2>", unsafe_allow_html=True)
    with col7:
        st.success("**🍽️ Table**\n\n(Cassandra)\nServed ready to eat.")
    
    st.markdown("---")
    
    # Project Agenda
    st.markdown("### � Project Agenda")
    
    agenda_steps = [
        {"title": "Ingestion", "icon": "�", "tool": "API", "desc": "Fetch user data from an external API (randomuser.me)."},
        {"title": "Orchestration", "icon": "🌪️", "tool": "Airflow", "desc": "Schedule and manage the ingestion process using Apache Airflow."},
        {"title": "Streaming", "icon": "📨", "tool": "Kafka", "desc": "Push the ingested data to a message broker to decouple systems."},
        {"title": "Processing", "icon": "⚡", "tool": "Spark", "desc": "Consume data from Kafka using Structured Streaming for transformation."},
        {"title": "Storage", "icon": "💾", "tool": "Cassandra", "desc": "Persist the processed data into a high-performance NoSQL database."},
        {"title": "Containerization", "icon": "�", "tool": "Docker", "desc": "Encapsulate the entire stack in Docker for easy deployment."}
    ]
    
    for i, step in enumerate(agenda_steps, 1):
        st.markdown(f"""
        <div class="info-card" style="display: flex; align-items: flex-start; gap: 15px; padding: 20px; margin-bottom: 15px;">
            <div style="background: rgba(0, 212, 255, 0.1); color: #00d4ff; font-size: 1.2rem; font-weight: bold; 
                        width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                {i}
            </div>
            <div style="flex: 1;">
                <h4 style="margin: 0 0 5px 0; color: white; display: flex; align-items: center; gap: 10px;">
                    {step['title']} 
                    <span style="font-size: 0.8rem; background: rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 12px; color: #00d4ff; border: 1px solid rgba(0,212,255,0.3);">
                        {step['icon']} {step['tool']}
                    </span>
                </h4>
                <p style="margin: 0; color: #ccc; font-size: 0.95rem; line-height: 1.5;">{step['desc']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Detailed Step-by-Step
    st.markdown("### 🔄 Step-by-Step Pipeline Execution")
    
    execution_steps = [
        {"num": "01", "title": "Data Ingestion (Airflow)", "icon": "📝",
         "desc": "Fetch random user data from an external API (`randomuser.me`). Airflow orchestrates this task to run periodically."},
        {"num": "02", "title": "Message Broker (Kafka)", "icon": "📨",
         "desc": "The fetched data is pushed to a Kafka topic named `users_data`. Kafka acts as a buffer/queue to decouple the ingestion from processing."},
        {"num": "03", "title": "Stream Processing (Spark)", "icon": "⚡",
         "desc": "Spark Structured Streaming consumes messages from Kafka in real-time. It transforms the JSON data into a structured format."},
        {"num": "04", "title": "Storage (Cassandra)", "icon": "💾",
         "desc": "The processed records are written to Apache Cassandra, a NoSQL database designed for high write throughput."},
        {"num": "05", "title": "Visualization (Streamlit)", "icon": "📊",
         "desc": "This dashboard connects to Cassandra and visualizes the incoming data live, completing the end-to-end flow."}
    ]
    
    for step in execution_steps:
        st.markdown(f"""
        <div class="info-card" style="display: flex; align-items: center; gap: 20px; padding: 15px;">
            <div style="background: linear-gradient(135deg, #00d4ff, #00ff88); color: #000; font-size: 1.5rem; font-weight: bold; 
                        width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                {step['num']}
            </div>
            <div style="flex: 1;">
                <h4 style="margin: 0; color: #00d4ff;">{step['icon']} {step['title']}</h4>
                <p style="margin: 5px 0; color: #ccc;">{step['desc']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==================== TAB 3: ARCHITECTURE & TECH STACK ====================
with tab3:
    st.markdown("## 🏗️ System Architecture")
    st.markdown("---")
    
    # Visual Flow Diagram (CSS based)
    st.markdown("### 📐 Data Flow Visual")
    st.markdown("""
    <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 15px; margin: 20px 0;">
        <div style="display: flex; justify-content: center; align-items: center; flex-wrap: nowrap; gap: 10px; overflow-x: auto;">
            <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 10px 15px; border-radius: 10px; min-width: 110px;">
                <span style="display: block; font-size: 1rem; color: white; font-weight: 800; margin-bottom: 5px;">API Source</span>
                <span style="display: block; font-size: 0.75rem; color: #eee;">randomuser.me</span>
            </div>
            <span style="font-size: 1.5rem; color: white; font-weight: bold;">➜</span>
            <div style="background: linear-gradient(135deg, #f093fb, #f5576c); padding: 10px 15px; border-radius: 10px; min-width: 110px;">
                <span style="display: block; font-size: 1rem; color: white; font-weight: 800; margin-bottom: 5px;">Airflow</span>
                <span style="display: block; font-size: 0.75rem; color: #eee;">Producer Task</span>
            </div>
            <span style="font-size: 1.5rem; color: white; font-weight: bold;">➜</span>
            <div style="background: linear-gradient(135deg, #4facfe, #00f2fe); padding: 10px 15px; border-radius: 10px; min-width: 110px;">
                <span style="display: block; font-size: 1rem; color: white; font-weight: 800; margin-bottom: 5px;">Kafka</span>
                <span style="display: block; font-size: 0.75rem; color: #eee;">Topic: users_data</span>
            </div>
            <span style="font-size: 1.5rem; color: white; font-weight: bold;">➜</span>
            <div style="background: linear-gradient(135deg, #43e97b, #38f9d7); padding: 10px 15px; border-radius: 10px; min-width: 110px;">
                <span style="display: block; font-size: 1rem; color: black; font-weight: 800; margin-bottom: 5px;">Spark</span>
                <span style="display: block; font-size: 0.75rem; color: #333;">Processing</span>
            </div>
            <span style="font-size: 1.5rem; color: white; font-weight: bold;">➜</span>
            <div style="background: linear-gradient(135deg, #fa709a, #fee140); padding: 10px 15px; border-radius: 10px; min-width: 110px;">
                <span style="display: block; font-size: 1rem; color: black; font-weight: 800; margin-bottom: 5px;">Cassandra</span>
                <span style="display: block; font-size: 0.75rem; color: #333;">Table Storage</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("---")
    
    # Tech Stack Details (Cards)
    st.markdown("### 🛠️ Technology Stack Details")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    tech_stack = [
        {"icon": "🌪️", "name": "Airflow", "desc": "An open-source platform to programmatically author, schedule, and monitor workflows. Used here for orchestrating data ingestion."},
        {"icon": "📨", "name": "Kafka", "desc": "A distributed event streaming platform used for high-performance data pipelines. Acts as the buffer between ingestion and processing."},
        {"icon": "🐘", "name": "Zookeeper", "desc": "Centralized service for maintaining configuration information, naming, providing distributed synchronization, and group services for Kafka."},
        {"icon": "⚡", "name": "Spark", "desc": "A unified analytics engine for large-scale data processing. We use **Spark Structured Streaming** to process real-time data from Kafka."},
        {"icon": "💾", "name": "Cassandra", "desc": "A highly scalable, high-performance distributed NoSQL database designed to handle large amounts of data across many commodity servers."}
    ]
    
    cols = [col1, col2, col3, col4, col5]
    for i, tech in enumerate(tech_stack):
        with cols[i]:
            st.markdown(f"""
            <div class="info-card" style="text-align: center; min-height: 280px; padding: 15px;">
                <div style="font-size: 2.5rem; margin-bottom: 10px;">{tech['icon']}</div>
                <h4 style="color: #00d4ff; margin: 0;">{tech['name']}</h4>
                <hr style="border-color: rgba(255,255,255,0.1); margin: 10px 0;">
                <p style="color: #aaa; font-size: 0.85rem; line-height: 1.4;">{tech['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Real-Time Example
    st.markdown("### 🚀 Real-Time Example: User Sign-up System")
    st.info("""
    **Scenario**: Imagine a user signs up on a website.
    
    1.  **User Action**: A user fills a form on a website.
    2.  **API Call**: The form data is sent to an API.
    3.  **Ingestion**: **Airflow/Producer** grabs this data immediately.
    4.  **Buffering**: **Kafka** queues it securely.
    5.  **Processing**: **Spark** sees the new user, validates the email, checks for duplicates, and inserts it into the database.
    6.  **Insight**: Customer support Dashboard (connected to **Cassandra**) sees the new user appearing **milliseconds** after they clicked 'Submit'.
    """)
    
    # Architecture Image (Fallback)
    st.markdown("---")
    st.markdown("### 📷 Pipeline Diagram")
    image_paths = ["Data engineering architecture.png", "data_engineering_architecture.png", "dags/Data engineering architecture.png"]
    for p in image_paths:
        if os.path.exists(p):
            st.image(Image.open(p), caption="Detailed Architecture Diagram", use_container_width=True)
            break

# ==================== TAB 4: SYSTEM LOGS ====================
with tab4:
    st.markdown("## 🔍 Real-Time System Logs")
    
    # Horizontal Radio Selection
    log_selection = st.radio(
        "Select Service Log:",
        ["Spark Master", "Airflow Scheduler", "Kafka Broker", "Cassandra"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    container_map = {
        "Spark Master": "airflow-kafka-spark-cassandra-streaming-spark-master-1",
        "Airflow Scheduler": "airflow-kafka-spark-cassandra-streaming-scheduler-1",
        "Kafka Broker": "broker",
        "Cassandra": "cassandra"
    }
    
    selected_container = container_map.get(log_selection)
    
    if selected_container:
        st.markdown(f"### 🖥️ {log_selection} Logs")
        logs = get_docker_logs(selected_container, lines=100)
        
        col_buttons = st.columns([1, 4])
        with col_buttons[0]:
            if st.button("🔄 Refresh Logs", key="refresh_logs"):
                st.rerun()
        with col_buttons[1]:
            st.download_button(
                label="📥 Download Logs",
                data=logs,
                file_name=f"{log_selection.replace(' ', '_').lower()}_logs.txt",
                mime="text/plain"
            )
        
        st.code(logs, language="bash", line_numbers=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #white; padding: 30px;'>
    <p style='font-size: 0.9rem; margin-top: 15px;'>
        Built with ❤️ by <strong>Ratnesh Singh</strong> | Data Scientist (4+ Year Exp)
    </p>
    <p style="font-size: 1.2rem;">🚀 <strong></strong> Real-Time User Data Pipeline | End-to-End Data Engineering Project</p>
    <p style="font-size: 1.2rem;">🚀 <strong></strong>Technologies( Python | Apache Airflow | Apache Kafka | Apache Zookeeper | Apache Spark | Cassandra | PostgreSQL | Docker)</p>
    <p style="font-size: 1.2rem;">🚀 <strong></strong>Data Flow ( 1. Airflow (Orchestrator) | 2.Kafka (Message Broker) | 3.Spark (Stream Processing) | 4.Cassandra (NoSQL    Database) | 5.Docker (Containerization) )</p>
     
</div>
""", unsafe_allow_html=True)

# Global Auto-Refresh Logic
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()
