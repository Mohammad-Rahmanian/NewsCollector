from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import NewTopic,KafkaAdminClient
from config import kafka_config
import json

def create_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=kafka_config['bootstrap_servers'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

def create_kafka_topic():
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
        admin_client.create_topics(new_topics=[topic], validate_only=False)
        print(f"Topic {kafka_config['topic_name']} created.")
    except Exception as e:
        print(f"Failed to create topic: {str(e)}")

def create_kafka_consumer(group_id):
    return KafkaConsumer(
        bootstrap_servers=kafka_config['bootstrap_servers'],
        group_id=group_id,
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    ),kafka_config['topic_name']
