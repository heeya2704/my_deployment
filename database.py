import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "ml_database")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))


def get_db_connection():
    """Establish and return a connection to the configured MySQL database."""
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        port=MYSQL_PORT
    )


def init_db():
    """Ensure database and predictions table exist in MySQL."""
    # First connect to server without selecting database
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        port=MYSQL_PORT
    )
    cursor = conn.cursor()
    
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DATABASE}`")
    conn.commit()
    cursor.close()
    conn.close()

    # Now connect to ml_database and create predictions table
    db_conn = get_db_connection()
    db_cursor = db_conn.cursor()
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS predictions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        study_hours FLOAT NOT NULL,
        prediction FLOAT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    db_cursor.execute(create_table_query)
    db_conn.commit()
    db_cursor.close()
    db_conn.close()


def insert_prediction(study_hours: float, prediction: float) -> dict:
    """Insert a new prediction record into MySQL table and return record details."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    INSERT INTO predictions (study_hours, prediction)
    VALUES (%s, %s)
    """
    cursor.execute(query, (study_hours, prediction))
    conn.commit()
    
    record_id = cursor.lastrowid
    
    # Retrieve created record
    select_query = "SELECT id, study_hours, prediction, created_at FROM predictions WHERE id = %s"
    cursor.execute(select_query, (record_id,))
    record = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if record and "created_at" in record and record["created_at"]:
        record["created_at"] = str(record["created_at"])
        
    return record


def get_all_predictions() -> list:
    """Retrieve all predictions stored in MySQL database."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT id, study_hours, prediction, created_at FROM predictions ORDER BY id ASC"
    cursor.execute(query)
    records = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    for row in records:
        if "created_at" in row and row["created_at"]:
            row["created_at"] = str(row["created_at"])
            
    return records
