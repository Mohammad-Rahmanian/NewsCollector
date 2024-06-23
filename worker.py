from database import connect_to_database, create_news_table,create_news_agency_table,insert_news_items
from kafka_utils import create_kafka_consumer
import time
from config import kafka_config
import requests
import xml.etree.ElementTree as ET
def wait_for_topic(consumer, topic):
    while True:
        topics = consumer.topics()
        if topic in topics:
            print(f"Topic {topic} is now available.")
            break
        time.sleep(1)

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

if __name__ == "__main__":
    db = connect_to_database()
    create_news_agency_table(db)
    create_news_table(db)
    consumer,topic = create_kafka_consumer('news_collector_group')
    consumer.subscribe(topic)
    wait_for_topic(consumer, kafka_config['topic_name'])
    for message in consumer:
        print("Wait message ..")
        agency_data = message.value
        print(f"Consuming message for agency name {agency_data['name']} with RSS link {agency_data['link']} from partition {message.partition}")
        rss_link = agency_data['link']
        if rss_link:
            news_items = parse_rss(rss_link)
            insert_news_items(db,news_items,agency_data['id'])