import requests
import xml.etree.ElementTree as ET
from database import insert_news_items, setup_database
from kafka_utils import create_kafka_consumer, wait_for_topic
from config import kafka_config, app_logger


def parse_rss(url):
    """Fetch and parse RSS feed returning news items."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        news_items = []
        for item in root.findall('.//item'):
            news_dict = {'title': item.find('title').text, 'link': item.find('link').text}
            news_items.append(news_dict)
        return news_items
    except requests.RequestException as e:
        app_logger.error(f"Network or HTTP error occurred while fetching RSS feed: {e}")
        return []
    except ET.ParseError as e:
        app_logger.error(f"XML parsing error: {e}")
        return []


def process_messages(consumer, db):
    """Process messages from Kafka topic."""
    for message in consumer:
        agency_data = message.value
        app_logger.info(
            f"Consuming message from partition {message.partition} for agency {agency_data['name']} with RSS link {agency_data['link']}")

        rss_link = agency_data['link']
        if rss_link:
            news_items = parse_rss(rss_link)
            if news_items:
                insert_news_items(db, news_items, agency_data['id'])
                app_logger.info(f"Inserted {len(news_items)} items for agency {agency_data['name']}.")


def main():
    """Main function to handle workflow of consuming Kafka messages and processing news data."""
    db = setup_database()
    consumer = create_kafka_consumer(kafka_config['consumer_group'])
    consumer.subscribe([kafka_config['topic_name']])
    wait_for_topic(consumer, kafka_config['topic_name'])
    app_logger.info("Ready to consume messages...")

    try:
        process_messages(consumer, db)
    except Exception as e:
        app_logger.critical(f"An error occurred: {e}")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
