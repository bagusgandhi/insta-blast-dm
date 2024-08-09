import sqlite3
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

DB = os.getenv('DB')

def get_db_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn