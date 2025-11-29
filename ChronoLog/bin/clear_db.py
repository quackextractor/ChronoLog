import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from db import SQLConnection

def clear_db():
    print("Clearing database...")
    db = SQLConnection()
    conn = db.get_connection()
    cursor = conn.cursor()

    try:
        # Truncate TimelineEvents first (referencing table)
        print("Truncating TimelineEvents...")
        cursor.execute("TRUNCATE TABLE TimelineEvents")
        
        # Delete from Messages (referenced table) - TRUNCATE fails with FKs
        print("Deleting from Messages...")
        cursor.execute("DELETE FROM Messages")
        
        # Reset Identity for Messages
        print("Reseting Messages identity...")
        cursor.execute("DBCC CHECKIDENT ('Messages', RESEED, 0)")
        
        conn.commit()
        print("Database cleared successfully.")
    except Exception as e:
        print(f"Error clearing database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    confirm = input("Are you sure you want to delete ALL data? (y/n): ")
    if confirm.lower() == 'y':
        clear_db()
    else:
        print("Operation cancelled.")
