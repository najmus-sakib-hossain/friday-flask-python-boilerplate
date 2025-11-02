#!/usr/bin/env python3
"""
Comprehensive API Testing Script
Tests all endpoints to ensure Vercel deployment readiness
"""
import requests
import json
import time

BASE_URL = "http://localhost:8080"

def test_endpoint(method, endpoint, data=None, expected_status=200, description=""):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n{'='*60}")
    print(f"Testing: {description or endpoint}")
    print(f"{'='*60}")
    print(f"Method: {method}")
    print(f"URL: {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            print(f"Data: {json.dumps(data, indent=2)}")
            response = requests.post(url, json=data, timeout=10)
        
        print(f"\nStatus Code: {response.status_code}")
        
        # Check if response is JSON
        try:
            response_data = response.json()
            print(f"Response: {json.dumps(response_data, indent=2)}")
        except:
            print(f"Response (text): {response.text[:500]}")
        
        if response.status_code == expected_status:
            print("✅ PASS")
            return True
        else:
            print(f"⚠️  Expected {expected_status}, got {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ FAIL - Could not connect to server")
        print("   Make sure the Flask app is running!")
        return False
    except Exception as e:
        print(f"❌ FAIL - {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("🚀 Flask API - Comprehensive Testing Suite")
    print("="*60)
    print(f"\nBase URL: {BASE_URL}")
    print(f"Testing started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Test 1: Home Page
    results.append(test_endpoint(
        "GET", "/",
        description="Home Page (HTML)"
    ))
    
    # Test 2: Sample Data Endpoint
    results.append(test_endpoint(
        "GET", "/api/data",
        description="Get Sample Data"
    ))
    
    # Test 3: Get Item by ID
    results.append(test_endpoint(
        "GET", "/api/items/1",
        description="Get Item by ID (id=1)"
    ))
    
    # Test 4: Get Item by ID (different ID)
    results.append(test_endpoint(
        "GET", "/api/items/42",
        description="Get Item by ID (id=42)"
    ))
    
    # Test 5: Multimodal API Guide
    results.append(test_endpoint(
        "GET", "/api/multimodal",
        description="Multimodal API Guide"
    ))
    
    # Test 6: Generate Image (will fail without env vars, but tests endpoint)
    results.append(test_endpoint(
        "POST", "/api/generate-image",
        data={"prompt": "A beautiful sunset"},
        expected_status=503,  # Expected to fail without config
        description="Generate Image (without env vars - should return 503)"
    ))
    
    # Test 7: Generate Image with bad request (no prompt)
    results.append(test_endpoint(
        "POST", "/api/generate-image",
        data={},
        expected_status=400,
        description="Generate Image (bad request - no prompt)"
    ))
    
    # Test 8: Generate Music (will fail without env vars)
    results.append(test_endpoint(
        "POST", "/api/generate-music",
        data={"prompt": "Upbeat electronic music"},
        expected_status=503,  # Expected to fail without config
        description="Generate Music (without env vars - should return 503)"
    ))
    
    # Test 9: Start Video (will fail without env vars)
    results.append(test_endpoint(
        "POST", "/api/video/start",
        data={"prompt": "A drone flying over beach"},
        expected_status=503,  # Expected to fail without config
        description="Start Video Generation (without env vars - should return 503)"
    ))
    
    # Print Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED!")
        print("\n🎉 Your app is ready for Vercel deployment!")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        print("\nCheck the failures above for details.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
