import mysql.connector
from config import db_config,app_logger


def connect_to_database():
    """Establish a connection to the database."""
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        app_logger.info("Database connection successful.")
        return connection
    except mysql.connector.Error as err:
        app_logger.error(f"Database connection failed: {err}")
        return None


def create_table(connection, query):
    """Generic function to create a table based on provided SQL query."""
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        app_logger.info("Table created successfully.")
    except mysql.connector.Error as err:
        app_logger.error(f"Failed to create table: {err}")
    finally:
        cursor.close()


def insert_news_items(connection, news_items, agency_id):
    """Insert news items into the 'news' table."""
    query = """
    INSERT INTO news (agency_id, news_link, news_title)
    VALUES (%s, %s, %s)
    """
    try:
        cursor = connection.cursor()
        data_tuples = [(agency_id, item['link'], item['title']) for item in news_items]
        cursor.executemany(query, data_tuples)
        connection.commit()
        app_logger.info(f"{cursor.rowcount} records inserted successfully into the news table.")
    except mysql.connector.Error as err:
        app_logger.error(f"Failed to insert records into MySQL table: {err}")
    finally:
        cursor.close()



def insert_news_agency(connection, name, rss_link):
    """Insert a new agency into the 'news_agency' table."""
    try:
        cursor = connection.cursor()
        query = "INSERT INTO news_agency (name, rss_link) VALUES (%s, %s)"
        cursor.execute(query, (name, rss_link))
        connection.commit()
        agency_id = cursor.lastrowid
        app_logger.info(f"Added {name} with RSS link {rss_link} and ID {agency_id}")
        return agency_id
    except mysql.connector.Error as err:
        app_logger.error(f"Failed to insert news agency: {err}")
    finally:
        cursor.close()
def setup_database():
    db = connect_to_database()
    if db:
        create_table(db, '''
            CREATE TABLE IF NOT EXISTS news_agency (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                rss_link VARCHAR(255) NOT NULL
            )
        ''')
        create_table(db, '''
            CREATE TABLE IF NOT EXISTS news (
                id INT AUTO_INCREMENT PRIMARY KEY,
                agency_id INT,
                news_link VARCHAR(1023),
                news_title VARCHAR(255),
                crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (agency_id) REFERENCES news_agency(id)
            )
        ''')
    return db
