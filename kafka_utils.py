from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from kafka.admin import NewTopic
from config import kafka_config,app_logger
import json
import time



def create_kafka_producer():
    """Create and return a Kafka producer."""
    producer = KafkaProducer(
        bootstrap_servers=kafka_config['bootstrap_servers'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    return producer


def create_kafka_topic():
    """Create a Kafka topic based on configuration settings."""
    admin_client = KafkaAdminClient(
        bootstrap_servers=kafka_config['bootstrap_servers'],
        client_id='admin_client'
    )
    topic = NewTopic(
        name=kafka_config['topic_name'],
        num_partitions=kafka_config['num_partitions'],
        replication_factor=kafka_config['replication_factor']
    )
    try:
        admin_client.create_topics(new_topics=[topic])
        app_logger.info(f"Topic {kafka_config['topic_name']} created.")
    except Exception as e:
        app_logger.error(f"Failed to create topic: {e}")

def send_message_to_kafka(producer, topic, key, message):
    """Send a message to a Kafka topic."""
    try:
        producer.send(topic, key=key, value=message).get(timeout=100)
        app_logger.info(f"Message sent to topic {topic}: {message}")
    except Exception as e:
        app_logger.error(f"Failed to send message to Kafka: {str(e)}")

def create_kafka_consumer(group_id):
    """Create and return a Kafka consumer for a specific group."""
    consumer = KafkaConsumer(
        kafka_config['topic_name'],
        bootstrap_servers=kafka_config['bootstrap_servers'],
        group_id=group_id,
        auto_offset_reset=kafka_config['auto_offset_reset'],
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    return consumer


def wait_for_topic(consumer, topic):
    """Wait for the specified topic to be ready."""
    app_logger.info(f"Waiting for topic {topic} to be ready.")
    while topic not in consumer.topics():
        time.sleep(1)
    app_logger.info(f"Topic {topic} is now available.")
