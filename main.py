import mysql.connector
import pandas as pd

# Connect to the MySQL container
db = mysql.connector.connect(
    host="localhost",
    port=3306,  # Explicitly defining the port
    user="user",
    password="password",
    database="news_db"
)


cursor = db.cursor()

# Create table for news agency
cursor.execute('''
CREATE TABLE IF NOT EXISTS news_agency (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    rss_link VARCHAR(255) NOT NULL
)
''')

def add_news_agency(name, rss_link):
    """
    Adds a news agency and its RSS link to the database.
    """
    if pd.isna(name) or pd.isna(rss_link):
        print("Skipping entry due to NaN values.")
        return
    query = "INSERT INTO news_agency (name, rss_link) VALUES (%s, %s)"
    values = (name, rss_link)
    cursor.execute(query, values)
    db.commit()
    print(f"Added {name} with RSS link {rss_link}")

df = pd.read_csv('./News Agencies.csv')

if __name__ == "__main__":
    for index, row in df.iterrows():
        add_news_agency(row['name'], row['link'])