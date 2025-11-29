import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from db import SQLConnection

def drop_tables():
    print("Dropping tables...")
    db = SQLConnection()
    conn = db.get_connection()
    cursor = conn.cursor()

    try:
        # Drop TimelineEvents first (referencing table)
        print("Dropping TimelineEvents...")
        cursor.execute("IF OBJECT_ID('dbo.TimelineEvents', 'U') IS NOT NULL DROP TABLE dbo.TimelineEvents")
        
        # Drop Messages (referenced table)
        print("Dropping Messages...")
        cursor.execute("IF OBJECT_ID('dbo.Messages', 'U') IS NOT NULL DROP TABLE dbo.Messages")
        
        conn.commit()
        print("Tables dropped successfully.")
    except Exception as e:
        print(f"Error dropping tables: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    drop_tables()
