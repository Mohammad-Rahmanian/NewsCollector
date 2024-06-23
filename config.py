import logging
# General configuration for logging
logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

# Custom logger for application-specific logs
app_logger = logging.getLogger('application')
app_logger.setLevel(logging.INFO)

db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'user',
    'password': 'password',
    'database': 'news_db'
}

kafka_config = {
    'bootstrap_servers': 'localhost:9092',
    'topic_name': 'agency_topic',
    'consumer_group': 'news_collector_group',
    'auto_offset_reset': 'earliest',
    'num_partitions': 8,
    'replication_factor': 1
}

file_paths = {
    'news_agencies_csv': './News Agencies.csv'
}