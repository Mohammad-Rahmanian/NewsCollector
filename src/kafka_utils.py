import json
import time
from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError, NoBrokersAvailable, KafkaError
from config import kafka_config, app_logger


def create_kafka_producer():
    """Create and return a Kafka producer with logging."""
    try:
        producer = KafkaProducer(
            bootstrap_servers=kafka_config['bootstrap_servers'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        app_logger.info("Kafka producer created successfully.")
        return producer
    except NoBrokersAvailable:
        app_logger.error("Failed to connect to Kafka brokers.")
        return None


def create_kafka_topic():
    """Create a Kafka topic based on configuration settings with exception handling."""
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=kafka_config['bootstrap_servers'],
            client_id='admin_client'
        )
        topic = NewTopic(
            name=kafka_config['topic_name'],
            num_partitions=kafka_config['num_partitions'],
            replication_factor=kafka_config['replication_factor']
        )
        admin_client.create_topics(new_topics=[topic])
        app_logger.info(f"Topic {kafka_config['topic_name']} created successfully.")
    except TopicAlreadyExistsError:
        app_logger.warning(f"Topic {kafka_config['topic_name']} already exists.")
    except KafkaError as e:
        app_logger.error(f"Failed to create topic due to KafkaError: {e}")


def send_message_to_kafka(producer, topic, key, message):
    """Send a message to a Kafka topic and log the outcome."""
    if not producer:
        app_logger.error("Producer not available, cannot send message.")
        return
    try:
        future = producer.send(topic, key=key, value=message)
        future.get(timeout=10)
        app_logger.info(f"Message sent to topic {topic}: {message}")
    except KafkaError as e:
        app_logger.error(f"Failed to send message to Kafka: {e}")


def create_kafka_consumer(group_id):
    """Create and return a Kafka consumer for a specific group with error handling."""
    try:
        consumer = KafkaConsumer(
            bootstrap_servers=kafka_config['bootstrap_servers'],
            group_id=group_id,
            auto_offset_reset=kafka_config['auto_offset_reset'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        app_logger.info(f"Kafka consumer created for group {group_id}.")
        return consumer
    except NoBrokersAvailable:
        app_logger.error("No Kafka brokers available to connect.")
        return None


def wait_for_topic(consumer, topic):
    """Wait for the specified topic to be ready, with logging and timeout."""
    if not consumer:
        app_logger.error("Consumer not available, cannot wait for topic.")
        return
    app_logger.info(f"Waiting for topic {topic} to become available.")

    while topic not in consumer.topics():
        time.sleep(1)
    app_logger.info(f"Topic {topic} is now available.")
