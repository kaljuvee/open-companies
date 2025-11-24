"""
Fast batch import script for Estonian company data.
Uses SQLAlchemy bulk operations for much faster imports.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_ingestor import EstonianDataIngestor

def main():
    """Run fast batch import."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Fast import Estonian company data')
    parser.add_argument('limit', type=int, nargs='?', default=1000, 
                       help='Number of companies to import (default: 1000)')
    
    args = parser.parse_args()
    
    print(f"Starting fast import of {args.limit} companies...")
    
    ingestor = EstonianDataIngestor()
    
    try:
        # Download and parse
        csv_path = ingestor.download_data()
        companies = ingestor.parse_csv(csv_path, limit=args.limit)
        
        print(f"\nParsed {len(companies)} companies")
        print("Starting bulk import...")
        
        # Use bulk import
        imported = ingestor.bulk_import_companies(companies)
        
        print(f"\n✅ Successfully imported {imported} companies!")
        
    except Exception as e:
        print(f"\n❌ Error during import: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
