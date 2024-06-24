import pandas as pd
from database import setup_database, insert_news_agency
from kafka_utils import create_kafka_producer, create_kafka_topic, send_message_to_kafka
from config import file_paths, kafka_config, app_logger


def load_and_process_agencies(db, producer):
    """Load news agencies from CSV, add to DB and send to Kafka."""
    try:
        df = pd.read_csv(file_paths['news_agencies_csv'])
        for index, row in df.iterrows():
            try:
                agency_id = insert_news_agency(db, row['name'], row['res_link'])
                if agency_id:
                    message = {'id': agency_id, 'name': row['name'], 'link': row['res_link']}
                    send_message_to_kafka(producer, kafka_config['topic_name'], str(agency_id).encode('utf-8'), message)
                    app_logger.info(f"Produced message to Kafka: {message}")
            except Exception as e:
                app_logger.error(f"Failed to process agency {row['name']}: {e}")
    except FileNotFoundError as e:
        app_logger.error(f"Could not read file: {e}")
    except Exception as e:
        app_logger.error(f"Error processing agencies: {e}")


def main():
    """Main function to set up and run the application logic."""
    try:
        db = setup_database()
        if db:
            create_kafka_topic()  # Setup Kafka topic
            producer = create_kafka_producer()
            load_and_process_agencies(db, producer)
        else:
            app_logger.error("Database setup failed, terminating application.")
    except Exception as e:
        app_logger.critical(f"Critical failure in main application: {e}")


if __name__ == "__main__":
    main()
