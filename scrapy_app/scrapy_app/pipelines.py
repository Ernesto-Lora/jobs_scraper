# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2
from scrapy.exceptions import DropItem

class PostgresPipeline:
    def open_spider(self, spider):
        # Connect to the PostgreSQL database
        self.connection = psycopg2.connect(
            dbname=spider.settings.get('DATABASE')['database'],
            user=spider.settings.get('DATABASE')['username'],
            password=spider.settings.get('DATABASE')['password'],
            host=spider.settings.get('DATABASE')['host'],
            port=spider.settings.get('DATABASE')['port'],
        )
        self.cursor = self.connection.cursor()

        # Create the table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS quotes (
                id SERIAL PRIMARY KEY,
                text TEXT NOT NULL,
                author TEXT NOT NULL,
                tags TEXT[]
            )
        """)
        self.connection.commit()

    def close_spider(self, spider):
        # Close the database connection
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        # Insert the item into the database
        self.cursor.execute("""
            INSERT INTO quotes (text, author, tags)
            VALUES (%s, %s, %s)
        """, (
            item['text'],
            item['author'],
            item['tags'],
        ))
        self.connection.commit()
        return item