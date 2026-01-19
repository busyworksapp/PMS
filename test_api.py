#!/usr/bin/env python
"""
API Testing Script for Barron Manufacturing System
Tests all major endpoints and workflows
"""

import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
TOKEN = None

def log_test(title, status, details=""):
    """Log test results."""
    symbol = "✅" if status else "❌"
    print(f"\n{symbol} {title}")
    if details:
        print(f"   {details}")

def test_health_check():
    """Test health endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            log_test("Health Check", True, response.json())
            return True
    except Exception as e:
        log_test("Health Check", False, str(e))
    return False

def test_root():
    """Test root endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            log_test("Root Endpoint", True, f"Message: {data.get('message')}")
            return True
    except Exception as e:
        log_test("Root Endpoint", False, str(e))
    return False

def test_create_user():
    """Test user creation."""
    global TOKEN
    try:
        payload = {
            "email": f"testuser_{datetime.now().timestamp()}@test.com",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=payload,
            timeout=5
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            TOKEN = data.get("access_token")
            log_test("User Registration", True, f"Email: {payload['email']}")
            return True
        else:
            log_test("User Registration", False, f"Status: {response.status_code}, {response.text[:200]}")
    except Exception as e:
        log_test("User Registration", False, str(e))
    return False

def test_login():
    """Test user login."""
    global TOKEN
    try:
        payload = {
            "email": "testuser@test.com",
            "password": "TestPassword123!"
        }
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            TOKEN = data.get("access_token")
            log_test("User Login", True, f"Token received: {TOKEN[:20]}...")
            return True
        else:
            log_test("User Login", False, f"Status: {response.status_code}")
    except Exception as e:
        log_test("User Login", False, str(e))
    return False

def test_master_data():
    """Test master data endpoints."""
    if not TOKEN:
        log_test("Master Data Endpoints", False, "No token available")
        return False
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    # Test departments
    try:
        response = requests.get(
            f"{BASE_URL}/api/master/departments?skip=0&limit=10",
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            count = len(data) if isinstance(data, list) else data.get("total", 0)
            log_test("GET /api/master/departments", True, f"Found {count} departments")
        else:
            log_test("GET /api/master/departments", False, f"Status: {response.status_code}")
    except Exception as e:
        log_test("GET /api/master/departments", False, str(e))
    
    # Test products
    try:
        response = requests.get(
            f"{BASE_URL}/api/master/products?skip=0&limit=10",
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            count = len(data) if isinstance(data, list) else data.get("total", 0)
            log_test("GET /api/master/products", True, f"Found {count} products")
        else:
            log_test("GET /api/master/products", False, f"Status: {response.status_code}")
    except Exception as e:
        log_test("GET /api/master/products", False, str(e))
    
    # Test machines
    try:
        response = requests.get(
            f"{BASE_URL}/api/master/machines?skip=0&limit=10",
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            count = len(data) if isinstance(data, list) else data.get("total", 0)
            log_test("GET /api/master/machines", True, f"Found {count} machines")
        else:
            log_test("GET /api/master/machines", False, f"Status: {response.status_code}")
    except Exception as e:
        log_test("GET /api/master/machines", False, str(e))

def test_orders():
    """Test orders endpoints."""
    if not TOKEN:
        log_test("Orders Endpoints", False, "No token available")
        return False
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/jobs/orders?skip=0&limit=10",
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            count = len(data) if isinstance(data, list) else data.get("total", 0)
            log_test("GET /api/jobs/orders", True, f"Found {count} orders")
        else:
            log_test("GET /api/jobs/orders", False, f"Status: {response.status_code}")
    except Exception as e:
        log_test("GET /api/jobs/orders", False, str(e))

def test_defects():
    """Test defects endpoints."""
    if not TOKEN:
        log_test("Defects Endpoints", False, "No token available")
        return False
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/defects/rejects?skip=0&limit=10",
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            count = len(data) if isinstance(data, list) else data.get("total", 0)
            log_test("GET /api/defects/rejects", True, f"Found {count} defects")
        else:
            log_test("GET /api/defects/rejects", False, f"Status: {response.status_code}")
    except Exception as e:
        log_test("GET /api/defects/rejects", False, str(e))

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("BARRON MANUFACTURING SYSTEM - API TESTING")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Run tests
    test_health_check()
    test_root()
    test_create_user()
    
    if TOKEN:
        test_master_data()
        test_orders()
        test_defects()
    
    print("\n" + "="*60)
    print("API TESTING COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
