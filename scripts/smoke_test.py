#!/usr/bin/env python
"""
Smoke test for Barron Manufacturing System
Tests basic backend and frontend connectivity
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://127.0.0.1:8001"
FRONTEND_URL = "http://127.0.0.1:8080"

def log_test(name, passed, details=""):
    """Log test result."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} | {name}")
    if details:
        print(f"      {details}")

def test_backend_health():
    """Test backend health endpoint."""
    try:
        resp = requests.get(f"{BASE_URL}/health", timeout=5)
        passed = resp.status_code == 200 and resp.json().get("status") == "ok"
        log_test("Backend Health Check", passed, f"Status: {resp.status_code}")
        return passed
    except Exception as e:
        log_test("Backend Health Check", False, str(e))
        return False

def test_backend_root():
    """Test root endpoint."""
    try:
        resp = requests.get(f"{BASE_URL}/", timeout=5)
        passed = resp.status_code == 200
        log_test("Backend Root Endpoint", passed, f"Status: {resp.status_code}")
        return passed
    except Exception as e:
        log_test("Backend Root Endpoint", False, str(e))
        return False

def test_backend_docs():
    """Test Swagger docs."""
    try:
        resp = requests.get(f"{BASE_URL}/docs", timeout=5)
        passed = resp.status_code == 200
        log_test("Backend Swagger Docs", passed, f"Status: {resp.status_code}")
        return passed
    except Exception as e:
        log_test("Backend Swagger Docs", False, str(e))
        return False

def test_frontend_index():
    """Test frontend index page."""
    try:
        resp = requests.get(f"{FRONTEND_URL}/", timeout=5)
        passed = resp.status_code == 200
        log_test("Frontend Index Page", passed, f"Status: {resp.status_code}")
        return passed
    except Exception as e:
        log_test("Frontend Index Page", False, str(e))
        return False

def test_frontend_login():
    """Test frontend login page."""
    try:
        resp = requests.get(f"{FRONTEND_URL}/login.html", timeout=5)
        passed = resp.status_code == 200
        log_test("Frontend Login Page", passed, f"Status: {resp.status_code}")
        return passed
    except Exception as e:
        log_test("Frontend Login Page", False, str(e))
        return False

def test_frontend_dashboard():
    """Test frontend dashboard page."""
    try:
        resp = requests.get(f"{FRONTEND_URL}/dashboard.html", timeout=5)
        passed = resp.status_code == 200
        log_test("Frontend Dashboard Page", passed, f"Status: {resp.status_code}")
        return passed
    except Exception as e:
        log_test("Frontend Dashboard Page", False, str(e))
        return False

def main():
    """Run all smoke tests."""
    print("\n" + "="*60)
    print("Barron Manufacturing System - Smoke Test")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    tests = [
        test_backend_health,
        test_backend_root,
        test_backend_docs,
        test_frontend_index,
        test_frontend_login,
        test_frontend_dashboard,
    ]
    
    results = [test() for test in tests]
    
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    print(f"Summary: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    return 0 if all(results) else 1

if __name__ == "__main__":
    sys.exit(main())
