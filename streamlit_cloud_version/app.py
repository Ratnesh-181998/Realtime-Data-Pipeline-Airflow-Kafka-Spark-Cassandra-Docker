import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import time
import os
import datetime
import random

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

# ------------------ FUNCTIONS (MOCKED FOR CLOUD) ------------------

def get_cassandra_session():
    # Simulate meaningful connection check
    return True

def get_data(session):
    # GENERATE FAKE DATA FOR DEMO
    users = []
    base_time = datetime.datetime.now()
    
    # Generate 50 items
    first_names = ["Ratnesh", "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Ivan"]
    last_names = ["Singh", "Doe", "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia"]
    genders = ["male", "female"]
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "example.com"]
    
    for i in range(50):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        g = random.choice(genders)
        email = f"{fn.lower()}.{ln.lower()}@{random.choice(domains)}"
        reg_date = base_time - datetime.timedelta(days=random.randint(0, 365*20)) # 20 years history
        
        users.append({
            "username": f"{fn.lower()}{random.randint(100,999)}",
            "first_name": fn,
            "last_name": ln,
            "gender": g,
            "email": email,
            "registered_date": reg_date
        })
        
    df = pd.DataFrame(users)
    count = 5432 + random.randint(1, 100) # Fake growing count
    return count, df

