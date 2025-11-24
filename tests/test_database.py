"""Test script for database connectivity and operations."""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db_utils import test_connection, execute_sql, get_db_engine

def main():
    """Run database tests."""
    results = {
        "test_name": "Database Connection Test",
        "timestamp": datetime.now().isoformat(),
        "tests": []
    }
    
    print("=" * 60)
    print("Testing Database Connection")
    print("=" * 60)
    
    # Test 1: Basic Connection
    print("\n1. Testing Database Connection...")
    try:
        connection_ok = test_connection()
        results["tests"].append({
            "name": "Database Connection",
            "status": "PASS" if connection_ok else "FAIL",
            "message": "Database connection successful" if connection_ok else "Database connection failed"
        })
        print(f"   {'✓' if connection_ok else '✗'} Database Connection")
    except Exception as e:
        results["tests"].append({
            "name": "Database Connection",
            "status": "ERROR",
            "message": str(e)
        })
        print(f"   ✗ Database Connection Error: {e}")
        # If connection fails, skip other tests
        save_results(results)
        return results
    
    # Test 2: Check if schema exists
    print("\n2. Testing Schema Existence...")
    try:
        query = """
        SELECT schema_name 
        FROM information_schema.schemata 
        WHERE schema_name = 'company'
        """
        result = execute_sql(query)
        
        schema_exists = len(result) > 0
        results["tests"].append({
            "name": "Schema Existence",
            "status": "PASS" if schema_exists else "WARNING",
            "message": "Schema 'company' exists" if schema_exists else "Schema 'company' not found - run SQL scripts to create"
        })
        print(f"   {'✓' if schema_exists else '⚠'} Schema Existence")
    except Exception as e:
        results["tests"].append({
            "name": "Schema Existence",
            "status": "ERROR",
            "message": str(e)
        })
        print(f"   ✗ Schema Existence Error: {e}")
    
    # Test 3: Check if tables exist
    print("\n3. Testing Table Existence...")
    try:
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'company'
        ORDER BY table_name
        """
        result = execute_sql(query)
        
        tables = result['table_name'].tolist() if not result.empty else []
        expected_tables = ['companies', 'ubos', 'events', 'statistics']
        
        all_exist = all(table in tables for table in expected_tables)
        
        results["tests"].append({
            "name": "Table Existence",
            "status": "PASS" if all_exist else "WARNING",
            "message": f"Found tables: {tables}" if tables else "No tables found - run SQL scripts to create",
            "expected_tables": expected_tables,
            "found_tables": tables
        })
        print(f"   {'✓' if all_exist else '⚠'} Table Existence (found: {len(tables)})")
    except Exception as e:
        results["tests"].append({
            "name": "Table Existence",
            "status": "ERROR",
            "message": str(e)
        })
        print(f"   ✗ Table Existence Error: {e}")
    
    # Test 4: Test query execution
    print("\n4. Testing Query Execution...")
    try:
        query = "SELECT 1 as test_column"
        result = execute_sql(query)
        
        query_ok = not result.empty and result.iloc[0]['test_column'] == 1
        results["tests"].append({
            "name": "Query Execution",
            "status": "PASS" if query_ok else "FAIL",
            "message": "Query execution successful" if query_ok else "Query execution failed"
        })
        print(f"   {'✓' if query_ok else '✗'} Query Execution")
    except Exception as e:
        results["tests"].append({
            "name": "Query Execution",
            "status": "ERROR",
            "message": str(e)
        })
        print(f"   ✗ Query Execution Error: {e}")
    
    # Test 5: Test data retrieval (if tables exist)
    print("\n5. Testing Data Retrieval...")
    try:
        query = """
        SELECT COUNT(*) as count 
        FROM information_schema.tables 
        WHERE table_schema = 'company' AND table_name = 'companies'
        """
        result = execute_sql(query)
        
        if not result.empty and result.iloc[0]['count'] > 0:
            # Table exists, try to query it
            data_query = "SELECT COUNT(*) as company_count FROM company.companies"
            data_result = execute_sql(data_query)
            
            count = data_result.iloc[0]['company_count'] if not data_result.empty else 0
            results["tests"].append({
                "name": "Data Retrieval",
                "status": "PASS",
                "message": f"Successfully retrieved data. Companies in database: {count}"
            })
            print(f"   ✓ Data Retrieval ({count} companies)")
        else:
            results["tests"].append({
                "name": "Data Retrieval",
                "status": "SKIP",
                "message": "Companies table does not exist yet"
            })
            print(f"   ⊘ Data Retrieval (table not found)")
    except Exception as e:
        results["tests"].append({
            "name": "Data Retrieval",
            "status": "ERROR",
            "message": str(e)
        })
        print(f"   ✗ Data Retrieval Error: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(1 for t in results["tests"] if t["status"] == "PASS")
    failed = sum(1 for t in results["tests"] if t["status"] == "FAIL")
    errors = sum(1 for t in results["tests"] if t["status"] == "ERROR")
    warnings = sum(1 for t in results["tests"] if t["status"] == "WARNING")
    skipped = sum(1 for t in results["tests"] if t["status"] == "SKIP")
    
    print(f"Test Summary: {passed} passed, {failed} failed, {errors} errors, {warnings} warnings, {skipped} skipped")
    print("=" * 60)
    
    # Save results
    save_results(results)
    
    return results

def save_results(results):
    """Save test results to JSON file."""
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test-results")
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "database_test.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    main()
