"""
Quick import script using raw SQL for maximum speed.
"""

import os
import sys
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

def map_status(status_code):
    """Map Estonian status code to our schema."""
    status_map = {
        'R': 'Active',  # Registrisse kantud (Registered)
        'L': 'LIK',     # Likvideerimises (In liquidation)
        'M': 'MAA',     # Maksejõuetus (Bankruptcy)
        'K': 'Deleted', # Kustutatud (Deleted)
    }
    return status_map.get(status_code, 'Active')

def parse_date(date_str):
    """Parse date from Estonian format."""
    if pd.isna(date_str) or str(date_str).strip() == '':
        return None
    try:
        return datetime.strptime(str(date_str).strip(), '%d.%m.%Y')
    except:
        return None

def main(limit=1000):
    """Import companies using raw SQL."""
    
    csv_path = "/tmp/estonian_data/ettevotja_rekvisiidid__lihtandmed.csv"
    
    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        print("Please run data_ingestor.py first to download the file")
        return
    
    print(f"Reading CSV file...")
    df = pd.read_csv(csv_path, encoding='utf-8-sig', sep=';', low_memory=False)
    
    print(f"Total rows in CSV: {len(df)}")
    
    # Take only the rows we need
    df = df.head(limit)
    print(f"Processing {len(df)} rows")
    
    # Connect to database
    db_url = os.getenv('MAIN_DB_URL')
    if not db_url:
        raise ValueError("MAIN_DB_URL not set")
    
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    print("Preparing data...")
    
    # Prepare data for insert
    records = []
    for idx, row in df.iterrows():
        registry_code = str(row.get('ariregistri_kood', '')).strip()
        
        # Skip if already exists
        cur.execute("SELECT 1 FROM company.companies WHERE registry_code = %s", (registry_code,))
        if cur.fetchone():
            continue
        
        name = str(row.get('nimi', '')).strip() if pd.notna(row.get('nimi')) else None
        status_code = str(row.get('ettevotja_staatus', 'R')).strip()
        status = map_status(status_code)
        address = str(row.get('ettevotja_aadress', '')).strip() if pd.notna(row.get('ettevotja_aadress')) else None
        reg_date = parse_date(row.get('registri_kande_kuupaev'))
        
        records.append((
            registry_code,
            name,
            status,
            'EE',  # country_code
            address,
            reg_date,
            None,  # liquidation_date
            None,  # bankruptcy_date
        ))
        
        if len(records) % 100 == 0:
            print(f"Prepared {len(records)} records...")
    
    print(f"\nInserting {len(records)} new companies...")
    
    # Bulk insert
    insert_query = """
        INSERT INTO company.companies 
        (registry_code, name, status, country_code, address, registration_date, liquidation_date, bankruptcy_date)
        VALUES %s
        ON CONFLICT (registry_code) DO NOTHING
    """
    
    execute_values(cur, insert_query, records, page_size=500)
    conn.commit()
    
    print(f"✅ Successfully imported {len(records)} companies!")
    
    # Get final count
    cur.execute("SELECT COUNT(*) FROM company.companies")
    total = cur.fetchone()[0]
    print(f"Total companies in database: {total}")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    main(limit)
