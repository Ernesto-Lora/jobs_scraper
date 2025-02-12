# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2
import psycopg2.extras
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
    
def clean_list(text_list):
    """Removes '\r\n' items and replaces '\xa0' with a space in all text elements."""
    return [text.replace("\xa0", " ") for text in text_list if text != '\r\n']

def list_to_string(cleaned_list, separator="-"):
    """Joins the cleaned list into a single string with a given separator."""
    return separator.join(cleaned_list)

from scrapy.exceptions import CloseSpider

class JobsPipeline:
    def open_spider(self, spider):
        # Connect to the PostgreSQL database
        self.connection = psycopg2.connect(
            dbname=spider.settings.get('DATABASE')['database'],
            user=spider.settings.get('DATABASE')['username'],
            password=spider.settings.get('DATABASE')['password'],
            host=spider.settings.get('DATABASE')['host'],
            port=spider.settings.get('DATABASE')['port'],
        )
        self.connection.autocommit = False  # Ensure transactions are manually committed
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Create the table if it doesn't exist
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id SERIAL PRIMARY KEY,
                    job_title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    salary VARCHAR(100),
                    requirements TEXT,
                    benefits TEXT,
                    location TEXT,
                    business_name TEXT
                )
            """)
            self.connection.commit()
        except Exception as e:
            spider.logger.error(f"Error creating table: {e}")
            self.connection.rollback()

    def close_spider(self, spider):
        # Close the database connection
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        try:
            # Check if the job already exists in the database
            self.cursor.execute("""
                SELECT id FROM jobs 
                WHERE job_title = %s AND business_name = %s AND location = %s
            """, (
                item['job_title'],
                item['business_name'],
                item['location'],
            ))
            existing_job = self.cursor.fetchone()
            
            if existing_job:
                spider.logger.info(f"Duplicate job found: {item['job_title']} at {item['business_name']} in {item['location']}. Stopping spider.")
                # Stop the spider immediately
                spider.crawler.engine.close_spider(spider, 'duplicate_job_found')
                return item  # Return the item to avoid further processing
            
            # Insert the item into the database if it doesn't exist
            self.cursor.execute("""
                INSERT INTO jobs (job_title, description, salary, requirements, benefits, location, business_name)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                item['job_title'],
                list_to_string(item['description']),
                item['salary'],
                list_to_string(item['requirements']),
                list_to_string(item['benefits']),
                item['location'],
                item['business_name'],
            ))
            self.connection.commit()
        except psycopg2.Error as e:
            spider.logger.error(f"Database error: {e}")
            self.connection.rollback()  # Rollback the transaction to prevent blocking other queries
        except Exception as e:
            spider.logger.error(f"Unexpected error: {e}")
            self.connection.rollback()
        return item
