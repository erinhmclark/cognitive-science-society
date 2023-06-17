import os

BASE_URL = "https://cognitivesciencesociety.org/blog/"

PAGE_LIMIT = 500
MYSQL_DB_NAME = 'cognitive_science_society'
COG_SS_TABLE = 'cognitive_ss_blog'
MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')

MYSQL_CONFIG = {
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'host': MYSQL_HOST,
    'database': MYSQL_DB_NAME,
    'raise_on_warnings': True
}
