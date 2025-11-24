"""
Test to verify the count of records in the database.
"""

import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db_utils import get_companies

def test_record_count():
    """
    Test to verify the number of companies in the database.
    """
    print("Testing database record count...")
    
    try:
        # Get all companies
        df = get_companies()
        
        # Count total records
        total_count = len(df)
        print(f"✅ Total companies in database: {total_count}")
        
        # Count by status
        status_counts = df['status'].value_counts().to_dict()
        print(f"\n📊 Breakdown by status:")
        for status, count in status_counts.items():
            percentage = (count / total_count * 100) if total_count > 0 else 0
            print(f"  - {status}: {count} ({percentage:.1f}%)")
        
        # Verify minimum count (should have at least the 100 we imported)
        assert total_count >= 100, f"Expected at least 100 companies, found {total_count}"
        print(f"\n✅ Record count test passed! Database has {total_count} companies.")
        
        # Save results to JSON
        results = {
            "test": "database_record_count",
            "timestamp": datetime.now().isoformat(),
            "status": "passed",
            "total_companies": total_count,
            "breakdown": status_counts,
            "message": f"Database contains {total_count} companies"
        }
        
        # Create test-results directory if it doesn't exist
        os.makedirs("test-results", exist_ok=True)
        
        # Save results
        with open("test-results/record_count_test.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Results saved to test-results/record_count_test.json")
        
        return results
        
    except Exception as e:
        print(f"❌ Error during record count test: {e}")
        import traceback
        traceback.print_exc()
        
        # Save error results
        results = {
            "test": "database_record_count",
            "timestamp": datetime.now().isoformat(),
            "status": "failed",
            "error": str(e)
        }
        
        os.makedirs("test-results", exist_ok=True)
        with open("test-results/record_count_test.json", "w") as f:
            json.dump(results, f, indent=2)
        
        raise


if __name__ == "__main__":
    test_record_count()
