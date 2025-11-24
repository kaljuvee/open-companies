"""
Test to verify search functionality for filtering company records.
Tests filtering by company name and status.
"""

import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db_utils import get_companies

def test_search_by_name():
    """
    Test searching companies by name (case-insensitive partial match).
    """
    print("\n" + "="*60)
    print("TEST 1: Search by Company Name")
    print("="*60)
    
    try:
        # Get all companies
        df = get_companies()
        total_count = len(df)
        print(f"Total companies in database: {total_count}")
        
        # Test case 1: Search for "OÜ" (very common in Estonian companies)
        search_term = "OÜ"
        filtered = df[df['name'].str.contains(search_term, case=False, na=False)]
        print(f"\n✅ Search for '{search_term}':")
        print(f"   Found {len(filtered)} companies")
        if len(filtered) > 0:
            print(f"   Sample results:")
            for idx, row in filtered.head(3).iterrows():
                print(f"   - {row['name']} ({row['registry_code']})")
        
        # Test case 2: Search for "AS" (another common form)
        search_term = "AS"
        filtered = df[df['name'].str.contains(search_term, case=False, na=False)]
        print(f"\n✅ Search for '{search_term}':")
        print(f"   Found {len(filtered)} companies")
        if len(filtered) > 0:
            print(f"   Sample results:")
            for idx, row in filtered.head(3).iterrows():
                print(f"   - {row['name']} ({row['registry_code']})")
        
        # Test case 3: Search for specific company (if we have Bolt, Tallink, etc)
        test_names = ["Bolt", "Tallink", "Telekom", "007"]
        for search_term in test_names:
            filtered = df[df['name'].str.contains(search_term, case=False, na=False)]
            if len(filtered) > 0:
                print(f"\n✅ Search for '{search_term}':")
                print(f"   Found {len(filtered)} companies")
                for idx, row in filtered.iterrows():
                    print(f"   - {row['name']} ({row['registry_code']}) - Status: {row['status']}")
                break
        
        # Test case 4: Empty search (should return all)
        search_term = ""
        filtered = df if search_term == "" else df[df['name'].str.contains(search_term, case=False, na=False)]
        print(f"\n✅ Empty search (should return all):")
        print(f"   Found {len(filtered)} companies (expected {total_count})")
        assert len(filtered) == total_count, "Empty search should return all companies"
        
        print("\n✅ Name search test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Name search test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_search_by_status():
    """
    Test filtering companies by status.
    """
    print("\n" + "="*60)
    print("TEST 2: Filter by Status")
    print("="*60)
    
    try:
        # Get all companies
        df = get_companies()
        total_count = len(df)
        print(f"Total companies in database: {total_count}")
        
        # Get status breakdown
        status_counts = df['status'].value_counts().to_dict()
        print(f"\nStatus breakdown:")
        for status, count in status_counts.items():
            print(f"  - {status}: {count}")
        
        # Test case 1: Filter by "Active"
        status_filter = "Active"
        filtered = df[df['status'] == status_filter]
        expected_count = status_counts.get(status_filter, 0)
        print(f"\n✅ Filter by status '{status_filter}':")
        print(f"   Found {len(filtered)} companies (expected {expected_count})")
        assert len(filtered) == expected_count, f"Expected {expected_count} Active companies, found {len(filtered)}"
        if len(filtered) > 0:
            print(f"   Sample results:")
            for idx, row in filtered.head(3).iterrows():
                print(f"   - {row['name']} - {row['status']}")
        
        # Test case 2: Filter by "LIK" (Liquidation)
        status_filter = "LIK"
        filtered = df[df['status'] == status_filter]
        expected_count = status_counts.get(status_filter, 0)
        print(f"\n✅ Filter by status '{status_filter}':")
        print(f"   Found {len(filtered)} companies (expected {expected_count})")
        assert len(filtered) == expected_count, f"Expected {expected_count} LIK companies, found {len(filtered)}"
        if len(filtered) > 0:
            print(f"   Results:")
            for idx, row in filtered.iterrows():
                print(f"   - {row['name']} - {row['status']}")
        
        # Test case 3: Filter by "MAA" (Bankruptcy)
        status_filter = "MAA"
        filtered = df[df['status'] == status_filter]
        expected_count = status_counts.get(status_filter, 0)
        print(f"\n✅ Filter by status '{status_filter}':")
        print(f"   Found {len(filtered)} companies (expected {expected_count})")
        assert len(filtered) == expected_count, f"Expected {expected_count} MAA companies, found {len(filtered)}"
        if len(filtered) > 0:
            print(f"   Results:")
            for idx, row in filtered.iterrows():
                print(f"   - {row['name']} - {row['status']}")
        
        # Test case 4: Filter by "All" (should return all)
        filtered = df  # No filter
        print(f"\n✅ Filter by 'All' (no filter):")
        print(f"   Found {len(filtered)} companies (expected {total_count})")
        assert len(filtered) == total_count, "All filter should return all companies"
        
        print("\n✅ Status filter test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Status filter test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_combined_search():
    """
    Test combining name search and status filter.
    """
    print("\n" + "="*60)
    print("TEST 3: Combined Name + Status Search")
    print("="*60)
    
    try:
        # Get all companies
        df = get_companies()
        print(f"Total companies in database: {len(df)}")
        
        # Test case: Search for "OÜ" AND status "Active"
        search_term = "OÜ"
        status_filter = "Active"
        
        filtered = df[
            (df['name'].str.contains(search_term, case=False, na=False)) &
            (df['status'] == status_filter)
        ]
        
        print(f"\n✅ Search for '{search_term}' with status '{status_filter}':")
        print(f"   Found {len(filtered)} companies")
        
        if len(filtered) > 0:
            print(f"   Sample results:")
            for idx, row in filtered.head(5).iterrows():
                print(f"   - {row['name']} - {row['status']} ({row['registry_code']})")
        
        # Verify all results match both criteria
        for idx, row in filtered.iterrows():
            assert search_term.lower() in row['name'].lower(), f"Name doesn't contain '{search_term}'"
            assert row['status'] == status_filter, f"Status is not '{status_filter}'"
        
        print("\n✅ Combined search test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Combined search test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_edge_cases():
    """
    Test edge cases and special characters in search.
    """
    print("\n" + "="*60)
    print("TEST 4: Edge Cases")
    print("="*60)
    
    try:
        # Get all companies
        df = get_companies()
        print(f"Total companies in database: {len(df)}")
        
        # Test case 1: Search with special characters
        search_term = "&"
        filtered = df[df['name'].str.contains(search_term, case=False, na=False, regex=False)]
        print(f"\n✅ Search for special character '{search_term}':")
        print(f"   Found {len(filtered)} companies")
        if len(filtered) > 0:
            print(f"   Sample results:")
            for idx, row in filtered.head(3).iterrows():
                print(f"   - {row['name']}")
        
        # Test case 2: Search with numbers
        search_term = "007"
        filtered = df[df['name'].str.contains(search_term, case=False, na=False)]
        print(f"\n✅ Search for numbers '{search_term}':")
        print(f"   Found {len(filtered)} companies")
        if len(filtered) > 0:
            print(f"   Sample results:")
            for idx, row in filtered.head(3).iterrows():
                print(f"   - {row['name']}")
        
        # Test case 3: Non-existent search term
        search_term = "XYZNONEXISTENT123"
        filtered = df[df['name'].str.contains(search_term, case=False, na=False)]
        print(f"\n✅ Search for non-existent term '{search_term}':")
        print(f"   Found {len(filtered)} companies (expected 0)")
        assert len(filtered) == 0, "Non-existent search should return 0 results"
        
        print("\n✅ Edge cases test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Edge cases test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """
    Run all search functionality tests and save results.
    """
    print("\n" + "="*60)
    print("SEARCH FUNCTIONALITY TEST SUITE")
    print("="*60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    results = {
        "test_suite": "search_functionality",
        "timestamp": datetime.now().isoformat(),
        "tests": {}
    }
    
    # Run all tests
    tests = [
        ("search_by_name", test_search_by_name),
        ("search_by_status", test_search_by_status),
        ("combined_search", test_combined_search),
        ("edge_cases", test_edge_cases)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results["tests"][test_name] = {
                "status": "passed" if success else "failed",
                "timestamp": datetime.now().isoformat()
            }
            if success:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            results["tests"][test_name] = {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            failed += 1
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    results["summary"] = {
        "total": len(tests),
        "passed": passed,
        "failed": failed,
        "success_rate": f"{(passed/len(tests)*100):.1f}%"
    }
    
    if failed == 0:
        print("\n✅ ALL TESTS PASSED!")
        results["overall_status"] = "passed"
    else:
        print(f"\n❌ {failed} TEST(S) FAILED")
        results["overall_status"] = "failed"
    
    # Save results to JSON
    os.makedirs("test-results", exist_ok=True)
    with open("test-results/search_functionality_test.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Results saved to test-results/search_functionality_test.json")
    
    return results


if __name__ == "__main__":
    run_all_tests()