def get_docker_logs(container_name, lines=50):
    # RETURN STATIC LOG SAMPLES
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if "spark" in container_name.lower():
        return f"""{timestamp} INFO SparkContext: Running Spark version 3.5.0
{timestamp} INFO ResourceUtils: ==============================================================
{timestamp} INFO ResourceUtils: No custom resources configured for spark.driver.
{timestamp} INFO SparkContext: Submitted application: SparkDataStreaming
{timestamp} INFO Utils: Successfully started service 'sparkDriver' on port 51234.
{timestamp} INFO Executor: Started executor ID 1 on host 172.18.0.4
{timestamp} INFO BlockManagerMasterEndpoint: Registering block manager 172.18.0.4:45612 with 9.8 GB RAM, BlockManagerId(1, 172.18.0.4, 45612, None)
{timestamp} INFO Utils: Successfully started service 'SparkUI' on port 4040.
{timestamp} INFO SparkContext: Added JAR file:/opt/spark/jars/spark-sql-kafka-0-10_2.12-3.5.0.jar
{timestamp} INFO SparkContext: Added JAR file:/opt/spark/jars/spark-cassandra-connector_2.12-3.4.0.jar
{timestamp} INFO ContextCleaner: Cleaned accumulator 1
{timestamp} INFO BlockManagerInfo: Added broadcast_0_piece0 in memory on 172.18.0.4:45612 (size: 4.8 KB, free: 9.8 GB)
{timestamp} INFO TaskSetManager: Starting task 0.0 in stage 0.0 (TID 0) (172.18.0.4, executor 1, partition 0, PROCESS_LOCAL, 7846 bytes)
{timestamp} INFO Executor: Finished task 0.0 in stage 0.0 (TID 0). 876 bytes result sent to driver
{timestamp} INFO TaskSetManager: Finished task 0.0 in stage 0.0 (TID 0) in 123 ms on 172.18.0.4 (executor 1) (1/1)
{timestamp} INFO DAGScheduler: ResultStage 0 (start at SparkDataStreaming.py:45) finished in 0.123 s
{timestamp} INFO CodeGenerator: Code generated in 12.345 ms
{timestamp} INFO WriteToDataSourceV2Exec: Data source write support: org.apache.spark.sql.execution.streaming.sources.MicroBatchWrite@...
{timestamp} INFO MicroBatchExecution: Triggering new Streaming Query processing..."""
    elif "kafka" in container_name.lower() or "broker" in container_name.lower():
         return f"""[{timestamp},123] INFO [KafkaServer id=1] started (kafka.server.KafkaServer)
[{timestamp},150] INFO [LogPartition=users_data-0] log directory '/var/lib/kafka/data' found.
[{timestamp},180] INFO [GroupCoordinator 1]: Starting up.
[{timestamp},210] INFO [SocketServer brokerId=1] Started data-plane acceptor and processor(s) for endpoint :PLAINTEXT://:9092
[{timestamp},234] INFO [TransactionCoordinator id=1] Starting up.
[{timestamp},345] INFO [TransactionCoordinator id=1] Startup complete.
[{timestamp},400] INFO [ExpirationReaper-1-Topic]: Starting
[{timestamp},450] INFO [LogDirFailureHandler]: Starting
[{timestamp},567] INFO [GroupCoordinator 1]: Startup complete.
[{timestamp},600] INFO [ZkClient] Wire protocol version: 2
[{timestamp},620] INFO [ZkClient] Connected to 127.0.0.1:2181
[{timestamp},650] INFO [ClusterControlManager] Controller 1 epoch 1 started
[{timestamp},678] INFO [/config/changes-event-process-thread]: Starting
[{timestamp},700] INFO [SocketServer brokerId=1] Started socket server acceptors and processors
[{timestamp},901] INFO Kafka version: 3.5.0
[{timestamp},012] INFO Kafka commitId: 2c6fb6c54477090f
[{timestamp},050] INFO [ReplicaManager broker=1] Started replica manager
[{timestamp},080] INFO [Partition user_data-0 broker=1] No checkpointed highwatermark is found for partition user_data-0
[{timestamp},123] INFO [ReplicaFetcherManager on broker 1] Removed fetcher for partitions users_data-0
[{timestamp},234] INFO [ReplicaFetcherManager on broker 1] Added fetcher for partitions users_data-0
[{timestamp},345] INFO [Log partition=users_data-0, dir=/var/lib/kafka/data] Rolled new log segment at offset 0 in 2 ms.
[{timestamp},456] INFO [Log partition=users_data-0, dir=/var/lib/kafka/data] Incrementing log start offset to 0
[{timestamp},567] INFO [GroupMetadataManager brokerId=1] Removed 0 expired offsets in 0 milliseconds.
[{timestamp},600] INFO [Processor] Processing 150 requests/s from Producer-1
[{timestamp},650] INFO [LogCleaner] Cleaning log users_data-0, deletes: 0%, size: 1.2 MB"""
    elif "cassandra" in container_name.lower():
        return f"""INFO  [{timestamp}]  StorageService.java:3005 - Node localhost/127.0.0.1 state jump to NORMAL
INFO  [{timestamp}]  StartupChecks.java:169 - jemalloc seems to be preloaded from /usr/lib/x86_64-linux-gnu/libjemalloc.so.2
INFO  [{timestamp}]  CassandraDaemon.java:556 - Cassandra 4.1.0-SNAPSHOT
INFO  [{timestamp}]  StorageService.java:1446 - JOINING: Finish joining ring
INFO  [{timestamp}]  DseDaemon.java:628 - DSE startup complete.
INFO  [{timestamp}]  Server.java:178 - Starting listening for CQL clients on /0.0.0.0:9042 (encrypted: false)
INFO  [{timestamp}]  Gossiper.java:1918 - No gossip backlog; proceeding
INFO  [{timestamp}]  MessagingService.java:433 - Starting Messaging Service on /127.0.0.1:7000 (encrypted: false)
INFO  [{timestamp}]  ColumnFamilyStore.java:449 - Initializing spark_streams.created_users
INFO  [{timestamp}]  ViewManager.java:137 - Initializing spark_streams.created_users view manager
INFO  [{timestamp}]  CompactionStrategyManager.java:89 - No compaction strategy decided for table spark_streams.created_users
INFO  [{timestamp}]  StorageService.java:2528 - Node /127.0.0.1 state jump to UPTODATE
INFO  [{timestamp}]  Memtable.java:123 - CF spark_streams.created_users switching to new memtable...
INFO  [{timestamp}]  HintsService.java:198 - Paused hints dispatch"""
    elif "airflow" in container_name.lower():
        return f"""[{timestamp}] {{scheduler_job.py:961}} INFO - Starting the scheduler
[{timestamp}] {{scheduler_job.py:966}} INFO - Processing each file at most -1 times
[{timestamp}] {{dag_processing.py:260}} INFO - Launching DagFileProcessorManager with 2 processes
[{timestamp}] {{scheduler_job.py:1057}} INFO - Resetting orphaned tasks for active dag runs
[{timestamp}] {{processor.py:161}} INFO - Processing /opt/airflow/dags/kafka_stream.py
[{timestamp}] {{scheduler_job.py:1283}} INFO - Executor reports execution of user_ingestion_task execution_date=2025-12-16T12:00:00+00:00 exited with success for try_number 1
[{timestamp}] {{scheduler_job.py:1320}} INFO - TaskInstance Finished: dag_id=kafka_stream, task_id=user_ingestion_task, run_id=scheduled__2025-12-16T12:00:00+00:00, map_index=-1, run_start_date=2025-12-16 12:00:01+00:00, run_end_date=2025-12-16 12:00:05+00:00, run_duration=4.123, state=success, executor_state=success, try_number=1, max_tries=0, job_id=None, pool=default_pool, queue=default, priority_weight=1, operator=PythonOperator, queued_dttm=2025-12-16 12:00:00+00:00, queued_by_job_id=123, pid=456
[{timestamp}] {{dag.py:2987}} INFO - Syncing DAGs...
[{timestamp}] {{processor.py:173}} INFO - Finished processing /opt/airflow/dags/kafka_stream.py
[{timestamp}] {{scheduler_job_runner.py:412}} INFO - 1 tasks up for execution:
   <TaskInstance: kafka_stream.user_ingestion_task scheduled__2025-12-16T12:05:00+00:00 [scheduled]>
[{timestamp}] {{scheduler_job_runner.py:534}} INFO - Sending TaskInstanceKey(dag_id='kafka_stream', task_id='user_ingestion_task', run_id='scheduled__2025-12-16T12:05:00+00:00', map_index=-1, try_number=1) to executor with priority 1 and queue default"""
    
    return "No logs available."

