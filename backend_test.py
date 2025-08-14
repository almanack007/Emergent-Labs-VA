#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class VoiceAgendaAPITester:
    def __init__(self, base_url="http://127.0.0.1:8001"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status=200, expected_keys=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json={}, headers=headers, timeout=10)

            print(f"   Status Code: {response.status_code}")
            
            success = response.status_code == expected_status
            if success:
                try:
                    data = response.json()
                    print(f"   Response: {json.dumps(data, indent=2)[:200]}...")
                    
                    # Check for expected keys if provided
                    if expected_keys:
                        missing_keys = []
                        for key in expected_keys:
                            if key not in data:
                                missing_keys.append(key)
                        
                        if missing_keys:
                            print(f"   ❌ Missing expected keys: {missing_keys}")
                            success = False
                        else:
                            print(f"   ✅ All expected keys present: {expected_keys}")
                    
                    if success:
                        self.tests_passed += 1
                        print(f"✅ PASSED - {name}")
                    
                    return success, data
                    
                except json.JSONDecodeError:
                    print(f"   ❌ Invalid JSON response")
                    return False, {}
            else:
                print(f"❌ FAILED - {name} - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                return False, {}

        except requests.exceptions.RequestException as e:
            print(f"❌ FAILED - {name} - Network Error: {str(e)}")
            return False, {}

    def test_health(self):
        """Test health endpoint"""
        return self.run_test(
            "Health Check",
            "GET",
            "api/health",
            200,
            ["status"]
        )

    def test_kpis(self):
        """Test KPIs endpoint"""
        return self.run_test(
            "KPIs Endpoint",
            "GET", 
            "api/kpis",
            200,
            ["callVolume", "resolutionRate", "sentiment", "jobTypeDistribution", "trend"]
        )

    def test_calls(self):
        """Test calls endpoint"""
        success, data = self.run_test(
            "Calls Endpoint",
            "GET",
            "api/calls", 
            200,
            ["items"]
        )
        
        if success and "items" in data and len(data["items"]) > 0:
            # Check first item has expected structure
            first_item = data["items"][0]
            expected_call_keys = ["id", "callerName", "callType", "datetime", "sentiment", "resolutionStatus"]
            missing_keys = [key for key in expected_call_keys if key not in first_item]
            
            if missing_keys:
                print(f"   ❌ Call items missing keys: {missing_keys}")
                return False, data
            else:
                print(f"   ✅ Call items have correct structure")
        
        return success, data

    def test_service_insights(self):
        """Test service insights endpoint"""
        return self.run_test(
            "Service Insights",
            "GET",
            "api/service-insights",
            200,
            ["categories"]
        )

    def test_summaries(self):
        """Test summaries endpoint"""
        return self.run_test(
            "Post-Call Summaries",
            "GET",
            "api/summaries",
            200,
            ["items"]
        )

    def test_integrations(self):
        """Test integrations endpoint"""
        return self.run_test(
            "Integrations",
            "GET",
            "api/integrations",
            200,
            ["items"]
        )

    def test_settings(self):
        """Test settings endpoint"""
        return self.run_test(
            "Settings",
            "GET",
            "api/settings",
            200,
            ["security", "dataRetention", "accessControls"]
        )

def main():
    print("🚀 Starting Voice Agenda API Tests")
    print("=" * 50)
    
    tester = VoiceAgendaAPITester()
    
    # Run all tests
    test_methods = [
        tester.test_health,
        tester.test_kpis,
        tester.test_calls,
        tester.test_service_insights,
        tester.test_summaries,
        tester.test_integrations,
        tester.test_settings
    ]
    
    for test_method in test_methods:
        try:
            test_method()
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
    
    # Print final results
    print("\n" + "=" * 50)
    print(f"📊 FINAL RESULTS")
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Tests Failed: {tester.tests_run - tester.tests_passed}")
    print(f"Success Rate: {(tester.tests_passed/tester.tests_run*100):.1f}%" if tester.tests_run > 0 else "0%")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 ALL TESTS PASSED!")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED!")
        return 1

if __name__ == "__main__":
    sys.exit(main())