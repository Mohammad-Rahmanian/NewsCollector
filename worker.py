import mysql.connector
from mysql.connector import Error
import requests
import xml.etree.ElementTree as ET

def connect_to_database(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

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
    try:
        cursor.execute(query)
        connection.commit()
        print("Table created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def parse_rss(url):
    response = requests.get(url)
    root = ET.fromstring(response.content)
    news_items = []
    for item in root.findall('.//item'):
        news_dict = {
            'title': item.find('title').text,
            'link': item.find('link').text
        }
        news_items.append(news_dict)
    return news_items

def fetch_agency(connection, row_id):
    cursor = connection.cursor()
    query = "SELECT rss_link FROM news_agency WHERE id = %s"
    cursor.execute(query, (row_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def insert_news_items(connection, news_items, agency_id):
    cursor = connection.cursor()
    query = "INSERT INTO news (agency_id, news_link, news_title) VALUES (%s, %s, %s)"
    try:
        for item in news_items:
            cursor.execute(query, (agency_id, item['link'], item['title']))
        connection.commit()
        print(f"{cursor.rowcount} records inserted successfully")
    except Error as err:
        print(f"Error: '{err}'")

if __name__ == "__main__":
    connection = connect_to_database("localhost", "user", "password", "news_db")
    create_news_table(connection)
    rss_link = fetch_agency(connection, 3) 
    if rss_link:
        news_items = parse_rss(rss_link)
        insert_news_items(connection, news_items, 3)
    connection.close()
