import pandas as pd
from database import connect_to_database, create_news_agency_table, insert_news_agency
from kafka_utils import create_kafka_producer, create_kafka_topic
from config import file_paths,kafka_config

if __name__ == "__main__":
    db = connect_to_database()
    create_news_agency_table(db)
    create_kafka_topic()
    producer = create_kafka_producer()
    df = pd.read_csv(file_paths['news_agencies_csv'])

    for index, row in df.iterrows():
        agency_id = insert_news_agency(db, row['name'], row['link'])
        key = str(agency_id).encode('utf-8')
        message = {'id': agency_id, 'name': row['name'], 'link': row['link']}
        producer.send(kafka_config['topic_name'], key=key, value=message)
        producer.flush()
        print(f"Produced message to Kafka: {message}")
