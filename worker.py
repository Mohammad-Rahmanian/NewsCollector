import time

import mysql.connector
from mysql.connector import Error
import requests
import xml.etree.ElementTree as ET
from kafka import KafkaConsumer
import json

def connect_to_database(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

def create_news_table(connection):
    cursor = connection.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS news (
        id INT AUTO_INCREMENT PRIMARY KEY,
        agency_id INT,
        news_link VARCHAR(1023),
        news_title VARCHAR(255),
        crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (agency_id) REFERENCES news_agency(id)
    );
    """
    cursor.execute(query)
    connection.commit()
    print("Table created successfully")
def wait_for_topic(consumer, topic):
    """
    Wait for the topic to be ready in Kafka.
    """
    timeout = 30  # wait for 30 seconds
    start_time = time.time()
    while True:
        topics = consumer.topics()
        if topic in topics:
            print(f"Topic {topic} is now available.")
            break
        elif time.time() - start_time > timeout:
            print(f"Timeout waiting for topic {topic}.")
            break
        time.sleep(1)  # sleep for 1 second before retrying

def parse_rss(url):
    response = requests.get(url)
    root = ET.fromstring(response.content)
    news_items = []
    for item in root.findall('.//item'):
        news_dict = {
            'title': item.find('title').text,
            'link': item.find('link').text
        }
        news_items.append(news_dict)
    return news_items

def insert_news_items(connection, news_items, agency_id):
    cursor = connection.cursor()
    query = "INSERT INTO news (agency_id, news_link, news_title) VALUES (%s, %s, %s)"
    cursor.executemany(query, [(agency_id, item['link'], item['title']) for item in news_items])
    connection.commit()
    print(f"{cursor.rowcount} records inserted successfully")

if __name__ == "__main__":
    connection = connect_to_database("localhost", "user", "password", "news_db")
    create_news_table(connection)

    consumer = KafkaConsumer(
        bootstrap_servers=['localhost:9092'],
        group_id='news_collector_group',
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    consumer.subscribe(['agency_topic'])

    # Wait for the topic to be ready
    wait_for_topic(consumer, 'agency_topic')

    print("Consumer is starting to consume messages...")
    for message in consumer:
        agency_data = message.value
        agency_id = agency_data['id']
        agency_name = agency_data['name']
        rss_link = agency_data['rss_link']
        partition_id = message.partition
        print(f"Consuming message for agency name {agency_name} with RSS link {rss_link} from partition {partition_id}")
        if rss_link:
            news_items = parse_rss(rss_link)
            insert_news_items(connection, news_items, agency_id)

    connection.close()
