<div style="display: flex; align-items: center;">
  <h1>News Collector System</h1>
  <img src="https://github.com/Mohammad-Rahmanian/NewsCollector/assets/78559411/2032f6b7-3daa-450f-a64d-41e51483b3e4" alt="News" width="100">
</div>

## Project Overview

The News Collector System automates the collection, storage, and management of news from various news agencies. By leveraging a distributed architecture that includes a Kafka cluster and MySQL Cluster, the system ensures efficient data flow, high availability, and robustness in processing news feeds.


<div style="display: flex; align-items: center;">
  
  <h1>Goals</h1>
  <img src="https://github.com/Mohammad-Rahmanian/NewsCollector/assets/78559411/b8d18301-aaa2-4d75-9bec-4d5b9f88c747" alt="News" width="80">
</div>



- **Efficient Data Collection**: Automatically gather and update news from multiple sources.
- **Scalability**: Scale effectively to accommodate growing data and user request loads.
- **Reliability**: Maintain high availability and persistence of news data through a resilient MySQL Cluster.
- **Real-Time Processing**: Utilize Kafka for immediate processing and distribution of news data.


<div style="display: flex; align-items: center;">
  <h1>Architecture</h1>
  <img src="https://github.com/Mohammad-Rahmanian/NewsCollector/assets/78559411/e3863684-14bf-4cdf-b878-5ad20e2f6cfd" alt="News" width="100">
</div>


This project is built around several key components that work together to ensure efficient data handling and storage:

- **Kafka Cluster**: Facilitates the real-time streaming of news data.
- **MySQL Cluster**: Provides scalable and highly available data storage.
- **Worker Nodes**: Handle the processing and storage of news data.
- **Master Node**: Manages and coordinates the workflow between worker nodes.

<div style="display: flex; align-items: center;">
  <h2>Master Node</h2>
  <img src="https://github.com/Mohammad-Rahmanian/NewsCollector/assets/78559411/84de8f0a-9c9f-4685-a0bb-7ce487aef7f1" alt="Master" width="100">
</div>



The master node serves as the central command center for the News Collector System. It performs several critical functions:

- **Load Agencies**: It loads news agencies' information from a dataset, which includes details like agency names and their RSS feed links..
- **Kafka Production**: After loading the data, it produces messages containing RSS feed information to Kafka topics, which worker nodes will consume.
- **Load Balancing**: Distributes tasks evenly across worker nodes to optimize resource utilization and avoid bottlenecks.


<div style="display: flex; align-items: center;">
  <h2>Worker Nodes</h2>
  <img src="https://github.com/Mohammad-Rahmanian/NewsCollector/assets/78559411/210e5cca-ba01-462c-92fd-c5def2bb4331" alt="Worker" width="100">
</div>


Worker nodes are the backbone of data processing within the News Collector System:

- **RSS Feed Processing**: Each worker node retrieves RSS feed messages from Kafka, parses the XML content, and extracts news items.
- **Data Insertion**: After parsing, worker nodes insert the news data into the MySQL Cluster, handling data formatting and ensuring integrity.
- **Scalability Handling**: Worker nodes are designed to scale horizontally, allowing the system to increase processing capabilities simply by adding more nodes.

## System Integration

Each component of the News Collector System is tightly integrated to form a cohesive environment:

- **Kafka** for handling incoming and outgoing data streams with high throughput.
- **MySQL Cluster** for storing structured news data that can be queried and analyzed.
- **Zookeeper** for managing the state of the Kafka cluster nodes and broker coordination.

The worker and master nodes are orchestrated to maximize data processing efficiency and reliability, ensuring that the system can handle real-time data ingestion and processing without data loss or delay.


<div style="display: flex; align-items: center;">
  <h2>Installation and Usage</h2>
  <img src="https://github.com/Mohammad-Rahmanian/NewsCollector/assets/78559411/ffe34d03-b4da-40e6-8e35-9ee74261716a" alt="News" width="100">
</div>


### Building Docker Images

Before running the system, you need to build the Docker images for both the master and the worker nodes. Navigate to the root directory of project  and run the following commands:

```bash
# Build the master node Docker image
docker build -f docker/Dockerfile.master -t app-master .

# Build the worker node Docker image
docker build -f docker/Dockerfile.worker -t app-worker .
```

### Running the System with Docker Compose

After building the Docker images, you can start the system using Docker Compose. Ensure you are in the directory containing the docker-compose.yml file, then execute:

```bash
docker-compose up -d
```

This command will start all components of the News Collector System, including Kafka brokers, Zookeeper, MySQL Cluster, and the worker and master nodes.


### Accessing Adminer

Adminer is set up to manage the MySQL database. It can be accessed via:

```
http://localhost:8081
```
