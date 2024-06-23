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
    'num_partitions': 8,
    'replication_factor': 1
}

file_paths = {
    'news_agencies_csv': './News Agencies.csv'
}
