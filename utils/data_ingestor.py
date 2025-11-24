"""
Data Ingestor for Estonian Company Registry
Downloads CSV files from the Estonian open data portal and imports them into the database.
"""

import os
import requests
import zipfile
import csv
import io
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd
from sqlalchemy import create_engine, text
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.db_utils import get_db_engine, insert_company

# URLs for Estonian open data CSV files
BASIC_DATA_CSV_URL = "https://avaandmed.ariregister.rik.ee/sites/default/files/avaandmed/ettevotja_rekvisiidid__lihtandmed.csv.zip"

class EstonianDataIngestor:
    """
    Downloads and imports Estonian company data from the open data portal.
    """
    
    def __init__(self):
        """Initialize the data ingestor."""
        self.engine = get_db_engine()
        self.download_dir = "/tmp/estonian_data"
        os.makedirs(self.download_dir, exist_ok=True)
    
    def download_csv_file(self, url: str, filename: str) -> str:
        """
        Download a ZIP file containing CSV data.
        
        Args:
            url: URL to download from
            filename: Name to save the file as
            
        Returns:
            Path to the extracted CSV file
        """
        print(f"Downloading {filename}...")
        
        # Download the ZIP file
        response = requests.get(url, stream=True, timeout=120)
        response.raise_for_status()
        
        zip_path = os.path.join(self.download_dir, f"{filename}.zip")
        
        # Save ZIP file
        total_size = 0
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                total_size += len(chunk)
        
        print(f"Downloaded {filename}.zip ({total_size / 1024 / 1024:.1f} MB)")
        
        # Extract ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.download_dir)
        
        # Find the CSV file
        csv_files = [f for f in os.listdir(self.download_dir) if f.endswith('.csv')]
        if not csv_files:
            raise FileNotFoundError("No CSV file found in the ZIP archive")
        
        csv_path = os.path.join(self.download_dir, csv_files[0])
        print(f"Extracted to {csv_path}")
        
        return csv_path
    
    def parse_basic_data_csv(self, csv_path: str, limit: Optional[int] = None) -> List[Dict]:
        """
        Parse the basic data CSV file.
        
        Args:
            csv_path: Path to the CSV file
            limit: Optional limit on number of rows to process
            
        Returns:
            List of company dictionaries
        """
        print(f"Parsing CSV file: {csv_path}")
        
        companies = []
        
        # Read CSV with proper encoding (Estonian files typically use UTF-8 with BOM or Windows-1252)
        encodings_to_try = ['utf-8-sig', 'utf-8', 'windows-1252', 'iso-8859-1']
        
        df = None
        for encoding in encodings_to_try:
            try:
                df = pd.read_csv(
                    csv_path, 
                    encoding=encoding, 
                    sep=';',  # Estonian CSVs use semicolon
                    on_bad_lines='warn',  # Warn about malformed lines but continue
                    low_memory=False
                )
                print(f"Successfully read CSV with encoding: {encoding}")
                break
            except Exception as e:
                print(f"Failed to read with encoding {encoding}: {e}")
                continue
        
        if df is None:
            raise ValueError("Could not read CSV file with any supported encoding")
        
        print(f"CSV columns: {list(df.columns)}")
        print(f"Total rows: {len(df)}")
        
        # Apply limit if specified
        if limit:
            df = df.head(limit)
            print(f"Processing first {limit} rows")
        
        # Map CSV columns to our database schema
        # Estonian CSV columns:
        # - nimi (name)
        # - ariregistri_kood (registry code)
        # - ettevotja_staatus (status code: R=registered, L=liquidation, etc)
        # - ettevotja_staatus_tekstina (status text)
        # - ettevotja_aadress (address)
        # - ettevotja_esmakande_kpv (registration date)
        
        for idx, row in df.iterrows():
            try:
                # Extract and clean data
                status_code = str(row.get('ettevotja_staatus', 'R')).strip()
                status_text = str(row.get('ettevotja_staatus_tekstina', '')).strip()
                
                company_data = {
                    'registry_code': str(row.get('ariregistri_kood', '')).strip(),
                    'name': str(row.get('nimi', '')).strip(),
                    'status': self._map_status(status_code, status_text),
                    'country_code': 'EE',
                    'address': str(row.get('ads_normaliseeritud_taisaadress', row.get('ettevotja_aadress', ''))).strip() if pd.notna(row.get('ads_normaliseeritud_taisaadress', row.get('ettevotja_aadress'))) else None,
                    'registration_date': self._parse_date(row.get('ettevotja_esmakande_kpv')),
                    'liquidation_date': None,  # Not in basic data CSV
                    'bankruptcy_date': None,  # Not in basic data CSV
                }
                
                # Skip if no registry code
                if not company_data['registry_code'] or company_data['registry_code'] == 'nan':
                    continue
                
                companies.append(company_data)
                
                if (idx + 1) % 1000 == 0:
                    print(f"Processed {idx + 1} rows...")
                    
            except Exception as e:
                print(f"Error processing row {idx}: {e}")
                continue
        
        print(f"Successfully parsed {len(companies)} companies")
        return companies
    
    def _map_status(self, status_code: str, status_text: str = '') -> str:
        """
        Map Estonian status to our standard status codes.
        
        Args:
            status_code: Status code from CSV (R, L, M, K, etc)
            status_text: Status text from CSV
            
        Returns:
            Mapped status code
        """
        code = status_code.upper().strip()
        text_lower = status_text.lower().strip()
        
        # Estonian status code mappings
        # R = Registrisse kantud (Registered/Active)
        # L = Likvideerimises (In Liquidation)
        # M = Maksejõuetus (Bankruptcy)
        # K = Kustutatud (Deleted)
        
        if code == 'L' or 'likvideerimine' in text_lower:
            return 'LIK'
        elif code == 'M' or 'pankrot' in text_lower or 'maksejõuetus' in text_lower:
            return 'MAA'
        elif code == 'K' or 'kustutatud' in text_lower:
            return 'Deleted'
        else:
            return 'Active'
    
    def _parse_date(self, date_value) -> Optional[datetime]:
        """
        Parse date from various formats.
        
        Args:
            date_value: Date value from CSV
            
        Returns:
            Parsed datetime or None
        """
        if pd.isna(date_value) or date_value == '' or str(date_value).strip() == '':
            return None
        
        date_str = str(date_value).strip()
        
        # Try different date formats
        date_formats = [
            '%Y-%m-%d',
            '%d.%m.%Y',
            '%d/%m/%Y',
            '%Y-%m-%d %H:%M:%S',
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        print(f"Could not parse date: {date_value}")
        return None
    
    def bulk_import_companies(self, companies: List[Dict], batch_size: int = 500) -> int:
        """
        Import companies using bulk operations for much faster performance.
        
        Args:
            companies: List of company dictionaries
            batch_size: Number of companies to insert per batch
            
        Returns:
            Number of companies imported
        """
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        import os
        
        print(f"Bulk importing {len(companies)} companies into database...")
        
        db_url = os.getenv('MAIN_DB_URL')
        if not db_url:
            raise ValueError("MAIN_DB_URL environment variable not set")
        
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        imported_count = 0
        failed_count = 0
        
        try:
            for i in range(0, len(companies), batch_size):
                batch = companies[i:i + batch_size]
                
                try:
                    # Use bulk_insert_mappings for fast batch insert
                    session.bulk_insert_mappings(
                        type('companies', (), {}),  # Dummy class
                        batch,
                        render_nulls=True
                    )
                    session.commit()
                    imported_count += len(batch)
                    print(f"Imported batch {i//batch_size + 1}: {imported_count}/{len(companies)} companies")
                except Exception as e:
                    session.rollback()
                    print(f"Error importing batch {i//batch_size + 1}: {e}")
                    # Fall back to individual inserts for this batch
                    for company in batch:
                        try:
                            insert_company(company)
                            imported_count += 1
                        except Exception as e2:
                            print(f"Error importing company {company.get('registry_code')}: {e2}")
                            failed_count += 1
        finally:
            session.close()
        
        print(f"\nImport complete: {imported_count} succeeded, {failed_count} failed")
        return imported_count
    
    def import_companies(self, companies: List[Dict], batch_size: int = 100) -> int:
        """
        Import companies into the database using SQLAlchemy.
        
        Args:
            companies: List of company dictionaries
            batch_size: Number of companies to insert per batch
            
        Returns:
            Number of companies imported
        """
        print(f"Importing {len(companies)} companies into database...")
        
        imported_count = 0
        failed_count = 0
        
        for i in range(0, len(companies), batch_size):
            batch = companies[i:i + batch_size]
            
            for company in batch:
                try:
                    insert_company(company)
                    imported_count += 1
                except Exception as e:
                    print(f"Error importing company {company.get('registry_code')}: {e}")
                    failed_count += 1
            
            if (i + batch_size) % 1000 == 0:
                print(f"Imported {imported_count} companies so far...")
        
        print(f"Import complete: {imported_count} succeeded, {failed_count} failed")
        return imported_count
    
    def ingest_basic_data(self, limit: Optional[int] = None) -> int:
        """
        Download and import basic company data.
        
        Args:
            limit: Optional limit on number of companies to import
            
        Returns:
            Number of companies imported
        """
        print("Starting Estonian company data ingestion...")
        print(f"Limit: {limit if limit else 'No limit'}")
        
        # Download CSV file
        csv_path = self.download_csv_file(BASIC_DATA_CSV_URL, "basic_data")
        
        # Parse CSV
        companies = self.parse_basic_data_csv(csv_path, limit=limit)
        
        # Import into database
        imported_count = self.import_companies(companies)
        
        print(f"Ingestion complete! Imported {imported_count} companies")
        return imported_count


def main():
    """Main function to run the data ingestor."""
    import sys
    
    # Get limit from command line argument if provided
    limit = None
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
            print(f"Limiting import to {limit} companies")
        except ValueError:
            print(f"Invalid limit value: {sys.argv[1]}")
            sys.exit(1)
    
    # Create ingestor and run
    ingestor = EstonianDataIngestor()
    
    try:
        count = ingestor.ingest_basic_data(limit=limit)
        print(f"\n✅ Successfully imported {count} companies!")
    except Exception as e:
        print(f"\n❌ Error during ingestion: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