# ------------------ SIDEBAR ------------------

with st.sidebar:
    st.image("https://airflow.apache.org/images/feature-image.png", use_container_width=True)
    st.markdown("## 🎛️ Pipeline Control")
    st.markdown("---")
    
    # Connection Status
    session = get_cassandra_session()
    if session:
        st.markdown('<div class="metric-card"><span class="live-dot"></span><strong>SYSTEM ONLINE</strong><br><small>Cloud Demo Mode</small></div>', unsafe_allow_html=True)
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
            count, df = get_data(session)
            # Replaced query logic with the mocked get_data returning full DF and count
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            count = 0
            df = pd.DataFrame()

        # Get total count separately for accuracy
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
    st.markdown("###  Project Agenda")
    
    agenda_steps = [
        {"title": "Ingestion", "icon": "", "tool": "API", "desc": "Fetch user data from an external API (randomuser.me)."},
        {"title": "Orchestration", "icon": "🌪️", "tool": "Airflow", "desc": "Schedule and manage the ingestion process using Apache Airflow."},
        {"title": "Streaming", "icon": "📨", "tool": "Kafka", "desc": "Push the ingested data to a message broker to decouple systems."},
        {"title": "Processing", "icon": "⚡", "tool": "Spark", "desc": "Consume data from Kafka using Structured Streaming for transformation."},
        {"title": "Storage", "icon": "💾", "tool": "Cassandra", "desc": "Persist the processed data into a high-performance NoSQL database."},
        {"title": "Containerization", "icon": "", "tool": "Docker", "desc": "Encapsulate the entire stack in Docker for easy deployment."}
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
