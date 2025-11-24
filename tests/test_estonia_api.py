"""Test script for Estonia API integration."""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.estonia_api import EstoniaAPI, test_api_connection

def main():
    """Run Estonia API tests."""
    results = {
        "test_name": "Estonia API Integration Test",
        "timestamp": datetime.now().isoformat(),
        "tests": []
    }
    
    print("=" * 60)
    print("Testing Estonia API Integration")
    print("=" * 60)
    
    # Test 1: API Connection
    print("\n1. Testing API Connection...")
    try:
        connection_ok = test_api_connection()
        results["tests"].append({
            "name": "API Connection",
            "status": "PASS" if connection_ok else "FAIL",
            "message": "API connection successful" if connection_ok else "API connection failed"
        })
        print(f"   {'✓' if connection_ok else '✗'} API Connection")
    except Exception as e:
        results["tests"].append({
            "name": "API Connection",
            "status": "ERROR",
            "message": str(e)
        })
        print(f"   ✗ API Connection Error: {e}")
    
    # Test 2: Get Company Details
    print("\n2. Testing Get Company Details...")
    try:
        api = EstoniaAPI()
        response = api.get_company_details('14854757')  # Test with known company
        
        has_data = 'keha' in response or 'ettevotjad' in str(response)
        results["tests"].append({
            "name": "Get Company Details",
            "status": "PASS" if has_data else "FAIL",
            "message": "Retrieved company details" if has_data else "No data returned",
            "sample_data": str(response)[:200] if has_data else None
        })
        print(f"   {'✓' if has_data else '✗'} Get Company Details")
    except Exception as e:
        results["tests"].append({
            "name": "Get Company Details",
            "status": "ERROR",
            "message": str(e)
        })
        print(f"   ✗ Get Company Details Error: {e}")
    
    # Test 3: Get Liquidations
    print("\n3. Testing Get Liquidations...")
    try:
        api = EstoniaAPI()
        liquidations = api.get_liquidations(limit=5)
        
        has_liquidations = len(liquidations) > 0
        results["tests"].append({
            "name": "Get Liquidations",
            "status": "PASS" if has_liquidations else "WARNING",
            "message": f"Retrieved {len(liquidations)} liquidation records",
            "sample_data": liquidations[:2] if has_liquidations else None
        })
        print(f"   {'✓' if has_liquidations else '⚠'} Get Liquidations ({len(liquidations)} records)")
    except Exception as e:
        results["tests"].append({
            "name": "Get Liquidations",
            "status": "ERROR",
            "message": str(e)
        })
        print(f"   ✗ Get Liquidations Error: {e}")
    
    # Test 4: Get Bankruptcies
    print("\n4. Testing Get Bankruptcies...")
    try:
        api = EstoniaAPI()
        bankruptcies = api.get_bankruptcies(limit=5)
        
        has_bankruptcies = len(bankruptcies) > 0
        results["tests"].append({
            "name": "Get Bankruptcies",
            "status": "PASS" if has_bankruptcies else "WARNING",
            "message": f"Retrieved {len(bankruptcies)} bankruptcy records",
            "sample_data": bankruptcies[:2] if has_bankruptcies else None
        })
        print(f"   {'✓' if has_bankruptcies else '⚠'} Get Bankruptcies ({len(bankruptcies)} records)")
    except Exception as e:
        results["tests"].append({
            "name": "Get Bankruptcies",
            "status": "ERROR",
            "message": str(e)
        })
        print(f"   ✗ Get Bankruptcies Error: {e}")
    
    # Test 5: Search Companies
    print("\n5. Testing Company Search...")
    try:
        api = EstoniaAPI()
        search_results = api.search_companies("OÜ", limit=5)
        
        has_results = len(search_results) > 0
        results["tests"].append({
            "name": "Company Search",
            "status": "PASS" if has_results else "WARNING",
            "message": f"Search returned {len(search_results)} results",
            "sample_data": search_results[:2] if has_results else None
        })
        print(f"   {'✓' if has_results else '⚠'} Company Search ({len(search_results)} results)")
    except Exception as e:
        results["tests"].append({
            "name": "Company Search",
            "status": "ERROR",
            "message": str(e)
        })
        print(f"   ✗ Company Search Error: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(1 for t in results["tests"] if t["status"] == "PASS")
    failed = sum(1 for t in results["tests"] if t["status"] == "FAIL")
    errors = sum(1 for t in results["tests"] if t["status"] == "ERROR")
    warnings = sum(1 for t in results["tests"] if t["status"] == "WARNING")
    
    print(f"Test Summary: {passed} passed, {failed} failed, {errors} errors, {warnings} warnings")
    print("=" * 60)
    
    # Save results
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test-results")
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "estonia_api_test.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    
    return results

if __name__ == "__main__":
    main()
