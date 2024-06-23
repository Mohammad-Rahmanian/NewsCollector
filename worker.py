import requests
import xml.etree.ElementTree as ET
from database import insert_news_items,setup_database
from kafka_utils import create_kafka_consumer, wait_for_topic
from config import kafka_config,app_logger

def parse_rss(url):
    """Fetch and parse RSS feed returning news items."""
    try:
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
    except requests.RequestException as e:
        app_logger.error(f"Failed to fetch RSS feed: {e}")
        return []


def main():
    """Main function to handle workflow of consuming Kafka messages and processing news data."""
    db = setup_database()

    consumer = create_kafka_consumer(kafka_config['consumer_group'])
    consumer.subscribe([kafka_config['topic_name']])

    wait_for_topic(consumer, kafka_config['topic_name'])
    app_logger.info("Ready to consume messages...")

    for message in consumer:
        agency_data = message.value
        app_logger.info(
            f"Consuming message for agency {agency_data['name']} with RSS link {agency_data['link']} from partition {message.partition}")

        rss_link = agency_data['link']
        if rss_link:
            news_items = parse_rss(rss_link)
            if news_items:
                insert_news_items(db, news_items, agency_data['id'])


if __name__ == "__main__":
    main()
