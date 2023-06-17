""" Setup script for MySQL database table for the cognitive_science_society_scraper.py.
    Add a timestamp for the date inserted and date updated.
"""
import mysql.connector
from settings import (MYSQL_DB_NAME, MYSQL_HOST,
                      MYSQL_USER, MYSQL_PASSWORD,
                      COG_SS_TABLE
                      )

CONN = mysql.connector.connect(
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    database=MYSQL_DB_NAME
)

CURSOR = CONN.cursor()


create_main_table_query = f"""
CREATE TABLE IF NOT EXISTS {COG_SS_TABLE} (
    entry_id VARCHAR(255) NOT NULL PRIMARY KEY,
    date_inserted TIMESTAMP NULL,
    date_updated TIMESTAMP NULL,
    title VARCHAR(255),
    date_published TIMESTAMP,
    link VARCHAR(255),
    tags TEXT,
    full_text TEXT
);
"""
CURSOR.execute(create_main_table_query)

# Create trigger for date_inserted
create_trigger_insert = f"""
CREATE TRIGGER insert_{COG_SS_TABLE}_timestamp 
BEFORE INSERT ON {COG_SS_TABLE} 
FOR EACH ROW 
SET NEW.date_inserted = NOW();
"""
CURSOR.execute(create_trigger_insert)

# Create trigger for date_updated
create_trigger_update = f"""
CREATE TRIGGER update_{COG_SS_TABLE}_timestamp 
BEFORE UPDATE ON {COG_SS_TABLE} 
FOR EACH ROW 
SET NEW.date_updated = NOW();
"""
CURSOR.execute(create_trigger_update)


CONN.commit()
CONN.close()
