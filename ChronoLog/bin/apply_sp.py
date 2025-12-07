import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from db import SQLConnection

def apply_sp():
    try:
        db = SQLConnection()
    except Exception as e:
        print(f"Could not connect to DB: {e}")
        return
    
    # Read the updated SP definition from the file
    sql_path = os.path.join(os.path.dirname(__file__), '..', 'database', '02_stored_procedures.sql')
    with open(sql_path, 'r') as f:
        sql = f.read()
    
    # Extract sp_GetTimelinePage parts
    # The file has multiple GO statements. We need to split by GO and find the one for sp_GetTimelinePage
    statements = sql.split('GO')
    
    sp_drop = None
    sp_create = None
    
    for stmt in statements:
        if 'DROP PROCEDURE [dbo].[sp_GetTimelinePage]' in stmt:
            sp_drop = stmt.strip()
        if 'CREATE PROCEDURE [dbo].[sp_GetTimelinePage]' in stmt:
            sp_create = stmt.strip()
            # Ensure it doesn't end with PRINT or similar if split by GO included it (GO is separator)
    
    if sp_drop and sp_create:
        print("Applying SP update...")
        try:
            if sp_drop:
                db.execute_non_query(sp_drop)
                print("Dropped old SP.")
            if sp_create:
                db.execute_non_query(sp_create)
                print("Created new SP.")
        except Exception as e:
            print(f"Error applying SP: {e}")
    else:
        print("Could not find SP definition in file.")

if __name__ == "__main__":
    apply_sp()
