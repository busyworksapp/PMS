#!/usr/bin/env python
"""Create test user for Barron Production Management System."""

import requests
import json

BASE_URL = "http://127.0.0.1:8001"


def create_test_user():
    """Create test user via API."""
    user_data = {
        "username": "admin",
        "password": "admin123",
        "email": "admin@barron.com",
        "fullname": "System Administrator",
        "employee_number": "ADM001",
        "role": "admin",
        "department_id": None
    }
    
    print("Creating test user...")
    print(f"POST {BASE_URL}/api/auth/register")
    print(f"Data: {json.dumps(user_data, indent=2)}")
    print()
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=user_data,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        print()
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS! Test user created:")
            print(f"  Username: {result.get('username')}")
            print(f"  Email: {result.get('email')}")
            print(f"  ID: {result.get('id')}")
            print()
            print("🔐 Login credentials:")
            print("  Username: admin")
            print("  Password: admin123")
            print()
            print("📍 Next step: Go to")
            print("   http://localhost:3000/templates/login.html")
            return True
        else:
            print(f"❌ Failed to create user: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"   Make sure the backend is running on {BASE_URL}")
        return False

if __name__ == "__main__":
    create_test_user()
