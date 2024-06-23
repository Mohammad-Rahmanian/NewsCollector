import pandas as pd
from database import setup_database, insert_news_agency
from kafka_utils import create_kafka_producer, create_kafka_topic, send_message_to_kafka
from config import file_paths, kafka_config,app_logger


def load_and_process_agencies(db, producer):
    """Load news agencies from CSV, add to DB and send to Kafka."""
    df = pd.read_csv(file_paths['news_agencies_csv'])
    for index, row in df.iterrows():
        agency_id = insert_news_agency(db, row['name'], row['link'])
        if agency_id:  # Ensure the agency was added before sending to Kafka
            message = {'id': agency_id, 'name': row['name'], 'link': row['link']}
            send_message_to_kafka(producer, kafka_config['topic_name'], str(agency_id).encode('utf-8'), message)
            app_logger.info(f"Produced message to Kafka: {message}")

if __name__ == "__main__":
    db = setup_database()
    if db:  # Ensure the database setup was successful before proceeding
        create_kafka_topic()  # Setup Kafka topic
        producer = create_kafka_producer()
        load_and_process_agencies(db, producer)
