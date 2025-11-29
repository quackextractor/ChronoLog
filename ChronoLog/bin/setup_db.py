import sys
import os
import re

# Add src to path to import db
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from db import SQLConnection
except ImportError as e:
    print(f"Error: Could not import src.db. Exception: {e}")
    sys.exit(1)

def run_sql_file(conn, file_path):
    print(f"Executing {os.path.basename(file_path)}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Split by GO command (case insensitive, on its own line)
    # SQL Server tools often use GO as a batch separator, but pyodbc doesn't understand it.
    batches = re.split(r'^\s*GO\s*$', sql_content, flags=re.MULTILINE | re.IGNORECASE)

    cursor = conn.cursor()
    for batch in batches:
        batch = batch.strip()
        if not batch:
            continue
        try:
            cursor.execute(batch)
            conn.commit()
        except Exception as e:
            print(f"Error executing batch in {file_path}: {e}")
            # Optional: decide whether to stop or continue. 
            # For now, we print and continue, but in production you might want to stop.
            # However, some "Errors" might be "Object already exists" which we want to ignore if not handled in SQL.
            # The SQL scripts provided seem to check for existence, so real errors should be reported.

def main():
    print("Starting database setup...")
    
    try:
        db = SQLConnection()
        conn = db.get_connection()
        conn.autocommit = True
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        print("Check your .env file and ensure SQL Server is running.")
        sys.exit(1)

    # Define order of scripts
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'database')
    files = [
        "01_create_tables.sql",
        "02_stored_procedures.sql",
        "03_views.sql",
        "04_sample_data.sql"
    ]

    for filename in files:
        path = os.path.join(base_dir, filename)
        if os.path.exists(path):
            run_sql_file(conn, path)
        else:
            print(f"Warning: File {filename} not found at {path}")

    print("Database setup complete.")
    conn.close()

if __name__ == "__main__":
    main()
