import mysql.connector
import pandas as pd
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
import json

# Connect to the MySQL container
db = mysql.connector.connect(
    host="localhost",
    port=3306,  # Explicitly defining the port
    user="user",
    password="password",
    database="news_db"
)

cursor = db.cursor()

# Create table for news agency
cursor.execute('''
CREATE TABLE IF NOT EXISTS news_agency (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    rss_link VARCHAR(255) NOT NULL
)
''')

def create_kafka_topic(topic_name, num_partitions, replication_factor):
    admin_client = KafkaAdminClient(
        bootstrap_servers="localhost:9092",  # Adjust this to your Kafka server settings
        client_id='admin_client'
    )
    topic_list = [NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)]
    try:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        print(f"Topic {topic_name} created with {num_partitions} partitions.")
    except Exception as e:
        print(f"Failed to create topic: {str(e)}")

# Setup Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def add_news_agency(name, rss_link):
    """
    Adds a news agency and its RSS link to the database and sends a message to Kafka.
    """
    if pd.isna(name) or pd.isna(rss_link):
        print("Skipping entry due to NaN values.")
        return
    query = "INSERT INTO news_agency (name, rss_link) VALUES (%s, %s)"
    values = (name, rss_link)
    cursor.execute(query, values)
    db.commit()
    agency_id = cursor.lastrowid  # Get the ID of the inserted news agency
    print(f"Added {name} with RSS link {rss_link} and ID {agency_id}")

    # Produce a message to Kafka
    key = str(agency_id).encode('utf-8')
    message = {'id': agency_id, 'name': name, 'rss_link': rss_link}
    producer.send('agency_topic', key=key, value=message)
    producer.flush()
    print(f"Produced message to Kafka: {message}")




if __name__ == "__main__":
    create_kafka_topic("agency_topic", 8, 1)
    df = pd.read_csv('./News Agencies.csv')
    for index, row in df.iterrows():
        add_news_agency(row['name'], row['link'])
