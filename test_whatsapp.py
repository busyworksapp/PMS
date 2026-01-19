#!/usr/bin/env python3
"""
WhatsApp Integration Test Script
Tests all WhatsApp API endpoints

Usage:
    python test_whatsapp.py
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
API_BASE = "http://127.0.0.1:8000/api/whatsapp"
TIMEOUT = 5


class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def print_header(text):
    """Print section header"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f" {text}")
    print(f"{'='*60}{Colors.END}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_info(text):
    """Print info message"""
    print(f"{Colors.YELLOW}ℹ {text}{Colors.END}")


def test_health():
    """Test health endpoint"""
    print_header("Test 1: Health Check")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=TIMEOUT)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(json.dumps(data, indent=2))
        
        if response.status_code == 200:
            print_success("Health check passed")
            return True
        else:
            print_error("Health check failed")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_get_contacts():
    """Test get contacts endpoint"""
    print_header("Test 2: Get Contacts")
    try:
        response = requests.get(f"{API_BASE}/contacts", timeout=TIMEOUT)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(json.dumps(data, indent=2))
        
        if response.status_code == 200:
            print_success(
                f"Retrieved {data.get('total_count', 0)} contacts"
            )
            return True
        else:
            print_error("Failed to get contacts")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_send_message():
    """Test send message endpoint"""
    print_header("Test 3: Send Message (Requires Config)")
    print_info(
        "This test requires WHATSAPP_API_TOKEN to be configured"
    )


def test_get_stats():
    """Test get statistics endpoint"""
    print_header("Test 4: Get Statistics")
    try:
        response = requests.get(f"{API_BASE}/stats", timeout=TIMEOUT)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(json.dumps(data, indent=2))

        if response.status_code == 200:
            total_msg = data.get('total_messages', 0)
            total_con = data.get('total_contacts', 0)
            print_success(
                f"Total messages: {total_msg}, "
                f"Total contacts: {total_con}"
            )
            return True
        else:
            print_error("Failed to get statistics")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_database_connection():
    """Test database connection"""
    print_header("Test 5: Database Connection")
    try:
        # This implicitly tests database by trying to get contacts
        response = requests.get(f"{API_BASE}/contacts", timeout=TIMEOUT)

        if response.status_code == 200:
            print_success("Database connected successfully")
            return True
        else:
            print_error("Database connection failed")
            return False
    except requests.ConnectionError:
        msg = "Cannot connect to backend (is it running on :8000?)"
        print_error(msg)
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def run_all_tests():
    """Run all tests"""
    header = '='*60
    print(f"\n{Colors.BLUE}{header}")
    print(" WhatsApp Integration Test Suite")
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f" Started: {ts}")
    print(f"{header}{Colors.END}")
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Health Check", test_health),
        ("Get Contacts", test_get_contacts),
        ("Send Message", test_send_message),
        ("Get Statistics", test_get_stats),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"Test '{name}' crashed: {str(e)}")
            results.append((name, False))
    
    # Print summary
    print_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        pass_str = f"{Colors.GREEN}PASS{Colors.END}"
        fail_str = f"{Colors.RED}FAIL{Colors.END}"
        status = pass_str if result else fail_str
        print(f"  {status} - {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print_success("All tests passed!")
        return 0
    else:
        print_error(f"{total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    try:
        exit_code = run_all_tests()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
