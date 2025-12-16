# ⚡ Real-Time Data Pipeline: End-to-End Data Engineering Project

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-Orchestration-blue?style=for-the-badge&logo=apache-airflow)
![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-Streaming-black?style=for-the-badge&logo=apache-kafka)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-Processing-orange?style=for-the-badge&logo=apache-spark)
![Apache Cassandra](https://img.shields.io/badge/Apache%20Cassandra-Storage-skyblue?style=for-the-badge&logo=apache-cassandra)
![Docker](https://img.shields.io/badge/Docker-Containerization-blue?style=for-the-badge&logo=docker)
![Streamlit](https://img.shields.io/badge/Streamlit-Visualization-red?style=for-the-badge&logo=streamlit)

---

## 🚀 Overview

This project implements a scalable, fault-tolerant, **End-to-End Real-Time Data Engineering Pipeline** capable of processing user data in milliseconds. It demonstrates a complete flow from data ingestion to visualization using industry-standard tools.

---
## 🌐🎬 Live Demo
🚀 **Try it now:**
- **Streamlit Profile** - https://share.streamlit.io/user/ratnesh-181998
- **Project Demo** - https://realtime-data-pipeline-airflow-kafka-spark-cassandra-docker-7v.streamlit.app/
- **Technologies** - Apache Airflow(Orchestrator),Python,Apache Kafka(Message Broker),Apache Zookeeper,Apache Spark(Stream Processing) ,Cassandra(NoSQL Database),PostgreSQL,Docker(Containerization)
---
### 🌟 Key Features
- **Real-Time Data Ingestion**: Systematically fetches user data from an external API (`randomuser.me`) using **Apache Airflow**.
- **Event Streaming**: Uses **Apache Kafka** (and Zookeeper) to buffer and stream data events, ensuring decoupling and reliability.
- **Stream Processing**: Leverages **Spark Structured Streaming** to consume, process, and transform data in real-time.
- **NoSQL Storage**: Persists processed records into **Apache Cassandra** for high-throughput write performance.
- **Interactive Dashboard**: Visualizes live data trends, logs, and system health using **Streamlit**.
- **Containerization**: Fully Dockerized environment for consistent deployment across any machine.

---

## 🏗️ Architecture

<img width="1654" height="622" alt="image" src="https://github.com/user-attachments/assets/ebd8ddff-4082-450e-a1b8-3dffcb5c1c85" />


The pipeline follows a standard robust data engineering architecture:
1.  **Ingestion Source**: `randomuser.me` API.
2.  **Orchestrator**: **Airflow DAG** triggers a producer task periodically.
3.  **Message Broker**: **Kafka** receives the JSON data and queues it in the `users_data` topic.
4.  **Processing Engine**: **Spark Master & Workers** subscribe to the Kafka topic, process the stream, and extract relevant fields.
5.  **Data Sink**: **Cassandra** stores the clean, structured user data.
6.  **Visualization**: **Streamlit Web App** connects to Cassandra to display real-time insights.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.9 | Core programming language for scripts and DAGs. |
| **Orchestration** | Apache Airflow | schedules and monitors the data ingestion workflows. |
| **Streaming** | Apache Kafka | Distributed event streaming platform for high-throughput pipelines. |
| **Coordination** | Apache Zookeeper | Manages specific configurations and synchronization for Kafka. |
| **Processing** | Apache Spark | Unified analytics engine for large-scale data processing (Structured Streaming). |
| **Database** | Apache Cassandra | Wide-column NoSQL store known for scalability and high availability. |
| **Visualization** | Streamlit | Turns data scripts into shareable web apps in minutes. |
| **Containerization** | Docker | Ensures the application works on any machine by bundling dependencies. |

---

## 📊 Dashboard UI Features

The **Streamlit Dashboard** is the command center for this project, featuring **4 Interactive Tabs**:

### 1. 📊 Project Demo (Live)
- **Live Metrics**: Shows "Total Records Processed", "Latest User", and "System Status".
- **Real-Time Charts**:
    - **Gender Distribution**: Dynamic Pie chart updating as new users arrive.
    - **Top Email Providers**: Bar chart analyzing email domains (Gmail, Yahoo, etc.).
    - **Registration Timeline**: Trend analysis of user registrations over the years.
- **Live Data Table**: Displays the most recent 20 records inserted into the database.

<img width="940" height="475" alt="image" src="https://github.com/user-attachments/assets/e50a606e-62eb-4ea4-bd17-efd3ade61ee5" />
<img width="940" height="470" alt="image" src="https://github.com/user-attachments/assets/08575c6c-9921-4669-90d7-17d728c9c714" />
<img width="940" height="477" alt="image" src="https://github.com/user-attachments/assets/15077900-c670-422a-8ac0-bb93eaa02741" />
<img width="940" height="475" alt="image" src="https://github.com/user-attachments/assets/b1f6b91f-dd66-4f45-8bde-77a4cb8a1146" />

### 2. ℹ️ About the Project
- **Pizza Shop Analogy**: Explains the complex Kafka/Spark/Cassandra flow using a simple "Waiter -> Kitchen -> Table" analogy.
- **Project Agenda**: Detailed breakdown of every stage (Ingestion, Orchestration, Streaming, etc.).
- **Step-by-Step Guide**: Explains exactly what happens to a data packet from API to Dashboard.
<img width="940" height="469" alt="image" src="https://github.com/user-attachments/assets/90fc0070-2bf9-43c1-8f65-a9e51e507c0f" />
<img width="940" height="483" alt="image" src="https://github.com/user-attachments/assets/6e96c2b8-d962-4881-9a0b-cf71b4e7a003" />
<img width="940" height="474" alt="image" src="https://github.com/user-attachments/assets/1b04857f-0787-4182-8953-db9e03e12b0b" />
<img width="940" height="475" alt="image" src="https://github.com/user-attachments/assets/347befdc-8d96-46f9-8d9b-cc4c9c313f86" />
<img width="940" height="469" alt="image" src="https://github.com/user-attachments/assets/abdf277d-fa0e-43db-85d7-196c9d4e74b3" />

### 3. 🏗️ Architecture & Tech Stack
- **Visual Data Flow**: A CSS-styled flow diagram showing the journey of data.
- **Tech Deep Dive**: Information cards explaining why each technology (Airflow, Kafka, etc.) was chosen.
- **Real-World Example**: Describes how this pipeline mirrors a real "User Sign-Up System".
<img width="940" height="478" alt="image" src="https://github.com/user-attachments/assets/3aa5deee-dcc8-42e0-9514-aa071393d180" />
<img width="940" height="469" alt="image" src="https://github.com/user-attachments/assets/14e359bc-1495-47f5-893e-199520260681" />
<img width="940" height="477" alt="image" src="https://github.com/user-attachments/assets/d680fd36-ac93-4003-b9ba-98ceac258452" />


### 4. 📜 System Logs (Simulated for Cloud)
- **Centralized Logging**: View logs from **Spark Master**, **Airflow Scheduler**, **Kafka Broker**, and **Cassandra** in one place.
- **Downloadable Logs**: One-click download button to save system logs for debugging.
- **Refresh Capability**: Button to fetch the latest system status.
<img width="940" height="483" alt="image" src="https://github.com/user-attachments/assets/df0c9ef4-8bab-49fd-90d0-95ddf9e0ce2b" />
<img width="940" height="482" alt="image" src="https://github.com/user-attachments/assets/b2100fe3-dccc-4d4c-bb41-dbdf46518077" />
<img width="940" height="468" alt="image" src="https://github.com/user-attachments/assets/ddcae12d-7696-4d4b-98f5-2e34ed43e9e0" />
<img width="940" height="470" alt="image" src="https://github.com/user-attachments/assets/0d24da49-080f-4e22-a668-892711c46e41" />

### 5. 📜 Project Run (Local System)
<img width="940" height="274" alt="image" src="https://github.com/user-attachments/assets/b1f42bd3-d7e7-480d-8d44-82b31e89cae9" />
<img width="940" height="559" alt="image" src="https://github.com/user-attachments/assets/21727a77-ba20-40a1-8e11-b74819e02488" />
<img width="940" height="552" alt="image" src="https://github.com/user-attachments/assets/c7999805-3935-4778-b58b-2126e319bc5c" />
<img width="940" height="589" alt="image" src="https://github.com/user-attachments/assets/c500eab8-9911-4eac-bb5e-9297e700663e" />
<img width="940" height="589" alt="image" src="https://github.com/user-attachments/assets/03e64dde-ef91-4c13-9e81-511d64384678" />
<img width="940" height="532" alt="image" src="https://github.com/user-attachments/assets/d9362d2c-cc2c-4b5f-b87d-fc79af0298b5" />
<img width="940" height="525" alt="image" src="https://github.com/user-attachments/assets/014cc2a4-5e46-4259-a1c2-4f4a49eac983" />
<img width="940" height="526" alt="image" src="https://github.com/user-attachments/assets/e5809dbb-002c-445a-8802-f5d5d6fea8ea" />


---

## 💻 Installation & Setup (Local)

### Prerequisites
- Docker & Docker Compose
- Python 3.9+
- Git

### Steps
1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Ratnesh-181998/Realtime-Data-Pipeline-Airflow-Kafka-Spark-Cassandra-Docker.git
    cd Realtime-Data-Pipeline-Airflow-Kafka-Spark-Cassandra-Docker
    ```

2.  **Start Services (Docker)**
    ```bash
    docker-compose up -d
    ```
    *This might take 5-10 minutes to pull all images (Airflow, Kafka, Spark, Cassandra).*

3.  **Install Python Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Dashboard**
    ```bash
    streamlit run app.py
    ```

---

## ☁️ Deployment (Streamlit Cloud)

This project includes a **Cloud-Optimized Version** that runs without the heavy local infrastructure.

1.  **Upload** the contents of the `streamlit_cloud_version` folder to your GitHub repo.
2.  **Connect** your GitHub account to **Streamlit Cloud**.
3.  **Deploy** the `app.py` file.
    - *Note: The cloud version uses simulated backend data for demonstration purposes.*

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 📞 Contact

**RATNESH SINGH**

- 📧 Email: [rattudacsit2021gate@gmail.com](mailto:rattudacsit2021gate@gmail.com)
- 💼 LinkedIn: [https://www.linkedin.com/in/ratneshkumar1998/](https://www.linkedin.com/in/ratneshkumar1998/)
- 🐙 GitHub: [https://github.com/Ratnesh-181998](https://github.com/Ratnesh-181998)
- 📱 Phone: +91-947XXXXX46

### Project Links
- 🌐 Live Demo: [Streamlit Cloud App](https://realtime-data-pipeline-airflow-kafka-spark-cassandra-docker-7v.streamlit.app/)
- 📖 Documentation: [GitHub Wiki](https://github.com/Ratnesh-181998/Realtime-Data-Pipeline-Airflow-Kafka-Spark-Cassandra-Docker)
- 🐛 Issue Tracker: [GitHub Issues](https://github.com/Ratnesh-181998/Realtime-Data-Pipeline-Airflow-Kafka-Spark-Cassandra-Docker/issues)

---
*Built with ❤️ by Ratnesh Singh | Data Scientist(4+Year Experience)*
