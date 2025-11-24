#!/usr/bin/env python3
"""
Populate database with test company data for demonstration
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db_utils import insert_company, test_connection

# Test company data
test_companies = [
    {
        'registry_code': '10560025',
        'name': 'AS Eesti Telekom',
        'status': 'Active',
        'country_code': 'EE',
        'address': 'Mustamäe tee 3, Tallinn 10621',
        'registration_date': datetime(1991, 7, 1),
        'liquidation_date': None,
        'bankruptcy_date': None
    },
    {
        'registry_code': '10747013',
        'name': 'Tallink Grupp AS',
        'status': 'Active',
        'country_code': 'EE',
        'address': 'Sadama 5/7, Tallinn 10111',
        'registration_date': datetime(2006, 5, 2),
        'liquidation_date': None,
        'bankruptcy_date': None
    },
    {
        'registry_code': '11065244',
        'name': 'Bolt Technology OÜ',
        'status': 'Active',
        'country_code': 'EE',
        'address': 'Vana-Lõuna 15, Tallinn 10134',
        'registration_date': datetime(2013, 3, 1),
        'liquidation_date': None,
        'bankruptcy_date': None
    },
    {
        'registry_code': '10123456',
        'name': 'Example Liquidation OÜ',
        'status': 'LIK',
        'country_code': 'EE',
        'address': 'Test Street 1, Tallinn 10111',
        'registration_date': datetime(2015, 1, 15),
        'liquidation_date': datetime(2024, 6, 1),
        'bankruptcy_date': None
    },
    {
        'registry_code': '10234567',
        'name': 'Sample Bankruptcy AS',
        'status': 'MAA',
        'country_code': 'EE',
        'address': 'Demo Road 2, Tartu 50001',
        'registration_date': datetime(2010, 3, 20),
        'liquidation_date': None,
        'bankruptcy_date': datetime(2024, 8, 15)
    },
    {
        'registry_code': '10345678',
        'name': 'Test Company OÜ',
        'status': 'Active',
        'country_code': 'EE',
        'address': 'Sample Avenue 3, Pärnu 80001',
        'registration_date': datetime(2018, 7, 10),
        'liquidation_date': None,
        'bankruptcy_date': None
    },
    {
        'registry_code': '10456789',
        'name': 'Demo Services AS',
        'status': 'Active',
        'country_code': 'EE',
        'address': 'Example Street 4, Narva 20001',
        'registration_date': datetime(2020, 2, 5),
        'liquidation_date': None,
        'bankruptcy_date': None
    },
    {
        'registry_code': '10567890',
        'name': 'Mock Trading OÜ',
        'status': 'LIK',
        'country_code': 'EE',
        'address': 'Test Boulevard 5, Tallinn 10112',
        'registration_date': datetime(2012, 11, 30),
        'liquidation_date': datetime(2024, 10, 1),
        'bankruptcy_date': None
    }
]

def main():
    """Populate database with test data"""
    print("Testing database connection...")
    if not test_connection():
        print("❌ Database connection failed!")
        return
    
    print("✅ Database connected")
    print(f"\nInserting {len(test_companies)} test companies...")
    
    success_count = 0
    for company in test_companies:
        try:
            insert_company(company)
            print(f"✅ Inserted: {company['name']} ({company['registry_code']})")
            success_count += 1
        except Exception as e:
            print(f"❌ Error inserting {company['name']}: {str(e)}")
    
    print(f"\n✅ Successfully inserted {success_count}/{len(test_companies)} companies")
    print("\nYou can now view this data by:")
    print("1. Go to EE Analytics page")
    print("2. Select 'Database' as data source")
    print("3. View the companies in the overview tab")

if __name__ == "__main__":
    main()
