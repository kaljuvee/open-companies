"""Database utility functions for PostgreSQL connection and operations."""

import os
from typing import Optional, List, Dict, Any
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_db_engine() -> Engine:
    """Create and return a SQLAlchemy engine for database connections."""
    db_url = os.getenv('MAIN_DB_URL')
    if not db_url:
        raise ValueError("MAIN_DB_URL environment variable is not set")
    
    # Add SSL requirement for production databases
    if 'render.com' in db_url or 'amazonaws.com' in db_url:
        if '?' in db_url:
            db_url += '&sslmode=require'
        else:
            db_url += '?sslmode=require'
    
    return create_engine(db_url)


def execute_sql(query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """
    Execute a SQL query and return results as a pandas DataFrame.
    
    Args:
        query: SQL query string
        params: Optional dictionary of query parameters
        
    Returns:
        DataFrame with query results
    """
    engine = get_db_engine()
    try:
        with engine.connect() as conn:
            if params:
                result = pd.read_sql(text(query), conn, params=params)
            else:
                result = pd.read_sql(text(query), conn)
        return result
    except Exception as e:
        raise Exception(f"Database query failed: {str(e)}")


def execute_sql_write(query: str, params: Optional[Dict[str, Any]] = None) -> int:
    """
    Execute a SQL write operation (INSERT, UPDATE, DELETE).
    
    Args:
        query: SQL query string
        params: Optional dictionary of query parameters
        
    Returns:
        Number of rows affected
    """
    engine = get_db_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            conn.commit()
            return result.rowcount
    except Exception as e:
        raise Exception(f"Database write operation failed: {str(e)}")


def insert_company(data: Dict[str, Any]) -> int:
    """
    Insert a company record into the database.
    
    Args:
        data: Dictionary containing company data
        
    Returns:
        ID of inserted company
    """
    query = """
    INSERT INTO company.companies 
    (registry_code, name, status, country_code, address, registration_date, liquidation_date, bankruptcy_date)
    VALUES (:registry_code, :name, :status, :country_code, :address, :registration_date, :liquidation_date, :bankruptcy_date)
    ON CONFLICT (registry_code) 
    DO UPDATE SET 
        name = EXCLUDED.name,
        status = EXCLUDED.status,
        address = EXCLUDED.address,
        liquidation_date = EXCLUDED.liquidation_date,
        bankruptcy_date = EXCLUDED.bankruptcy_date,
        updated_at = CURRENT_TIMESTAMP
    RETURNING id
    """
    
    engine = get_db_engine()
    with engine.connect() as conn:
        result = conn.execute(text(query), data)
        conn.commit()
        return result.fetchone()[0]


def get_companies(status: Optional[str] = None, country_code: str = 'EE') -> pd.DataFrame:
    """
    Retrieve companies from the database.
    
    Args:
        status: Optional status filter (e.g., 'LIK', 'MAA')
        country_code: Country code filter (default: 'EE')
        
    Returns:
        DataFrame with company data
    """
    query = "SELECT * FROM company.companies WHERE country_code = :country_code"
    params = {'country_code': country_code}
    
    if status:
        query += " AND status = :status"
        params['status'] = status
    
    query += " ORDER BY created_at DESC"
    
    return execute_sql(query, params)


def insert_statistics(country_code: str, stat_type: str, stat_date: str, count: int, metadata: Optional[Dict] = None):
    """
    Insert or update statistics record.
    
    Args:
        country_code: Country code (e.g., 'EE')
        stat_type: Type of statistic (e.g., 'deletions', 'formations')
        stat_date: Date of the statistic
        count: Count value
        metadata: Optional additional metadata as JSON
    """
    query = """
    INSERT INTO company.statistics (country_code, stat_type, stat_date, count, metadata)
    VALUES (:country_code, :stat_type, :stat_date, :count, :metadata)
    ON CONFLICT (country_code, stat_type, stat_date)
    DO UPDATE SET 
        count = EXCLUDED.count,
        metadata = EXCLUDED.metadata,
        created_at = CURRENT_TIMESTAMP
    """
    
    import json
    params = {
        'country_code': country_code,
        'stat_type': stat_type,
        'stat_date': stat_date,
        'count': count,
        'metadata': json.dumps(metadata) if metadata else None
    }
    
    execute_sql_write(query, params)


def test_connection() -> bool:
    """Test database connection."""
    try:
        engine = get_db_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Connection test failed: {str(e)}")
        return False
