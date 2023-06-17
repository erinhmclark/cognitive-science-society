"""  """
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
    updated TIMESTAMP,
    title VARCHAR(255),
    date_published TIMESTAMP,
    link VARCHAR(255),
    tags TEXT,
    full_text TEXT
);
"""
CURSOR.execute(create_main_table_query)


CONN.commit()
CONN.close()
