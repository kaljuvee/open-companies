"""Test script for XAI API integration."""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.xai_utils import XAIAnalyzer, test_xai_connection

def main():
    """Run XAI API tests."""
    results = {
        "test_name": "XAI API Integration Test",
        "timestamp": datetime.now().isoformat(),
        "tests": []
    }
    
    print("=" * 60)
    print("Testing XAI API Integration")
    print("=" * 60)
    
    # Test 1: API Connection
    print("\n1. Testing XAI API Connection...")
    try:
        connection_ok = test_xai_connection()
        results["tests"].append({
            "name": "XAI API Connection",
            "status": "PASS" if connection_ok else "FAIL",
            "message": "XAI API connection successful" if connection_ok else "XAI API connection failed"
        })
        print(f"   {'✓' if connection_ok else '✗'} XAI API Connection")
        
        if not connection_ok:
            # If connection fails, skip other tests
            save_results(results)
            return results
    except Exception as e:
        results["tests"].append({
            "name": "XAI API Connection",
            "status": "ERROR",
            "message": str(e)
        })
        print(f"   ✗ XAI API Connection Error: {e}")
        save_results(results)
        return results
    
    # Test 2: Analyze Company Data
    print("\n2. Testing Company Data Analysis...")
    try:
        analyzer = XAIAnalyzer()
        test_company = {
            "name": "Test Company OÜ",
            "registry_code": "12345678",
            "status": "LIK",
            "address": "Tallinn, Estonia"
        }
        
        analysis = analyzer.analyze_company_data(test_company)
        
        has_analysis = len(analysis) > 0
        results["tests"].append({
            "name": "Company Data Analysis",
            "status": "PASS" if has_analysis else "FAIL",
            "message": "Analysis generated successfully" if has_analysis else "No analysis generated",
            "sample_output": analysis[:200] + "..." if len(analysis) > 200 else analysis
        })
        print(f"   {'✓' if has_analysis else '✗'} Company Data Analysis")
    except Exception as e:
        results["tests"].append({
            "name": "Company Data Analysis",
            "status": "ERROR",
            "message": str(e)
        })
        print(f"   ✗ Company Data Analysis Error: {e}")
    
    # Test 3: Extract Relevant Fields
    print("\n3. Testing Field Extraction...")
    try:
        analyzer = XAIAnalyzer()
        raw_data = {
            "name": "Sample Company",
            "registryCode": "11223344",
            "status": "Active",
            "address": "Test Street 123",
            "extraField1": "value1",
            "extraField2": "value2"
        }
        
        extraction = analyzer.extract_relevant_fields(raw_data, "company")
        
        has_extraction = 'analysis' in extraction
        results["tests"].append({
            "name": "Field Extraction",
            "status": "PASS" if has_extraction else "FAIL",
            "message": "Field extraction successful" if has_extraction else "Field extraction failed",
            "sample_output": str(extraction)[:200] + "..." if len(str(extraction)) > 200 else str(extraction)
        })
        print(f"   {'✓' if has_extraction else '✗'} Field Extraction")
    except Exception as e:
        results["tests"].append({
            "name": "Field Extraction",
            "status": "ERROR",
            "message": str(e)
        })
        print(f"   ✗ Field Extraction Error: {e}")
    
    # Test 4: Generate Insights
    print("\n4. Testing Insights Generation...")
    try:
        analyzer = XAIAnalyzer()
        test_data = [
            {"name": "Company A", "status": "LIK"},
            {"name": "Company B", "status": "MAA"},
            {"name": "Company C", "status": "Active"}
        ]
        
        insights = analyzer.generate_insights(
            test_data,
            "Analyze these Estonian companies and identify trends."
        )
        
        has_insights = len(insights) > 0
        results["tests"].append({
            "name": "Insights Generation",
            "status": "PASS" if has_insights else "FAIL",
            "message": "Insights generated successfully" if has_insights else "No insights generated",
            "sample_output": insights[:200] + "..." if len(insights) > 200 else insights
        })
        print(f"   {'✓' if has_insights else '✗'} Insights Generation")
    except Exception as e:
        results["tests"].append({
            "name": "Insights Generation",
            "status": "ERROR",
            "message": str(e)
        })
        print(f"   ✗ Insights Generation Error: {e}")
    
    # Test 5: Summarize Statistics
    print("\n5. Testing Statistics Summary...")
    try:
        analyzer = XAIAnalyzer()
        stats_data = [
            {"month": "January", "deletions": 45},
            {"month": "February", "deletions": 52},
            {"month": "March", "deletions": 38}
        ]
        
        summary = analyzer.summarize_statistics(stats_data)
        
        has_summary = len(summary) > 0
        results["tests"].append({
            "name": "Statistics Summary",
            "status": "PASS" if has_summary else "FAIL",
            "message": "Summary generated successfully" if has_summary else "No summary generated",
            "sample_output": summary[:200] + "..." if len(summary) > 200 else summary
        })
        print(f"   {'✓' if has_summary else '✗'} Statistics Summary")
    except Exception as e:
        results["tests"].append({
            "name": "Statistics Summary",
            "status": "ERROR",
            "message": str(e)
        })
        print(f"   ✗ Statistics Summary Error: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(1 for t in results["tests"] if t["status"] == "PASS")
    failed = sum(1 for t in results["tests"] if t["status"] == "FAIL")
    errors = sum(1 for t in results["tests"] if t["status"] == "ERROR")
    
    print(f"Test Summary: {passed} passed, {failed} failed, {errors} errors")
    print("=" * 60)
    
    # Save results
    save_results(results)
    
    return results

def save_results(results):
    """Save test results to JSON file."""
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test-results")
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "xai_api_test.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    main()
