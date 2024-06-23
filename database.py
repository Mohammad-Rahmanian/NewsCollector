
import mysql.connector
from config import db_config

def connect_to_database():
    connection = mysql.connector.connect(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
    return connection

def create_news_agency_table(connection):
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news_agency (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            rss_link VARCHAR(255) NOT NULL
        )
    ''')
    connection.commit()

def create_news_table(connection):
    cursor = connection.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS news (
        id INT AUTO_INCREMENT PRIMARY KEY,
        agency_id INT,
        news_link VARCHAR(1023),
        news_title VARCHAR(255),
        crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (agency_id) REFERENCES news_agency(id)
    );
    """
    cursor.execute(query)
    connection.commit()

def insert_news_agency(connection, name, rss_link):
    cursor = connection.cursor()
    query = "INSERT INTO news_agency (name, rss_link) VALUES (%s, %s)"
    cursor.execute(query, (name, rss_link))
    connection.commit()
    return cursor.lastrowid


def insert_news_items(connection, news_items, agency_id):
    cursor = connection.cursor()
    query = """
    INSERT INTO news (agency_id, news_link, news_title)
    VALUES (%s, %s, %s)
    """
    try:
        data_tuples = [(agency_id, item['link'], item['title']) for item in news_items]

        cursor.executemany(query, data_tuples)
        connection.commit()
        print(f"{cursor.rowcount} records inserted successfully into the news table.")
    except mysql.connector.Error as err:
        print("Failed to insert records into MySQL table: {}".format(err))
    finally:
        cursor.close()
